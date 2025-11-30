"""Domain models specific to the simulation engine."""

from enum import Enum

from pydantic import BaseModel, field_validator


class TurnAction(str, Enum):
    """Action types for a simulation turn."""

    LIKE = "like"
    COMMENT = "comment"
    FOLLOW = "follow"


class TurnResult(BaseModel):
    """Result of executing a single simulation turn.

    Contains aggregated statistics about agent actions during the turn.

    Attributes:
        turn_number: The turn number (0-indexed).
        total_actions: Dictionary mapping action types to counts.
        execution_time_ms: Optional execution time in milliseconds.
    """

    turn_number: int
    total_actions: dict[TurnAction, int]
    execution_time_ms: int | None = None

    @field_validator("turn_number")
    @classmethod
    def validate_turn_number(cls, v: int) -> int:
        """Validate that turn_number is non-negative."""
        if v < 0:
            raise ValueError("turn_number must be >= 0")
        return v

    model_config = {"frozen": True}  # Make immutable
