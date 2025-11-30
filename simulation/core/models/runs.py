from enum import Enum

from pydantic import BaseModel, field_validator


class RunConfig(BaseModel):
    """Configuration for a simulation run."""

    num_agents: int
    num_turns: int

    @field_validator("num_agents")
    @classmethod
    def validate_num_agents(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("num_agents must be greater than 0")
        return v

    @field_validator("num_turns")
    @classmethod
    def validate_num_turns(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("num_turns must be greater than 0")
        return v


class RunStatus(str, Enum):
    """
    Enum representing the state of a simulation run.

    State transitions:
      - RUNNING: The run is actively in progress. All runs start in this state.
      - COMPLETED: The run has finished successfully. Set when the simulation
        completes all turns and agents have completed their actions.
      - FAILED: The run has terminated abnormally due to an error or interruption.
        No further progress will be made.

    Valid transitions:
      - RUNNING -> COMPLETED: Normal successful completion.
      - RUNNING -> FAILED: Error or failure during simulation.
    """

    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class Run(BaseModel):
    run_id: str
    created_at: str
    total_turns: int
    total_agents: int
    started_at: str
    status: RunStatus
    completed_at: str | None = None
