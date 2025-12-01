"""Tests for db.adapters.sqlite.run_adapter module."""

import json
import sqlite3
from contextlib import contextmanager
from unittest.mock import MagicMock, Mock, patch

import pytest

from db.adapters.sqlite.run_adapter import SQLiteRunAdapter
from simulation.core.models.actions import TurnAction
from simulation.core.models.turns import TurnMetadata


@pytest.fixture
def adapter():
    """Create a SQLiteRunAdapter instance."""
    return SQLiteRunAdapter()


@pytest.fixture
def default_test_data():
    """Common test data used across multiple tests."""
    return {"run_id": "run_123", "turn_number": 0}


def create_mock_row(row_data: dict) -> MagicMock:
    """Helper function to create a mock sqlite3.Row.

    Args:
        row_data: Dictionary mapping column names to values

    Returns:
        MagicMock configured to behave like a sqlite3.Row
    """
    mock_row = MagicMock()
    mock_row.__getitem__ = Mock(side_effect=lambda key: row_data[key])
    mock_row.keys = Mock(return_value=list(row_data.keys()))
    return mock_row


@pytest.fixture
def mock_db_connection():
    """Fixture that provides a context manager for mocking database connections.

    Usage:
        with mock_db_connection() as (mock_get_conn, mock_conn, mock_cursor):
            mock_cursor.fetchone.return_value = some_row
            # test code here
    """

    @contextmanager
    def _mock_db_connection():
        # Import here to ensure module is loaded
        from db import db

        with patch.object(db, "get_connection") as mock_get_conn:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_conn.__enter__ = Mock(return_value=mock_conn)
            mock_conn.__exit__ = Mock(return_value=None)
            mock_conn.execute.return_value = mock_cursor
            mock_get_conn.return_value = mock_conn
            yield mock_get_conn, mock_conn, mock_cursor

    return _mock_db_connection


class TestSQLiteRunAdapterReadTurnMetadata:
    """Tests for SQLiteRunAdapter.read_turn_metadata method."""

    def test_returns_turn_metadata_when_found(
        self, adapter, default_test_data, mock_db_connection
    ):
        """Test that read_turn_metadata returns TurnMetadata when row exists."""
        # Arrange
        run_id = default_test_data["run_id"]
        turn_number = default_test_data["turn_number"]
        # JSON stores enum values as strings
        total_actions_json = json.dumps({"like": 5, "comment": 2, "follow": 1})

        row_data = {
            "run_id": run_id,
            "turn_number": turn_number,
            "total_actions": total_actions_json,
            "created_at": "2024_01_01-12:00:00",
        }
        mock_row = create_mock_row(row_data)

        with mock_db_connection() as (mock_get_conn, mock_conn, mock_cursor):
            mock_cursor.fetchone.return_value = mock_row

            # Act
            result = adapter.read_turn_metadata(run_id, turn_number)

            # Assert
            assert result is not None
            assert isinstance(result, TurnMetadata)
            assert result.run_id == run_id
            assert result.turn_number == turn_number
            assert result.created_at == "2024_01_01-12:00:00"
            # Adapter explicitly converts string keys to TurnAction enum keys
            assert result.total_actions[TurnAction.LIKE] == 5
            assert result.total_actions[TurnAction.COMMENT] == 2
            assert result.total_actions[TurnAction.FOLLOW] == 1

    def test_returns_none_when_not_found(
        self, adapter, default_test_data, mock_db_connection
    ):
        """Test that read_turn_metadata returns None when row doesn't exist."""
        # Arrange
        run_id = default_test_data["run_id"]
        turn_number = default_test_data["turn_number"]

        with mock_db_connection() as (mock_get_conn, mock_conn, mock_cursor):
            mock_cursor.fetchone.return_value = None

            # Act
            result = adapter.read_turn_metadata(run_id, turn_number)

            # Assert
            assert result is None

    def test_raises_operational_error_on_database_error(
        self, adapter, default_test_data, mock_db_connection
    ):
        """Test that read_turn_metadata raises OperationalError on database errors."""
        # Arrange
        run_id = default_test_data["run_id"]
        turn_number = default_test_data["turn_number"]
        db_error = sqlite3.OperationalError("Database locked")

        with mock_db_connection() as (mock_get_conn, mock_conn, mock_cursor):
            mock_conn.execute.side_effect = db_error

            # Act & Assert
            with pytest.raises(sqlite3.OperationalError):
                adapter.read_turn_metadata(run_id, turn_number)

    def test_raises_keyerror_when_missing_required_column(
        self, adapter, default_test_data, mock_db_connection
    ):
        """Test that read_turn_metadata raises KeyError when required column is missing."""
        # Arrange
        run_id = default_test_data["run_id"]
        turn_number = default_test_data["turn_number"]

        # Create a mock row missing the 'total_actions' column
        row_data = {
            "run_id": run_id,
            "turn_number": turn_number,
            # Missing "total_actions"
            "created_at": "2024_01_01-12:00:00",
        }
        mock_row = create_mock_row(row_data)

        with mock_db_connection() as (mock_get_conn, mock_conn, mock_cursor):
            mock_cursor.fetchone.return_value = mock_row

            # Act & Assert
            with pytest.raises(
                KeyError, match="Missing required column 'total_actions'"
            ):
                adapter.read_turn_metadata(run_id, turn_number)

    def test_raises_keyerror_when_missing_created_at_column(
        self, adapter, default_test_data, mock_db_connection
    ):
        """Test that read_turn_metadata raises KeyError when created_at column is missing."""
        # Arrange
        run_id = default_test_data["run_id"]
        turn_number = default_test_data["turn_number"]

        # Create a mock row missing the 'created_at' column
        row_data = {
            "run_id": run_id,
            "turn_number": turn_number,
            "total_actions": '{"like": 5}',
            # Missing "created_at"
        }
        mock_row = create_mock_row(row_data)

        with mock_db_connection() as (mock_get_conn, mock_conn, mock_cursor):
            mock_cursor.fetchone.return_value = mock_row

            # Act & Assert
            with pytest.raises(KeyError, match="Missing required column 'created_at'"):
                adapter.read_turn_metadata(run_id, turn_number)

    def test_raises_valueerror_when_null_fields(
        self, adapter, default_test_data, mock_db_connection
    ):
        """Test that read_turn_metadata raises ValueError when fields are NULL."""
        # Arrange
        run_id = default_test_data["run_id"]
        turn_number = default_test_data["turn_number"]

        # Create a mock row with NULL turn_number
        row_data = {
            "run_id": run_id,
            "turn_number": None,  # NULL
            "total_actions": '{"like": 5}',
            "created_at": "2024_01_01-12:00:00",
        }
        mock_row = create_mock_row(row_data)

        with mock_db_connection() as (mock_get_conn, mock_conn, mock_cursor):
            mock_cursor.fetchone.return_value = mock_row

            # Act & Assert
            with pytest.raises(ValueError, match="Turn metadata has NULL fields"):
                adapter.read_turn_metadata(run_id, turn_number)

    def test_raises_valueerror_when_null_created_at(
        self, adapter, default_test_data, mock_db_connection
    ):
        """Test that read_turn_metadata raises ValueError when created_at is NULL."""
        # Arrange
        run_id = default_test_data["run_id"]
        turn_number = default_test_data["turn_number"]

        # Create a mock row with NULL created_at
        row_data = {
            "run_id": run_id,
            "turn_number": turn_number,
            "total_actions": '{"like": 5}',
            "created_at": None,  # NULL
        }
        mock_row = create_mock_row(row_data)

        with mock_db_connection() as (mock_get_conn, mock_conn, mock_cursor):
            mock_cursor.fetchone.return_value = mock_row

            # Act & Assert
            with pytest.raises(ValueError, match="Turn metadata has NULL fields"):
                adapter.read_turn_metadata(run_id, turn_number)

    def test_raises_valueerror_when_invalid_json(
        self, adapter, default_test_data, mock_db_connection
    ):
        """Test that read_turn_metadata raises ValueError when total_actions is invalid JSON."""
        # Arrange
        run_id = default_test_data["run_id"]
        turn_number = default_test_data["turn_number"]

        # Create a mock row with invalid JSON
        row_data = {
            "run_id": run_id,
            "turn_number": turn_number,
            "total_actions": "not valid json{",
            "created_at": "2024_01_01-12:00:00",
        }
        mock_row = create_mock_row(row_data)

        with mock_db_connection() as (mock_get_conn, mock_conn, mock_cursor):
            mock_cursor.fetchone.return_value = mock_row

            # Act & Assert
            with pytest.raises(
                ValueError, match="Could not parse total_actions as JSON"
            ):
                adapter.read_turn_metadata(run_id, turn_number)

    def test_raises_valueerror_when_invalid_turn_metadata_data(
        self, adapter, mock_db_connection
    ):
        """Test that read_turn_metadata raises ValueError when TurnMetadata validation fails."""
        # Arrange
        run_id = "run_123"
        turn_number = -1  # Invalid turn_number (negative)

        # Create a mock row with invalid turn_number
        row_data = {
            "run_id": run_id,
            "turn_number": turn_number,  # Invalid: negative
            "total_actions": '{"like": 5}',
            "created_at": "2024_01_01-12:00:00",
        }
        mock_row = create_mock_row(row_data)

        with mock_db_connection() as (mock_get_conn, mock_conn, mock_cursor):
            mock_cursor.fetchone.return_value = mock_row

            # Act & Assert
            with pytest.raises(ValueError, match="Invalid turn metadata data"):
                adapter.read_turn_metadata(run_id, turn_number)

    def test_raises_valueerror_when_invalid_action_type(
        self, adapter, default_test_data, mock_db_connection
    ):
        """Test that read_turn_metadata raises ValueError when action type is invalid."""
        # Arrange
        run_id = default_test_data["run_id"]
        turn_number = default_test_data["turn_number"]

        # Create a mock row with invalid action type
        row_data = {
            "run_id": run_id,
            "turn_number": turn_number,
            "total_actions": '{"invalid_action": 5}',
            "created_at": "2024_01_01-12:00:00",
        }
        mock_row = create_mock_row(row_data)

        with mock_db_connection() as (mock_get_conn, mock_conn, mock_cursor):
            mock_cursor.fetchone.return_value = mock_row

            # Act & Assert
            with pytest.raises(
                ValueError, match="Invalid action type in total_actions"
            ):
                adapter.read_turn_metadata(run_id, turn_number)

    def test_calls_database_with_correct_parameters(self, adapter, mock_db_connection):
        """Test that read_turn_metadata calls database with correct parameters."""
        # Arrange
        run_id = "run_123"
        turn_number = 5

        with mock_db_connection() as (mock_get_conn, mock_conn, mock_cursor):
            mock_cursor.fetchone.return_value = None

            # Act
            adapter.read_turn_metadata(run_id, turn_number)

            # Assert
            mock_conn.execute.assert_called_once()
            call_args = mock_conn.execute.call_args
            assert (
                "SELECT * FROM turn_metadata WHERE run_id = ? AND turn_number = ?"
                in str(call_args[0][0])
            )
            assert call_args[0][1] == (run_id, turn_number)
