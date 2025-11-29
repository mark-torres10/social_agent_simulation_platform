"""SQLite implementation of run database adapter."""

from typing import Optional

from db.adapters.base import RunDatabaseAdapter
from db.models import Run
from db.exceptions import RunNotFoundError


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
    
    def update_run_status(self, run_id: str, status: str, completed_at: Optional[str] = None) -> None:
        """Update run status in SQLite.
        
        Raises:
            RunNotFoundError: If no run exists with the given run_id
            sqlite3.OperationalError: If database operation fails
            sqlite3.IntegrityError: If status value violates CHECK constraints
        """
        from db.db import update_run_status
        update_run_status(run_id, status, completed_at)

