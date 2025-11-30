"""Integration tests for db.repositories.run_repository module.

These tests use a real SQLite database to test end-to-end functionality.
"""

import os
import tempfile
import time

import pytest

from db.db import DB_PATH, get_connection, initialize_database
from db.exceptions import InvalidTransitionError, RunNotFoundError
from db.repositories.run_repository import create_sqlite_repository
from simulation.core.models.runs import Run, RunConfig, RunStatus


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    # Save original DB path
    original_path = DB_PATH

    # Create temporary database
    fd, temp_path = tempfile.mkstemp(suffix=".sqlite")
    os.close(fd)

    # Monkey-patch DB_PATH
    import db.db

    db.db.DB_PATH = temp_path

    # Initialize the database
    initialize_database()

    yield temp_path

    # Cleanup
    db.db.DB_PATH = original_path
    if os.path.exists(temp_path):
        os.unlink(temp_path)


class TestSQLiteRunRepositoryIntegration:
    """Integration tests using a real database."""

    def test_create_and_read_run(self, temp_db):
        """Test creating a run and reading it back from the database."""
        repo = create_sqlite_repository()
        config = RunConfig(num_agents=5, num_turns=10)

        # Create run
        created_run = repo.create_run(config)
        assert created_run.status == RunStatus.RUNNING
        assert created_run.total_agents == 5
        assert created_run.total_turns == 10

        # Read it back
        retrieved_run = repo.get_run(created_run.run_id)
        assert retrieved_run is not None
        assert retrieved_run.run_id == created_run.run_id
        assert retrieved_run.status == RunStatus.RUNNING
        assert retrieved_run.total_agents == 5
        assert retrieved_run.total_turns == 10

    def test_update_run_status_to_completed(self, temp_db):
        """Test updating run status to completed."""
        repo = create_sqlite_repository()
        config = RunConfig(num_agents=3, num_turns=5)

        run = repo.create_run(config)

        # Update to completed
        repo.update_run_status(run.run_id, RunStatus.COMPLETED)

        # Verify update
        updated_run = repo.get_run(run.run_id)
        assert updated_run is not None
        assert updated_run.status == RunStatus.COMPLETED
        assert updated_run.completed_at is not None

    def test_update_run_status_to_failed(self, temp_db):
        """Test updating run status to failed."""
        repo = create_sqlite_repository()
        config = RunConfig(num_agents=3, num_turns=5)

        run = repo.create_run(config)

        # Update to failed
        repo.update_run_status(run.run_id, RunStatus.FAILED)

        # Verify update
        updated_run = repo.get_run(run.run_id)
        assert updated_run is not None
        assert updated_run.status == RunStatus.FAILED
        assert updated_run.completed_at is None

    def test_update_run_status_nonexistent_run(self, temp_db):
        """Test updating status of a non-existent run raises error."""
        repo = create_sqlite_repository()

        with pytest.raises(RunNotFoundError) as exc_info:
            repo.update_run_status("nonexistent_run_id", RunStatus.COMPLETED)

        assert exc_info.value.run_id == "nonexistent_run_id"

    def test_list_runs_returns_all_runs_ordered(self, temp_db):
        """Test that list_runs returns all runs in correct order."""
        repo = create_sqlite_repository()

        # Create multiple runs with delays to ensure distinct timestamps
        run1 = repo.create_run(RunConfig(num_agents=1, num_turns=1))
        time.sleep(1.1)  # Ensure different timestamp (format is down to seconds)
        run2 = repo.create_run(RunConfig(num_agents=2, num_turns=2))
        time.sleep(1.1)
        run3 = repo.create_run(RunConfig(num_agents=3, num_turns=3))

        # List runs (should be ordered by created_at DESC, so newest first)
        runs = repo.list_runs()

        assert len(runs) >= 3
        # Verify ordering (newest first)
        run_ids = [r.run_id for r in runs[:3]]
        expected_order = [run3.run_id, run2.run_id, run1.run_id]
        assert run_ids == expected_order


class TestRunStatusEnumSerialization:
    """Tests for RunStatus enum serialization/deserialization."""

    def test_enum_serializes_to_correct_string(self, temp_db):
        """Test that RunStatus enum values serialize correctly."""
        from db.db import write_run

        run = Run(
            run_id="test_run_1",
            created_at="2024_01_01-12:00:00",
            total_turns=5,
            total_agents=3,
            started_at="2024_01_01-12:00:00",
            status=RunStatus.RUNNING,
            completed_at=None,
        )

        write_run(run)

        # Read directly from DB to verify string storage
        conn = get_connection()
        row = conn.execute(
            "SELECT status FROM runs WHERE run_id = ?", (run.run_id,)
        ).fetchone()
        assert row["status"] == "running"
        conn.close()

    def test_invalid_status_string_raises_error(self, temp_db):
        """Test that reading invalid status string raises ValueError."""
        from unittest.mock import MagicMock

        from db.db import _row_to_run

        # We can't insert invalid status due to CHECK constraint, so we test _row_to_run directly
        # This simulates what would happen if the database had invalid data (e.g., from manual edits)

        # Create a mock row that simulates invalid status
        mock_row = MagicMock()

        def getitem(key):
            mapping = {
                "run_id": "test_run",
                "created_at": "2024_01_01-12:00:00",
                "total_turns": 5,
                "total_agents": 3,
                "started_at": "2024_01_01-12:00:00",
                "status": "invalid_status",  # Invalid status value
                "completed_at": None,
            }
            return mapping.get(key)

        # Configure mock to work with row[key] syntax
        type(mock_row).__getitem__ = lambda self, key: getitem(key)
        mock_row.keys = lambda: [
            "run_id",
            "created_at",
            "total_turns",
            "total_agents",
            "started_at",
            "status",
            "completed_at",
        ]

        # Test that _row_to_run raises ValueError for invalid status
        with pytest.raises(ValueError, match="Invalid status value"):
            _row_to_run(mock_row)

    def test_all_status_values_roundtrip(self, temp_db):
        """Test that all RunStatus enum values roundtrip correctly."""
        repo = create_sqlite_repository()
        config = RunConfig(num_agents=2, num_turns=2)

        # Test RUNNING status (default from create_run)
        run_running = repo.create_run(config)
        retrieved = repo.get_run(run_running.run_id)
        assert retrieved is not None
        assert retrieved.status == RunStatus.RUNNING

        # Test COMPLETED status (valid transition from RUNNING)
        run_completed = repo.create_run(config)
        repo.update_run_status(run_completed.run_id, RunStatus.COMPLETED)
        retrieved = repo.get_run(run_completed.run_id)
        assert retrieved is not None
        assert retrieved.status == RunStatus.COMPLETED

        # Test FAILED status (valid transition from RUNNING)
        run_failed = repo.create_run(config)
        repo.update_run_status(run_failed.run_id, RunStatus.FAILED)
        retrieved = repo.get_run(run_failed.run_id)
        assert retrieved is not None
        assert retrieved.status == RunStatus.FAILED

        # Test idempotent updates (setting same status again)
        repo.update_run_status(run_completed.run_id, RunStatus.COMPLETED)
        retrieved = repo.get_run(run_completed.run_id)
        assert retrieved is not None
        assert retrieved.status == RunStatus.COMPLETED

        repo.update_run_status(run_failed.run_id, RunStatus.FAILED)
        retrieved = repo.get_run(run_failed.run_id)
        assert retrieved is not None
        assert retrieved.status == RunStatus.FAILED


class TestConcurrentRunCreation:
    """Tests for concurrent run creation scenarios."""

    def test_concurrent_run_creation_generates_unique_ids(self, temp_db):
        """Test that concurrent run creation generates unique run IDs."""
        import threading

        repo = create_sqlite_repository()
        config = RunConfig(num_agents=1, num_turns=1)

        run_ids = []
        errors = []

        def create_run():
            try:
                run = repo.create_run(config)
                run_ids.append(run.run_id)
            except Exception as e:
                errors.append(e)

        # Create runs concurrently
        threads = [threading.Thread(target=create_run) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Verify all succeeded
        assert len(errors) == 0
        assert len(run_ids) == 10

        # Verify all IDs are unique
        assert len(set(run_ids)) == 10


class TestStateMachineValidationIntegration:
    """Integration tests for state machine validation."""

    def test_valid_transition_running_to_completed(self, temp_db):
        """Test that RUNNING -> COMPLETED transition works with real database."""
        repo = create_sqlite_repository()
        config = RunConfig(num_agents=3, num_turns=5)

        run = repo.create_run(config)
        assert run.status == RunStatus.RUNNING

        # Transition to completed
        repo.update_run_status(run.run_id, RunStatus.COMPLETED)

        updated_run = repo.get_run(run.run_id)
        assert updated_run is not None
        assert updated_run.status == RunStatus.COMPLETED

    def test_valid_transition_running_to_failed(self, temp_db):
        """Test that RUNNING -> FAILED transition works with real database."""
        repo = create_sqlite_repository()
        config = RunConfig(num_agents=3, num_turns=5)

        run = repo.create_run(config)
        assert run.status == RunStatus.RUNNING

        # Transition to failed
        repo.update_run_status(run.run_id, RunStatus.FAILED)

        updated_run = repo.get_run(run.run_id)
        assert updated_run is not None
        assert updated_run.status == RunStatus.FAILED

    def test_invalid_transition_completed_to_failed(self, temp_db):
        """Test that COMPLETED -> FAILED transition is rejected."""
        repo = create_sqlite_repository()
        config = RunConfig(num_agents=3, num_turns=5)

        run = repo.create_run(config)
        repo.update_run_status(run.run_id, RunStatus.COMPLETED)

        # Try invalid transition
        with pytest.raises(InvalidTransitionError) as exc_info:
            repo.update_run_status(run.run_id, RunStatus.FAILED)

        assert exc_info.value.run_id == run.run_id
        assert exc_info.value.current_status == "completed"
        assert exc_info.value.target_status == "failed"

        # Verify status is still COMPLETED
        updated_run = repo.get_run(run.run_id)
        assert updated_run is not None
        assert updated_run.status == RunStatus.COMPLETED

    def test_invalid_transition_failed_to_completed(self, temp_db):
        """Test that FAILED -> COMPLETED transition is rejected."""
        repo = create_sqlite_repository()
        config = RunConfig(num_agents=3, num_turns=5)

        run = repo.create_run(config)
        repo.update_run_status(run.run_id, RunStatus.FAILED)

        # Try invalid transition
        with pytest.raises(InvalidTransitionError) as exc_info:
            repo.update_run_status(run.run_id, RunStatus.COMPLETED)

        assert exc_info.value.run_id == run.run_id
        assert exc_info.value.current_status == "failed"
        assert exc_info.value.target_status == "completed"

        # Verify status is still FAILED
        updated_run = repo.get_run(run.run_id)
        assert updated_run is not None
        assert updated_run.status == RunStatus.FAILED

    def test_invalid_transition_completed_to_running(self, temp_db):
        """Test that COMPLETED -> RUNNING transition is rejected."""
        repo = create_sqlite_repository()
        config = RunConfig(num_agents=3, num_turns=5)

        run = repo.create_run(config)
        repo.update_run_status(run.run_id, RunStatus.COMPLETED)

        # Try invalid transition
        with pytest.raises(InvalidTransitionError) as exc_info:
            repo.update_run_status(run.run_id, RunStatus.RUNNING)

        assert exc_info.value.run_id == run.run_id
        assert exc_info.value.current_status == "completed"
        assert exc_info.value.target_status == "running"

        # Verify status is still COMPLETED
        updated_run = repo.get_run(run.run_id)
        assert updated_run is not None
        assert updated_run.status == RunStatus.COMPLETED

    def test_idempotent_status_update_completed(self, temp_db):
        """Test that setting COMPLETED status again is allowed (idempotent)."""
        repo = create_sqlite_repository()
        config = RunConfig(num_agents=3, num_turns=5)

        run = repo.create_run(config)
        repo.update_run_status(run.run_id, RunStatus.COMPLETED)

        # Setting to COMPLETED again should work
        repo.update_run_status(run.run_id, RunStatus.COMPLETED)

        updated_run = repo.get_run(run.run_id)
        assert updated_run is not None
        assert updated_run.status == RunStatus.COMPLETED

    def test_idempotent_status_update_failed(self, temp_db):
        """Test that setting FAILED status again is allowed (idempotent)."""
        repo = create_sqlite_repository()
        config = RunConfig(num_agents=3, num_turns=5)

        run = repo.create_run(config)
        repo.update_run_status(run.run_id, RunStatus.FAILED)

        # Setting to FAILED again should work
        repo.update_run_status(run.run_id, RunStatus.FAILED)

        updated_run = repo.get_run(run.run_id)
        assert updated_run is not None
        assert updated_run.status == RunStatus.FAILED


def _create_mock_row(**overrides):
    """Helper function to create a MockRow that mimics sqlite3.Row behavior.

    Args:
        **overrides: Dictionary of field overrides to apply to default values.

    Returns:
        MockRow instance with __getitem__ and keys methods.
    """
    default_data = {
        "run_id": "test_run",
        "created_at": "2024_01_01-12:00:00",
        "total_turns": 5,
        "total_agents": 3,
        "started_at": "2024_01_01-12:00:00",
        "status": "running",
        "completed_at": None,
    }
    default_data.update(overrides)

    class MockRow:
        def __init__(self, data):
            self._data = data

        def __getitem__(self, key):
            return self._data[key]

        def keys(self):
            return list(self._data.keys())

    return MockRow(default_data)


class TestNullabilityValidation:
    """Tests for nullability validation when reading runs."""

    def test_null_run_id_raises_error(self, temp_db):
        """Test that NULL run_id raises ValueError."""
        from db.db import _row_to_run

        mock_row = _create_mock_row(run_id=None)

        with pytest.raises(ValueError, match="run_id cannot be NULL"):
            _row_to_run(mock_row)  # type: ignore

    def test_null_status_raises_error(self, temp_db):
        """Test that NULL status raises ValueError."""
        from db.db import _row_to_run

        mock_row = _create_mock_row(status=None)

        with pytest.raises(ValueError, match="status cannot be NULL"):
            _row_to_run(mock_row)  # type: ignore
