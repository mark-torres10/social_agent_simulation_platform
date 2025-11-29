"""Abstraction for repositories."""

from abc import ABC, abstractmethod
from typing import Optional, Callable
import uuid

from db.models import RunConfig, Run, RunStatus
from db.adapters import RunDatabaseAdapter
from db.exceptions import (
    RunNotFoundError,
    InvalidTransitionError,
    RunCreationError,
    RunStatusUpdateError,
)

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
        """Update a run's status.
        
        Raises:
            RunNotFoundError: If the run with the given ID does not exist
            InvalidTransitionError: If the status transition is invalid
            RunStatusUpdateError: If the status update fails due to a database error
        """
        raise NotImplementedError

class SQLiteRunRepository(RunRepository):
    """SQLite implementation of RunRepository.
    
    Uses dependency injection to accept a database adapter and timestamp function,
    decoupling it from concrete implementations.
    """
    
    # Valid state transitions for run status
    VALID_TRANSITIONS = {
        RunStatus.RUNNING: {RunStatus.COMPLETED, RunStatus.FAILED},
        RunStatus.COMPLETED: set(),  # Terminal state
        RunStatus.FAILED: set(),     # Terminal state
    }
    
    def __init__(
        self,
        db_adapter: RunDatabaseAdapter,
        get_timestamp: Callable[[], str]
    ):
        """Initialize repository with injected dependencies.
        
        Args:
            db_adapter: Database adapter for run operations
            get_timestamp: Function that returns current timestamp as string
        """
        self._db_adapter = db_adapter
        self._get_timestamp = get_timestamp
    
    def create_run(self, config: RunConfig) -> Run:
        """Create a new run in SQLite.
        
        Args:
            config: Configuration for the run
            
        Returns:
            The created Run object
            
        Raises:
            RunCreationError: If the run cannot be created due to a database error
        """
        ts = self._get_timestamp()
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
            self._db_adapter.write_run(run)
        except Exception as e:
            raise RunCreationError(run_id, str(e)) from e
        return run

    def get_run(self, run_id: str) -> Optional[Run]:
        """Get a run from SQLite."""
        return self._db_adapter.read_run(run_id)
    
    def list_runs(self) -> list[Run]:
        """List all runs from SQLite."""
        return self._db_adapter.read_all_runs()
    
    def update_run_status(self, run_id: str, status: RunStatus) -> None:
        """Update run status in SQLite.
        
        Args:
            run_id: Unique identifier for the run to update
            status: New RunStatus enum value
            
        Raises:
            RunNotFoundError: If the run with the given ID does not exist
            InvalidTransitionError: If the status transition is invalid
            RunStatusUpdateError: If the status update fails due to a database error
        """
        # Get current run to validate state transition
        current_run = self.get_run(run_id)
        if current_run is None:
            raise RunNotFoundError(run_id)
        
        current_status = current_run.status
        
        # Validate state transition
        if status != current_status:
            valid_next_states = self.VALID_TRANSITIONS.get(current_status, set())
            if status not in valid_next_states:
                valid_transitions_list = (
                    [s.value for s in valid_next_states] if valid_next_states else None
                )
                raise InvalidTransitionError(
                    run_id=run_id,
                    current_status=current_status.value,
                    target_status=status.value,
                    valid_transitions=valid_transitions_list,
                )
        
        try:
            ts = self._get_timestamp()
            completed_at = ts if status == RunStatus.COMPLETED else None
            self._db_adapter.update_run_status(run_id, status.value, completed_at)
        except (RunNotFoundError, InvalidTransitionError):
            # Re-raise domain exceptions as-is
            raise
        except Exception as e:
            raise RunStatusUpdateError(run_id, str(e)) from e


def create_sqlite_repository() -> SQLiteRunRepository:
    """Factory function to create a SQLiteRunRepository with default dependencies.
    
    Returns:
        SQLiteRunRepository configured with SQLite adapter and default timestamp function
    """
    from db.adapters import SQLiteRunAdapter
    from lib.utils import get_current_timestamp
    return SQLiteRunRepository(
        db_adapter=SQLiteRunAdapter(),
        get_timestamp=get_current_timestamp
    )
