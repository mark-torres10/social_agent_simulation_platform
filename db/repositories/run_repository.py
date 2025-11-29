"""Abstraction for repositories."""

from abc import ABC, abstractmethod
from typing import Optional
import uuid

from db.models import RunConfig, Run, RunStatus
from lib.utils import get_current_timestamp

class RunRepository(ABC):
    """Abstract base class defining the interface for run repositories."""
    
    @abstractmethod
    def create_run(self, config: RunConfig) -> Run:
        """Create a new run."""
        raise NotImplementedError
    
    @abstractmethod
    def get_run(self, run_id: str) -> Optional[Run]:
        """Get a run by ID."""
        raise NotImplementedError
    
    @abstractmethod
    def list_runs(self) -> list[Run]:
        """List all runs."""
        raise NotImplementedError
    
    @abstractmethod
    def update_run_status(self, run_id: str, status: RunStatus) -> None:
        """Update a run's status."""
        raise NotImplementedError

class SQLiteRunRepository(RunRepository):
    """SQLite implementation of RunRepository.
    
    Uses functions from db.db module to interact with SQLite database.
    """
    
    def create_run(self, config: RunConfig) -> Run:
        """Create a new run in SQLite."""
        from db.db import write_run
        from lib.utils import get_current_timestamp
        
        ts = get_current_timestamp()
        run_id = f"run_{ts}_{uuid.uuid4()}"

        run = Run(
            run_id=run_id,
            created_at=ts,
            total_turns=config.num_turns,
            total_agents=config.num_agents,
            started_at=ts,
            status=RunStatus.RUNNING,
        )
        try:
            write_run(run)
        except Exception as e:
            raise RuntimeError(f"Failed to create run {run_id}: {e}") from e
        return run

    def get_run(self, run_id: str) -> Optional[Run]:
        """Get a run from SQLite."""
        from db.db import read_run
        return read_run(run_id)
    
    def list_runs(self) -> list[Run]:
        """List all runs from SQLite."""
        from db.db import read_all_runs
        return read_all_runs()
    
    def update_run_status(self, run_id: str, status: RunStatus) -> None:
        """Update run status in SQLite.
        
        Args:
            run_id: Unique identifier for the run to update
            status: New RunStatus enum value
            
        Raises:
            RuntimeError: If the update fails or run doesn't exist
        """
        try:
            from db.db import update_run_status
            ts = get_current_timestamp()
            completed_at = ts if status == RunStatus.COMPLETED else None
            update_run_status(run_id, status.value, completed_at)  # Convert enum to string
        except Exception as e:
            raise RuntimeError(f"Failed to update run status {run_id}: {e}") from e
