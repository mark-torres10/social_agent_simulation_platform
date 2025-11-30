import uuid
from enum import Enum

from pydantic import BaseModel, field_validator


class Like(BaseModel):
    like_id: str
    agent_id: str
    post_id: str
    created_at: str


class Comment(BaseModel):
    comment_id: str
    agent_id: str
    post_id: str
    created_at: str


class Follow(BaseModel):
    follow_id: str
    agent_id: str
    user_id: str
    created_at: str


class BlueskyProfile(BaseModel):
    """Relevant information from a Bluesky profile."""

    handle: str
    did: str
    display_name: str
    bio: str
    followers_count: int
    follows_count: int
    posts_count: int

    @field_validator("handle")
    @classmethod
    def validate_handle(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("handle cannot be empty")
        return v


class BlueskyFeedPost(BaseModel):
    uri: str
    author_display_name: str
    author_handle: str
    text: str
    bookmark_count: int
    like_count: int
    quote_count: int
    reply_count: int
    repost_count: int
    created_at: str

    @field_validator("uri")
    @classmethod
    def validate_uri(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("uri cannot be empty")
        return v

    @field_validator("author_handle")
    @classmethod
    def validate_author_handle(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("author_handle cannot be empty")
        return v


class GeneratedBio(BaseModel):
    """An AI-generated bio for a Bluesky profile."""

    handle: str
    generated_bio: str
    created_at: str


# TODO: for now, we support only Bluesky posts being added to feeds.
# We'll revisit how to add AI-generated posts to feeds later on.
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

    @classmethod
    def generate_feed_id(cls) -> str:
        return f"feed_{str(uuid.uuid4())}"


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
