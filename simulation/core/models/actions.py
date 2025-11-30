from enum import Enum

from pydantic import BaseModel


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


class TurnAction(str, Enum):
    """Action types for a simulation turn."""

    LIKE = "like"
    COMMENT = "comment"
    FOLLOW = "follow"
