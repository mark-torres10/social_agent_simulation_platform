"""SQLite implementation of run database adapter."""

import json
import sqlite3
from typing import Optional

from db.adapters.base import RunDatabaseAdapter
from db.exceptions import DuplicateTurnMetadataError
from simulation.core.models.actions import TurnAction
from simulation.core.models.runs import Run
from simulation.core.models.turns import TurnMetadata


class SQLiteRunAdapter(RunDatabaseAdapter):
    """SQLite implementation of RunDatabaseAdapter.

    Uses functions from db.db module to interact with SQLite database.

    This implementation raises SQLite-specific exceptions. See method docstrings
    for details on specific exception types.
    """

    def write_run(self, run: Run) -> None:
        """Write a run to SQLite.

        Raises:
            sqlite3.IntegrityError: If run_id violates constraints
            sqlite3.OperationalError: If database operation fails
        """
        from db.db import write_run

        write_run(run)

    def read_run(self, run_id: str) -> Optional[Run]:
        """Read a run from SQLite.

        Raises:
            ValueError: If the run data is invalid (NULL fields, invalid status)
            sqlite3.OperationalError: If database operation fails
            KeyError: If required columns are missing from the database row
        """
        from db.db import read_run

        return read_run(run_id)

    def read_all_runs(self) -> list[Run]:
        """Read all runs from SQLite.

        Raises:
            ValueError: If any run data is invalid (NULL fields, invalid status)
            sqlite3.OperationalError: If database operation fails
            KeyError: If required columns are missing from any database row
        """
        from db.db import read_all_runs

        return read_all_runs()

    def update_run_status(
        self, run_id: str, status: str, completed_at: Optional[str] = None
    ) -> None:
        """Update run status in SQLite.

        Raises:
            RunNotFoundError: If no run exists with the given run_id
            sqlite3.OperationalError: If database operation fails
            sqlite3.IntegrityError: If status value violates CHECK constraints
        """
        from db.db import update_run_status

        update_run_status(run_id, status, completed_at)

    def read_turn_metadata(
        self, run_id: str, turn_number: int
    ) -> Optional[TurnMetadata]:
        """Read turn metadata from SQLite.

        The total_actions field is stored as JSON with string keys (e.g., {"like": 5}).
        This method converts those string keys to TurnAction enum keys.

        Args:
            run_id: The ID of the run
            turn_number: The turn number (0-indexed)

        Returns:
            TurnMetadata if found, None otherwise

        Raises:
            ValueError: If the turn metadata data is invalid (NULL fields, invalid action types)
            sqlite3.OperationalError: If database operation fails
            KeyError: If required columns are missing from the database row
        """
        from db.db import get_connection

        with get_connection() as conn:
            try:
                row = conn.execute(
                    "SELECT * FROM turn_metadata WHERE run_id = ? AND turn_number = ?",
                    (run_id, turn_number),
                ).fetchone()
            except sqlite3.OperationalError:
                raise

            if row is None:
                return None

            # Check required columns
            required_cols = ["run_id", "turn_number", "total_actions", "created_at"]
            for col in required_cols:
                if col not in row.keys():
                    raise KeyError(
                        f"Missing required column '{col}' in turn_metadata row"
                    )

            # Check for NULL fields
            for col in required_cols:
                if row[col] is None:
                    raise ValueError(f"Turn metadata has NULL fields: {col}={row[col]}")

            try:
                total_actions_dict = json.loads(row["total_actions"])
            except json.JSONDecodeError as e:
                raise ValueError(
                    f"Could not parse total_actions as JSON for turn_metadata: {e}"
                )

            # Convert string keys to TurnAction enum keys
            try:
                total_actions = {
                    TurnAction(k): v for k, v in total_actions_dict.items()
                }
            except (ValueError, KeyError) as e:
                valid_keys = [action.value for action in TurnAction]
                raise ValueError(
                    f"Invalid action type in total_actions for turn_metadata: {e}. "
                    f"Expected keys: {valid_keys}, got: {list(total_actions_dict.keys())}"
                )

            try:
                return TurnMetadata(
                    run_id=row["run_id"],
                    turn_number=row["turn_number"],
                    total_actions=total_actions,
                    created_at=row["created_at"],
                )
            except Exception as e:
                raise ValueError(
                    f"Invalid turn metadata data: {e}. "
                    f"run_id={row['run_id']}, turn_number={row['turn_number']}, total_actions={total_actions}, created_at={row['created_at']}"
                )

    def write_turn_metadata(self, turn_metadata: TurnMetadata) -> None:
        """Write turn metadata to SQLite.

        Writes to the `turn_metadata` table. Uses INSERT.

        Args:
            turn_metadata: TurnMetadata model to write

        Raises:
            sqlite3.IntegrityError: If turn_number violates constraints
            sqlite3.OperationalError: If database operation fails
            DuplicateTurnMetadataError: If turn metadata already exists
        """
        from db.db import get_connection

        existing_turn_metadata = self.read_turn_metadata(
            turn_metadata.run_id, turn_metadata.turn_number
        )

        if existing_turn_metadata is not None:
            raise DuplicateTurnMetadataError(
                turn_metadata.run_id, turn_metadata.turn_number
            )

        with get_connection() as conn:
            total_actions_json = json.dumps(
                {k.value: v for k, v in turn_metadata.total_actions.items()}
            )
            conn.execute(
                "INSERT INTO turn_metadata (run_id, turn_number, total_actions, created_at) VALUES (?, ?, ?, ?)",
                (
                    turn_metadata.run_id,
                    turn_metadata.turn_number,
                    total_actions_json,
                    turn_metadata.created_at,
                ),
            )
            conn.commit()
