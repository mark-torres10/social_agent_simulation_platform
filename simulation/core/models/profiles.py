from pydantic import BaseModel, field_validator


class Profile(BaseModel):
    """Base profile model - platform agnostic.

    This represents a social media profile that can be used to create agents.
    Platform-specific implementations can extend this with additional fields.
    """

    handle: str
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


class BlueskyProfile(Profile):
    """Bluesky-specific profile with additional platform fields."""

    did: str  # Bluesky-specific decentralized identifier

    @field_validator("did")
    @classmethod
    def validate_did(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("did cannot be empty")
        return v
