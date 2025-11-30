from pydantic import BaseModel, field_validator, model_validator


class Post(BaseModel):
    """Base post model - platform agnostic.

    This represents a social media post. Platform-specific implementations
    can extend this with additional fields.
    """

    id: str  # Generic identifier (could be URI, URL, UUID, etc.)
    author_handle: str
    author_display_name: str
    text: str
    like_count: int
    created_at: str

    @field_validator("id")
    @classmethod
    def validate_id(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("id cannot be empty")
        return v

    @field_validator("author_handle")
    @classmethod
    def validate_author_handle(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("author_handle cannot be empty")
        return v


class BlueskyFeedPost(Post):
    """Bluesky-specific post with additional platform fields."""

    uri: str  # Bluesky-specific URI
    bookmark_count: int
    quote_count: int
    reply_count: int
    repost_count: int

    @field_validator("uri")
    @classmethod
    def validate_uri(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("uri cannot be empty")
        return v

    @model_validator(mode="before")
    @classmethod
    def set_id_from_uri(cls, data: dict) -> dict:
        """Set id from uri if not provided."""
        if isinstance(data, dict) and "uri" in data and "id" not in data:
            data["id"] = data["uri"]
        return data
