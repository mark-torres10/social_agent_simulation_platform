"""Abstraction for repositories."""

from abc import ABC, abstractmethod
from typing import Optional
import uuid

from db.models import RunConfig, Run, RunStatus

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
    
    # Valid state transitions for run status
    VALID_TRANSITIONS = {
        RunStatus.RUNNING: {RunStatus.COMPLETED, RunStatus.FAILED},
        RunStatus.COMPLETED: set(),  # Terminal state
        RunStatus.FAILED: set(),     # Terminal state
    }
    
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
            ValueError: If the status transition is invalid
            RuntimeError: If the update fails or run doesn't exist
        """
        # Get current run to validate state transition
        current_run = self.get_run(run_id)
        if current_run is None:
            raise RuntimeError(f"Run {run_id} not found")
        
        current_status = current_run.status
        
        # Validate state transition
        if status != current_status:
            valid_next_states = self.VALID_TRANSITIONS.get(current_status, set())
            if status not in valid_next_states:
                raise ValueError(
                    f"Invalid status transition for run {run_id}: "
                    f"{current_status.value} -> {status.value}. "
                    f"Valid transitions from {current_status.value} are: "
                    f"{[s.value for s in valid_next_states] if valid_next_states else 'none (terminal state)'}"
                )
        
        try:
            from db.db import update_run_status
            from lib.utils import get_current_timestamp
            ts = get_current_timestamp()
            completed_at = ts if status == RunStatus.COMPLETED else None
            update_run_status(run_id, status.value, completed_at)  # Convert enum to string
        except Exception as e:
            raise RuntimeError(f"Failed to update run status {run_id}: {e}") from e
