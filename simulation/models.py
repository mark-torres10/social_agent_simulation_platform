from typing import Optional
from pydantic import BaseModel, Field

from feeds.models import FeedObservation


# flesh this out. This should be a class that contains how the user engaged with a post.
class UserEngagement(BaseModel):
    """Container class for a user engagement."""

    metadata: Optional[dict] = Field(
        default=None, description="Metadata about the post."
    )
    observation: FeedObservation = Field(
        default=None, description="Observation about the post."
    )
    engagement: Optional[dict] = Field(
        default=None,
        description="Engagement, e.g., like/post/comment/follow, etc., plus rationale.",
    )
