"""Abstraction for repositories."""

from abc import ABC, abstractmethod
from typing import Optional
import uuid

from db.models import RunConfig, Run, RunStatus
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
    
    Uses functions from db.db module to interact with SQLite database.
    """
    
    # Valid state transitions for run status
    VALID_TRANSITIONS = {
        RunStatus.RUNNING: {RunStatus.COMPLETED, RunStatus.FAILED},
        RunStatus.COMPLETED: set(),  # Terminal state
        RunStatus.FAILED: set(),     # Terminal state
    }
    
    def create_run(self, config: RunConfig) -> Run:
        """Create a new run in SQLite.
        
        Args:
            config: Configuration for the run
            
        Returns:
            The created Run object
            
        Raises:
            RunCreationError: If the run cannot be created due to a database error
        """
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
            raise RunCreationError(run_id, str(e)) from e
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
            from db.db import update_run_status
            from lib.utils import get_current_timestamp
            ts = get_current_timestamp()
            completed_at = ts if status == RunStatus.COMPLETED else None
            update_run_status(run_id, status.value, completed_at)  # Convert enum to string
        except (RunNotFoundError, InvalidTransitionError):
            # Re-raise domain exceptions as-is
            raise
        except Exception as e:
            raise RunStatusUpdateError(run_id, str(e)) from e
