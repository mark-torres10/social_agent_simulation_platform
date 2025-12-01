"""Tests for db.adapters.sqlite.run_adapter module."""

import json
import sqlite3
from unittest.mock import MagicMock, Mock, patch

import pytest

from db.adapters.sqlite.run_adapter import SQLiteRunAdapter
from simulation.core.models.actions import TurnAction
from simulation.core.models.turns import TurnMetadata


class TestSQLiteRunAdapterReadTurnMetadata:
    """Tests for SQLiteRunAdapter.read_turn_metadata method."""

    def test_returns_turn_metadata_when_found(self):
        """Test that read_turn_metadata returns TurnMetadata when row exists."""
        # Arrange
        adapter = SQLiteRunAdapter()
        run_id = "run_123"
        turn_number = 0
        # JSON stores enum values as strings
        total_actions_json = json.dumps({"like": 5, "comment": 2, "follow": 1})

        # Create a mock row that mimics sqlite3.Row behavior
        mock_row = MagicMock()
        row_data = {
            "run_id": run_id,
            "turn_number": turn_number,
            "total_actions": total_actions_json,
            "created_at": "2024_01_01-12:00:00",
        }
        mock_row.__getitem__ = Mock(side_effect=lambda key: row_data[key])
        mock_row.keys = Mock(return_value=list(row_data.keys()))

        with patch("db.db.get_connection") as mock_get_conn:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = mock_row
            mock_conn.__enter__ = Mock(return_value=mock_conn)
            mock_conn.__exit__ = Mock(return_value=None)
            mock_conn.execute.return_value = mock_cursor
            mock_get_conn.return_value = mock_conn

            # Act
            result = adapter.read_turn_metadata(run_id, turn_number)

            # Assert
            assert result is not None
            assert isinstance(result, TurnMetadata)
            assert result.turn_number == turn_number
            # Adapter explicitly converts string keys to TurnAction enum keys
            assert result.total_actions[TurnAction.LIKE] == 5
            assert result.total_actions[TurnAction.COMMENT] == 2
            assert result.total_actions[TurnAction.FOLLOW] == 1

    def test_returns_none_when_not_found(self):
        """Test that read_turn_metadata returns None when row doesn't exist."""
        # Arrange
        adapter = SQLiteRunAdapter()
        run_id = "run_123"
        turn_number = 0

        with patch("db.db.get_connection") as mock_get_conn:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = None
            mock_conn.__enter__ = Mock(return_value=mock_conn)
            mock_conn.__exit__ = Mock(return_value=None)
            mock_conn.execute.return_value = mock_cursor
            mock_get_conn.return_value = mock_conn

            # Act
            result = adapter.read_turn_metadata(run_id, turn_number)

            # Assert
            assert result is None

    def test_raises_operational_error_on_database_error(self):
        """Test that read_turn_metadata raises OperationalError on database errors."""
        # Arrange
        adapter = SQLiteRunAdapter()
        run_id = "run_123"
        turn_number = 0
        db_error = sqlite3.OperationalError("Database locked")

        with patch("db.db.get_connection") as mock_get_conn:
            mock_conn = MagicMock()
            mock_conn.__enter__ = Mock(return_value=mock_conn)
            mock_conn.__exit__ = Mock(return_value=None)
            mock_conn.execute.side_effect = db_error
            mock_get_conn.return_value = mock_conn

            # Act & Assert
            with pytest.raises(sqlite3.OperationalError):
                adapter.read_turn_metadata(run_id, turn_number)

    def test_raises_keyerror_when_missing_required_column(self):
        """Test that read_turn_metadata raises KeyError when required column is missing."""
        # Arrange
        adapter = SQLiteRunAdapter()
        run_id = "run_123"
        turn_number = 0

        # Create a mock row missing the 'total_actions' column
        mock_row = MagicMock()
        mock_row.__getitem__ = Mock(
            side_effect=lambda key: {
                "run_id": run_id,
                "turn_number": turn_number,
                # Missing "total_actions"
                "created_at": "2024_01_01-12:00:00",
            }[key]
        )
        mock_row.keys = Mock(return_value=["run_id", "turn_number", "created_at"])

        with patch("db.db.get_connection") as mock_get_conn:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = mock_row
            mock_conn.__enter__ = Mock(return_value=mock_conn)
            mock_conn.__exit__ = Mock(return_value=None)
            mock_conn.execute.return_value = mock_cursor
            mock_get_conn.return_value = mock_conn

            # Act & Assert
            with pytest.raises(
                KeyError, match="Missing required column 'total_actions'"
            ):
                adapter.read_turn_metadata(run_id, turn_number)

    def test_raises_valueerror_when_null_fields(self):
        """Test that read_turn_metadata raises ValueError when fields are NULL."""
        # Arrange
        adapter = SQLiteRunAdapter()
        run_id = "run_123"
        turn_number = 0

        # Create a mock row with NULL turn_number
        mock_row = MagicMock()
        mock_row.__getitem__ = Mock(
            side_effect=lambda key: {
                "run_id": run_id,
                "turn_number": None,  # NULL
                "total_actions": '{"like": 5}',
                "created_at": "2024_01_01-12:00:00",
            }[key]
        )
        mock_row.keys = Mock(
            return_value=["run_id", "turn_number", "total_actions", "created_at"]
        )

        with patch("db.db.get_connection") as mock_get_conn:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = mock_row
            mock_conn.__enter__ = Mock(return_value=mock_conn)
            mock_conn.__exit__ = Mock(return_value=None)
            mock_conn.execute.return_value = mock_cursor
            mock_get_conn.return_value = mock_conn

            # Act & Assert
            with pytest.raises(ValueError, match="Turn metadata has NULL fields"):
                adapter.read_turn_metadata(run_id, turn_number)

    def test_raises_valueerror_when_invalid_json(self):
        """Test that read_turn_metadata raises ValueError when total_actions is invalid JSON."""
        # Arrange
        adapter = SQLiteRunAdapter()
        run_id = "run_123"
        turn_number = 0

        # Create a mock row with invalid JSON
        mock_row = MagicMock()
        mock_row.__getitem__ = Mock(
            side_effect=lambda key: {
                "run_id": run_id,
                "turn_number": turn_number,
                "total_actions": "not valid json{",
                "created_at": "2024_01_01-12:00:00",
            }[key]
        )
        mock_row.keys = Mock(
            return_value=["run_id", "turn_number", "total_actions", "created_at"]
        )

        with patch("db.db.get_connection") as mock_get_conn:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = mock_row
            mock_conn.__enter__ = Mock(return_value=mock_conn)
            mock_conn.__exit__ = Mock(return_value=None)
            mock_conn.execute.return_value = mock_cursor
            mock_get_conn.return_value = mock_conn

            # Act & Assert
            with pytest.raises(
                ValueError, match="Could not parse total_actions as JSON"
            ):
                adapter.read_turn_metadata(run_id, turn_number)

    def test_raises_valueerror_when_invalid_turn_metadata_data(self):
        """Test that read_turn_metadata raises ValueError when TurnMetadata validation fails."""
        # Arrange
        adapter = SQLiteRunAdapter()
        run_id = "run_123"
        turn_number = -1  # Invalid turn_number (negative)

        # Create a mock row with invalid turn_number
        mock_row = MagicMock()
        mock_row.__getitem__ = Mock(
            side_effect=lambda key: {
                "run_id": run_id,
                "turn_number": turn_number,  # Invalid: negative
                "total_actions": '{"like": 5}',
                "created_at": "2024_01_01-12:00:00",
            }[key]
        )
        mock_row.keys = Mock(
            return_value=["run_id", "turn_number", "total_actions", "created_at"]
        )

        with patch("db.db.get_connection") as mock_get_conn:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = mock_row
            mock_conn.__enter__ = Mock(return_value=mock_conn)
            mock_conn.__exit__ = Mock(return_value=None)
            mock_conn.execute.return_value = mock_cursor
            mock_get_conn.return_value = mock_conn

            # Act & Assert
            with pytest.raises(ValueError, match="Invalid turn metadata data"):
                adapter.read_turn_metadata(run_id, turn_number)

    def test_raises_valueerror_when_invalid_action_type(self):
        """Test that read_turn_metadata raises ValueError when action type is invalid."""
        # Arrange
        adapter = SQLiteRunAdapter()
        run_id = "run_123"
        turn_number = 0

        # Create a mock row with invalid action type
        mock_row = MagicMock()
        mock_row.__getitem__ = Mock(
            side_effect=lambda key: {
                "run_id": run_id,
                "turn_number": turn_number,
                "total_actions": '{"invalid_action": 5}',
                "created_at": "2024_01_01-12:00:00",
            }[key]
        )
        mock_row.keys = Mock(
            return_value=["run_id", "turn_number", "total_actions", "created_at"]
        )

        with patch("db.db.get_connection") as mock_get_conn:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = mock_row
            mock_conn.__enter__ = Mock(return_value=mock_conn)
            mock_conn.__exit__ = Mock(return_value=None)
            mock_conn.execute.return_value = mock_cursor
            mock_get_conn.return_value = mock_conn

            # Act & Assert
            with pytest.raises(
                ValueError, match="Invalid action type in total_actions"
            ):
                adapter.read_turn_metadata(run_id, turn_number)

    def test_calls_database_with_correct_parameters(self):
        """Test that read_turn_metadata calls database with correct parameters."""
        # Arrange
        adapter = SQLiteRunAdapter()
        run_id = "run_123"
        turn_number = 5

        with patch("db.db.get_connection") as mock_get_conn:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = None
            mock_conn.__enter__ = Mock(return_value=mock_conn)
            mock_conn.__exit__ = Mock(return_value=None)
            mock_conn.execute.return_value = mock_cursor
            mock_get_conn.return_value = mock_conn

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
