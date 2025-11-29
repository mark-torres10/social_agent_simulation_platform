"""Abstraction for repositories."""

from abc import ABC, abstractmethod
from typing import Optional
from db.models import RunConfig, Run, RunStatus
from lib.utils import get_current_timestamp


class RunRepository(ABC):
    """Abstract base class defining the interface for run repositories."""
    
    @abstractmethod
    def create_run(self, run_id: str, config: RunConfig) -> Run:
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
    def update_run_status(self, run_id: str, status: str) -> None:
        """Update a run's status."""
        raise NotImplementedError

class SQLiteRunRepository(RunRepository):
    """SQLite implementation of RunRepository.
    
    Uses functions from db.db module to interact with SQLite database.
    """
    
    def create_run(self, run_id: str, config: RunConfig) -> Run:
        """Create a new run in SQLite."""
        from db.db import write_run
        from lib.utils import get_current_timestamp
        
        run = Run(
            run_id=run_id,
            created_at=get_current_timestamp(),
            total_turns=config.num_turns,
            total_agents=config.num_agents,
            started_at=get_current_timestamp(),
            status=RunStatus.RUNNING,
        )
        write_run(run)
        return run
    
    def get_run(self, run_id: str) -> Optional[Run]:
        """Get a run from SQLite."""
        from db.db import read_run
        return read_run(run_id)
    
    def list_runs(self) -> list[Run]:
        """List all runs from SQLite."""
        from db.db import read_all_runs
        return read_all_runs()
    
    def update_run_status(self, run_id: str, status: str) -> None:
        """Update run status in SQLite."""
        from db.db import update_run_status
        update_run_status(run_id, status)
