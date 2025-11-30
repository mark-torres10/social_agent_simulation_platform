# TODO: for now, we support only Bluesky posts being added to feeds.
# We'll revisit how to add AI-generated posts to feeds later on.
import uuid

from pydantic import BaseModel, field_validator


class GeneratedFeed(BaseModel):
    """A feed generated for an AI agent."""

    feed_id: str
    run_id: str
    turn_number: int
    agent_handle: str
    post_uris: list[str]
    created_at: str

    @field_validator("agent_handle")
    @classmethod
    def validate_agent_handle(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("agent_handle cannot be empty")
        return v

    @field_validator("run_id")
    @classmethod
    def validate_run_id(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("run_id cannot be empty")
        return v

    @field_validator("feed_id")
    @classmethod
    def validate_feed_id(cls, v: str) -> str:
        """Validate that feed_id is a non-empty string."""
        if not v or not v.strip():
            raise ValueError("feed_id cannot be empty")
        return v.strip()

    @field_validator("turn_number")
    @classmethod
    def validate_turn_number(cls, v: int) -> int:
        """Validate that turn_number is a non-negative integer."""
        if not isinstance(v, int):
            raise ValueError("turn_number must be an integer")
        if v < 0:
            raise ValueError("turn_number must be >= 0")
        return v

    @classmethod
    def generate_feed_id(cls) -> str:
        return f"feed_{str(uuid.uuid4())}"
