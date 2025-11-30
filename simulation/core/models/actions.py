from enum import Enum

from pydantic import BaseModel, field_validator


class Like(BaseModel):
    like_id: str
    agent_id: str
    post_id: str
    created_at: str

    @field_validator("like_id", mode="before")
    @classmethod
    def validate_like_id(cls, v: str) -> str:
        """Validate that like_id is a non-empty string."""
        if v is None:
            raise ValueError("like_id must be a non-empty string")
        if not isinstance(v, str):
            v = str(v)
        v = v.strip()
        if not v:
            raise ValueError("like_id must be a non-empty string")
        return v

    @field_validator("agent_id", mode="before")
    @classmethod
    def validate_agent_id(cls, v: str) -> str:
        """Validate that agent_id is a non-empty string."""
        if v is None:
            raise ValueError("agent_id must be a non-empty string")
        if not isinstance(v, str):
            v = str(v)
        v = v.strip()
        if not v:
            raise ValueError("agent_id must be a non-empty string")
        return v

    @field_validator("post_id", mode="before")
    @classmethod
    def validate_post_id(cls, v: str) -> str:
        """Validate that post_id is a non-empty string."""
        if v is None:
            raise ValueError("post_id must be a non-empty string")
        if not isinstance(v, str):
            v = str(v)
        v = v.strip()
        if not v:
            raise ValueError("post_id must be a non-empty string")
        return v


class Comment(BaseModel):
    comment_id: str
    agent_id: str
    post_id: str
    created_at: str

    @field_validator("comment_id", mode="before")
    @classmethod
    def validate_comment_id(cls, v: str) -> str:
        """Validate that comment_id is a non-empty string."""
        if v is None:
            raise ValueError("comment_id must be a non-empty string")
        if not isinstance(v, str):
            v = str(v)
        v = v.strip()
        if not v:
            raise ValueError("comment_id must be a non-empty string")
        return v

    @field_validator("agent_id", mode="before")
    @classmethod
    def validate_agent_id(cls, v: str) -> str:
        """Validate that agent_id is a non-empty string."""
        if v is None:
            raise ValueError("agent_id must be a non-empty string")
        if not isinstance(v, str):
            v = str(v)
        v = v.strip()
        if not v:
            raise ValueError("agent_id must be a non-empty string")
        return v

    @field_validator("post_id", mode="before")
    @classmethod
    def validate_post_id(cls, v: str) -> str:
        """Validate that post_id is a non-empty string."""
        if v is None:
            raise ValueError("post_id must be a non-empty string")
        if not isinstance(v, str):
            v = str(v)
        v = v.strip()
        if not v:
            raise ValueError("post_id must be a non-empty string")
        return v


class Follow(BaseModel):
    follow_id: str
    agent_id: str
    user_id: str
    created_at: str

    @field_validator("follow_id", mode="before")
    @classmethod
    def validate_follow_id(cls, v: str) -> str:
        """Validate that follow_id is a non-empty string."""
        if v is None:
            raise ValueError("follow_id must be a non-empty string")
        if not isinstance(v, str):
            v = str(v)
        v = v.strip()
        if not v:
            raise ValueError("follow_id must be a non-empty string")
        return v

    @field_validator("agent_id", mode="before")
    @classmethod
    def validate_agent_id(cls, v: str) -> str:
        """Validate that agent_id is a non-empty string."""
        if v is None:
            raise ValueError("agent_id must be a non-empty string")
        if not isinstance(v, str):
            v = str(v)
        v = v.strip()
        if not v:
            raise ValueError("agent_id must be a non-empty string")
        return v

    @field_validator("user_id", mode="before")
    @classmethod
    def validate_user_id(cls, v: str) -> str:
        """Validate that user_id is a non-empty string."""
        if v is None:
            raise ValueError("user_id must be a non-empty string")
        if not isinstance(v, str):
            v = str(v)
        v = v.strip()
        if not v:
            raise ValueError("user_id must be a non-empty string")
        return v


class TurnAction(str, Enum):
    """Action types for a simulation turn."""

    LIKE = "like"
    COMMENT = "comment"
    FOLLOW = "follow"
