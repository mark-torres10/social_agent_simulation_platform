"""Tests for db.repositories.run_repository module."""

import pytest
from unittest.mock import patch
from db.repositories.run_repository import SQLiteRunRepository
from db.models import RunConfig, Run, RunStatus


class TestSQLiteRunRepositoryCreateRun:
    """Tests for SQLiteRunRepository.create_run method."""
    
    def test_creates_run_with_correct_config_values(self):
        """Test that create_run creates a run with correct configuration values."""
        import uuid
        # Arrange
        repo = SQLiteRunRepository()
        config = RunConfig(num_agents=5, num_turns=10)
        expected_timestamp = "2024_01_01-12:00:00"
        mock_uuid = uuid.UUID('12345678-1234-5678-9012-123456789012')
        
        with patch("lib.utils.get_current_timestamp", return_value=expected_timestamp):
            with patch("db.repositories.run_repository.uuid.uuid4", return_value=mock_uuid):
                with patch("db.db.write_run") as mock_write:
                    # Act
                    result = repo.create_run(config)
                    
                    # Assert
                    expected_run_id = f"run_{expected_timestamp}_{mock_uuid}"
                    assert result.run_id == expected_run_id
                    assert result.created_at == expected_timestamp
                    assert result.total_turns == 10
                    assert result.total_agents == 5
                    assert result.started_at == expected_timestamp
                    assert result.status == RunStatus.RUNNING
                    assert result.completed_at == None
    
    def test_creates_run_with_different_config_values(self):
        """Test that create_run handles different configuration values correctly."""
        import uuid
        # Arrange
        repo = SQLiteRunRepository()
        config = RunConfig(num_agents=20, num_turns=50)
        expected_timestamp = "2024_02_15-15:30:45"
        mock_uuid = uuid.UUID('00000000-0000-0000-0000-000000000000')
        
        with patch("lib.utils.get_current_timestamp", return_value=expected_timestamp):
            with patch("db.repositories.run_repository.uuid.uuid4", return_value=mock_uuid):
                with patch("db.db.write_run") as mock_write:
                    # Act
                    result = repo.create_run(config)
                    
                    # Assert
                    assert result.total_agents == 20
                    assert result.total_turns == 50
                    assert result.run_id.startswith(f"run_{expected_timestamp}_")
    
    def test_persists_run_to_database(self):
        """Test that create_run persists the run to the database via write_run."""
        # Arrange
        repo = SQLiteRunRepository()
        config = RunConfig(num_agents=5, num_turns=10)
        expected_timestamp = "2024_01_01-12:00:00"
        
        with patch("lib.utils.get_current_timestamp", return_value=expected_timestamp):
            with patch("db.db.write_run") as mock_write:
                # Act
                result = repo.create_run(config)
                
                # Assert
                mock_write.assert_called_once()
                call_args = mock_write.call_args[0][0]
                assert isinstance(call_args, Run)
                assert call_args.run_id == result.run_id
                assert call_args.total_agents == 5
                assert call_args.total_turns == 10
                assert call_args.status == RunStatus.RUNNING
    
    def test_generates_unique_run_id_with_timestamp(self):
        """Test that create_run generates a unique run_id using timestamp and UUID."""
        import uuid
        # Arrange
        repo = SQLiteRunRepository()
        config = RunConfig(num_agents=5, num_turns=10)
        timestamp1 = "2024_01_01-12:00:00"
        timestamp2 = "2024_01_01-12:00:01"
        uuid1 = uuid.UUID('11111111-1111-1111-1111-111111111111')
        uuid2 = uuid.UUID('22222222-2222-2222-2222-222222222222')
        
        with patch("lib.utils.get_current_timestamp", side_effect=[timestamp1, timestamp2]):
            with patch("db.repositories.run_repository.uuid.uuid4", side_effect=[uuid1, uuid2]):
                with patch("db.db.write_run"):
                    # Act
                    result1 = repo.create_run(config)
                    result2 = repo.create_run(config)
                    
                    # Assert
                    assert result1.run_id == f"run_{timestamp1}_{uuid1}"
                    assert result2.run_id == f"run_{timestamp2}_{uuid2}"
                    assert result1.run_id != result2.run_id
    
    def test_sets_status_to_running_on_creation(self):
        """Test that create_run always sets status to RUNNING."""
        # Arrange
        repo = SQLiteRunRepository()
        config = RunConfig(num_agents=5, num_turns=10)
        
        with patch("lib.utils.get_current_timestamp", return_value="2024_01_01-12:00:00"):
            with patch("db.db.write_run"):
                # Act
                result = repo.create_run(config)
                
                # Assert
                assert result.status == RunStatus.RUNNING
    
    def test_sets_completed_at_to_none_on_creation(self):
        """Test that create_run sets completed_at to None for new runs."""
        # Arrange
        repo = SQLiteRunRepository()
        config = RunConfig(num_agents=5, num_turns=10)
        
        with patch("lib.utils.get_current_timestamp", return_value="2024_01_01-12:00:00"):
            with patch("db.db.write_run"):
                # Act
                result = repo.create_run(config)
                
                # Assert
                assert result.completed_at is None
    
    def test_raises_runtime_error_when_write_run_fails(self):
        """Test that create_run raises RuntimeError when database write fails."""
        # Arrange
        repo = SQLiteRunRepository()
        config = RunConfig(num_agents=5, num_turns=10)
        expected_timestamp = "2024_01_01-12:00:00"
        expected_run_id = f"run_{expected_timestamp}"
        db_error = Exception("Database connection failed")
        
        with patch("lib.utils.get_current_timestamp", return_value=expected_timestamp):
            with patch("db.db.write_run", side_effect=db_error):
                # Act & Assert
                with pytest.raises(RuntimeError) as exc_info:
                    repo.create_run(config)
                
                assert f"Failed to create run {expected_run_id}" in str(exc_info.value)
                assert isinstance(exc_info.value.__cause__, Exception)
    
    def test_raises_runtime_error_with_correct_run_id_in_message(self):
        """Test that RuntimeError includes the correct run_id in the error message."""
        # Arrange
        repo = SQLiteRunRepository()
        config = RunConfig(num_agents=5, num_turns=10)
        expected_timestamp = "2024_01_01-12:00:00"
        expected_run_id = f"run_{expected_timestamp}"
        
        with patch("lib.utils.get_current_timestamp", return_value=expected_timestamp):
            with patch("db.db.write_run", side_effect=Exception("DB error")):
                # Act & Assert
                with pytest.raises(RuntimeError, match=f"Failed to create run {expected_run_id}"):
                    repo.create_run(config)
    
    def test_preserves_original_exception_in_runtime_error(self):
        """Test that the original exception is preserved as the cause of RuntimeError."""
        # Arrange
        repo = SQLiteRunRepository()
        config = RunConfig(num_agents=5, num_turns=10)
        original_error = ValueError("Invalid data")
        
        with patch("lib.utils.get_current_timestamp", return_value="2024_01_01-12:00:00"):
            with patch("db.db.write_run", side_effect=original_error):
                # Act & Assert
                with pytest.raises(RuntimeError) as exc_info:
                    repo.create_run(config)
                
                assert exc_info.value.__cause__ is original_error


class TestSQLiteRunRepositoryGetRun:
    """Tests for SQLiteRunRepository.get_run method."""
    
    def test_returns_run_when_found(self):
        """Test that get_run returns a Run when it exists in the database."""
        # Arrange
        repo = SQLiteRunRepository()
        run_id = "run_123"
        expected = Run(
            run_id=run_id,
            created_at="2024_01_01-12:00:00",
            total_turns=10,
            total_agents=5,
            started_at="2024_01_01-12:00:00",
            status=RunStatus.RUNNING,
            completed_at=None
        )
        
        with patch("db.db.read_run", return_value=expected):
            # Act
            result = repo.get_run(run_id)
            
            # Assert
            assert result is not None
            assert result.run_id == expected.run_id
            assert result.created_at == expected.created_at
            assert result.total_turns == expected.total_turns
            assert result.total_agents == expected.total_agents
            assert result.started_at == expected.started_at
            assert result.status == expected.status
            assert result.completed_at == expected.completed_at
    
    def test_returns_none_when_run_not_found(self):
        """Test that get_run returns None when run does not exist."""
        # Arrange
        repo = SQLiteRunRepository()
        run_id = "nonexistent_run"
        
        with patch("db.db.read_run", return_value=None):
            # Act
            result = repo.get_run(run_id)
            
            # Assert
            assert result is None
    
    def test_calls_read_run_with_correct_run_id(self):
        """Test that get_run calls read_run with the correct run_id parameter."""
        # Arrange
        repo = SQLiteRunRepository()
        run_id = "run_123"
        
        with patch("db.db.read_run") as mock_read:
            mock_read.return_value = None
            # Act
            repo.get_run(run_id)
            
            # Assert
            mock_read.assert_called_once_with(run_id)
    
    def test_returns_completed_run_correctly(self):
        """Test that get_run returns a completed run with completed_at timestamp."""
        # Arrange
        repo = SQLiteRunRepository()
        run_id = "run_123"
        expected = Run(
            run_id=run_id,
            created_at="2024_01_01-12:00:00",
            total_turns=10,
            total_agents=5,
            started_at="2024_01_01-12:00:00",
            status=RunStatus.COMPLETED,
            completed_at="2024_01_01-13:00:00"
        )
        
        with patch("db.db.read_run", return_value=expected):
            # Act
            result = repo.get_run(run_id)
            
            # Assert
            assert result is not None
            assert result.status == RunStatus.COMPLETED
            assert result.completed_at == "2024_01_01-13:00:00"
    
    def test_returns_failed_run_correctly(self):
        """Test that get_run returns a failed run correctly."""
        # Arrange
        repo = SQLiteRunRepository()
        run_id = "run_123"
        expected = Run(
            run_id=run_id,
            created_at="2024_01_01-12:00:00",
            total_turns=10,
            total_agents=5,
            started_at="2024_01_01-12:00:00",
            status=RunStatus.FAILED,
            completed_at=None
        )
        
        with patch("db.db.read_run", return_value=expected):
            # Act
            result = repo.get_run(run_id)
            
            # Assert
            assert result is not None
            assert result.status == RunStatus.FAILED


class TestSQLiteRunRepositoryListRuns:
    """Tests for SQLiteRunRepository.list_runs method."""
    
    def test_returns_empty_list_when_no_runs_exist(self):
        """Test that list_runs returns an empty list when no runs exist."""
        # Arrange
        repo = SQLiteRunRepository()
        expected = []
        
        with patch("db.db.read_all_runs", return_value=expected):
            # Act
            result = repo.list_runs()
            
            # Assert
            assert result == expected
            assert isinstance(result, list)
            assert len(result) == 0
    
    def test_returns_all_runs_when_runs_exist(self):
        """Test that list_runs returns all runs from the database."""
        # Arrange
        repo = SQLiteRunRepository()
        expected = [
            Run(
                run_id="run_1",
                created_at="2024_01_01-12:00:00",
                total_turns=10,
                total_agents=5,
                started_at="2024_01_01-12:00:00",
                status=RunStatus.COMPLETED,
                completed_at="2024_01_01-13:00:00"
            ),
            Run(
                run_id="run_2",
                created_at="2024_01_02-12:00:00",
                total_turns=20,
                total_agents=10,
                started_at="2024_01_02-12:00:00",
                status=RunStatus.RUNNING,
                completed_at=None
            )
        ]
        
        with patch("db.db.read_all_runs", return_value=expected):
            # Act
            result = repo.list_runs()
            
            # Assert
            assert len(result) == 2
            assert result[0].run_id == "run_1"
            assert result[1].run_id == "run_2"
    
    def test_returns_runs_in_correct_order(self):
        """Test that list_runs returns runs in the order provided by read_all_runs."""
        # Arrange
        repo = SQLiteRunRepository()
        expected = [
            Run(
                run_id="run_newest",
                created_at="2024_01_03-12:00:00",
                total_turns=10,
                total_agents=5,
                started_at="2024_01_03-12:00:00",
                status=RunStatus.RUNNING,
                completed_at=None
            ),
            Run(
                run_id="run_oldest",
                created_at="2024_01_01-12:00:00",
                total_turns=10,
                total_agents=5,
                started_at="2024_01_01-12:00:00",
                status=RunStatus.COMPLETED,
                completed_at="2024_01_01-13:00:00"
            )
        ]
        
        with patch("db.db.read_all_runs", return_value=expected):
            # Act
            result = repo.list_runs()
            
            # Assert
            assert result[0].run_id == "run_newest"
            assert result[1].run_id == "run_oldest"
    
    def test_calls_read_all_runs_once(self):
        """Test that list_runs calls read_all_runs exactly once."""
        # Arrange
        repo = SQLiteRunRepository()
        
        with patch("db.db.read_all_runs") as mock_read:
            mock_read.return_value = []
            # Act
            repo.list_runs()
            
            # Assert
            mock_read.assert_called_once()
    
    def test_handles_large_number_of_runs(self):
        """Test that list_runs handles a large number of runs correctly."""
        # Arrange
        repo = SQLiteRunRepository()
        expected = [
            Run(
                run_id=f"run_{i}",
                created_at=f"2024_01_{i:02d}-12:00:00",
                total_turns=10,
                total_agents=5,
                started_at=f"2024_01_{i:02d}-12:00:00",
                status=RunStatus.RUNNING,
                completed_at=None
            )
            for i in range(100)
        ]
        
        with patch("db.db.read_all_runs", return_value=expected):
            # Act
            result = repo.list_runs()
            
            # Assert
            assert len(result) == 100
            assert all(isinstance(run, Run) for run in result)


class TestSQLiteRunRepositoryUpdateRunStatus:
    """Tests for SQLiteRunRepository.update_run_status method."""
    
    def test_updates_status_to_completed(self):
        """Test that update_run_status updates status to COMPLETED correctly."""
        # Arrange
        repo = SQLiteRunRepository()
        run_id = "run_123"
        status = RunStatus.COMPLETED
        expected_timestamp = "2024_01_01-13:00:00"
        
        with patch("lib.utils.get_current_timestamp", return_value=expected_timestamp):
            with patch("db.db.update_run_status") as mock_update:
                # Act
                repo.update_run_status(run_id, status)
                
                # Assert
                # Note: status is passed as RunStatus enum, which will be converted to string by db function
                mock_update.assert_called_once()
                call_args = mock_update.call_args[0]
                assert call_args[0] == run_id
                assert call_args[1] == status  # Enum is passed directly
                assert call_args[2] == expected_timestamp
    
    def test_updates_status_to_failed_without_completed_at(self):
        """Test that update_run_status sets completed_at to None for FAILED status."""
        # Arrange
        repo = SQLiteRunRepository()
        run_id = "run_123"
        status = RunStatus.FAILED
        
        with patch("lib.utils.get_current_timestamp", return_value="2024_01_01-13:00:00"):
            with patch("db.db.update_run_status") as mock_update:
                # Act
                repo.update_run_status(run_id, status)
                
                # Assert
                mock_update.assert_called_once_with(run_id, status, None)
    
    def test_updates_status_to_running_without_completed_at(self):
        """Test that update_run_status sets completed_at to None for RUNNING status."""
        # Arrange
        repo = SQLiteRunRepository()
        run_id = "run_123"
        status = RunStatus.RUNNING
        
        with patch("lib.utils.get_current_timestamp", return_value="2024_01_01-13:00:00"):
            with patch("db.db.update_run_status") as mock_update:
                # Act
                repo.update_run_status(run_id, status)
                
                # Assert
                mock_update.assert_called_once_with(run_id, status, None)
    
    def test_calls_update_run_status_with_correct_parameters_for_completed(self):
        """Test that update_run_status calls db function with correct parameters for COMPLETED."""
        # Arrange
        repo = SQLiteRunRepository()
        run_id = "run_123"
        status = RunStatus.COMPLETED
        expected_timestamp = "2024_01_01-13:00:00"
        
        with patch("lib.utils.get_current_timestamp", return_value=expected_timestamp):
            with patch("db.db.update_run_status") as mock_update:
                # Act
                repo.update_run_status(run_id, status)
                
                # Assert
                mock_update.assert_called_once()
                call_args = mock_update.call_args[0]
                assert call_args[0] == run_id
                assert call_args[1] == status  # RunStatus enum is passed
                assert call_args[2] == expected_timestamp
    
    def test_calls_update_run_status_with_correct_parameters_for_failed(self):
        """Test that update_run_status calls db function with correct parameters for FAILED."""
        # Arrange
        repo = SQLiteRunRepository()
        run_id = "run_123"
        status = RunStatus.FAILED
        
        with patch("lib.utils.get_current_timestamp", return_value="2024_01_01-13:00:00"):
            with patch("db.db.update_run_status") as mock_update:
                # Act
                repo.update_run_status(run_id, status)
                
                # Assert
                mock_update.assert_called_once()
                call_args = mock_update.call_args[0]
                assert call_args[0] == run_id
                assert call_args[1] == status
                assert call_args[2] is None
    
    def test_uses_current_timestamp_for_completed_status(self):
        """Test that update_run_status uses get_current_timestamp for COMPLETED status."""
        # Arrange
        repo = SQLiteRunRepository()
        run_id = "run_123"
        status = RunStatus.COMPLETED
        timestamp1 = "2024_01_01-13:00:00"
        timestamp2 = "2024_01_01-14:00:00"
        
        with patch("lib.utils.get_current_timestamp", side_effect=[timestamp1, timestamp2]):
            with patch("db.db.update_run_status") as mock_update:
                # Act
                repo.update_run_status(run_id, status)
                
                # Assert
                mock_update.assert_called_once_with(run_id, status, timestamp1)
    
    def test_handles_all_run_status_values(self):
        """Test that update_run_status handles all RunStatus enum values correctly."""
        # Arrange
        repo = SQLiteRunRepository()
        run_id = "run_123"
        
        for status in RunStatus:
            with patch("lib.utils.get_current_timestamp", return_value="2024_01_01-13:00:00"):
                with patch("db.db.update_run_status") as mock_update:
                    # Act
                    repo.update_run_status(run_id, status)
                    
                    # Assert
                    expected_completed_at = "2024_01_01-13:00:00" if status == RunStatus.COMPLETED else None
                    mock_update.assert_called_once_with(run_id, status, expected_completed_at)
                    mock_update.reset_mock()

