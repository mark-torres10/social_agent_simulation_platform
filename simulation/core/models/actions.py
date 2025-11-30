from enum import Enum

from pydantic import BaseModel, ValidationInfo, field_validator


def validate_non_empty_string(v: str, info: ValidationInfo) -> str:
    """Shared validator for non-empty string fields.
    
    Checks None, coerces to str, strips whitespace, and raises ValueError
    if the result is empty. Uses info.field_name for error messages.
    """
    field_name = info.field_name if info else "field"
    if v is None:
        raise ValueError(f"{field_name} must be a non-empty string")
    if not isinstance(v, str):
        v = str(v)
    v = v.strip()
    if not v:
        raise ValueError(f"{field_name} must be a non-empty string")
    return v


class Like(BaseModel):
    like_id: str
    agent_id: str
    post_id: str
    created_at: str

    @field_validator("like_id", "agent_id", "post_id", mode="before")
    @classmethod
    def validate_identifier_fields(cls, v: str, info: ValidationInfo) -> str:
        """Validate that identifier fields are non-empty strings."""
        return validate_non_empty_string(v, info)


class Comment(BaseModel):
    comment_id: str
    agent_id: str
    post_id: str
    created_at: str

    @field_validator("comment_id", "agent_id", "post_id", mode="before")
    @classmethod
    def validate_identifier_fields(cls, v: str, info: ValidationInfo) -> str:
        """Validate that identifier fields are non-empty strings."""
        return validate_non_empty_string(v, info)


class Follow(BaseModel):
    follow_id: str
    agent_id: str
    user_id: str
    created_at: str

    @field_validator("follow_id", "agent_id", "user_id", mode="before")
    @classmethod
    def validate_identifier_fields(cls, v: str, info: ValidationInfo) -> str:
        """Validate that identifier fields are non-empty strings."""
        return validate_non_empty_string(v, info)


class TurnAction(str, Enum):
    """Action types for a simulation turn."""

    LIKE = "like"
    COMMENT = "comment"
    FOLLOW = "follow"
