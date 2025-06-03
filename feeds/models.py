from typing import Optional, Iterator

from pydantic import BaseModel, Field

from lib.helper import get_current_timestamp_str


class FeedPost(BaseModel):
    """Container class for a feed post."""

    post_id: str = Field(
        default="", description="Post ID, which is the author + timestamp."
    )
    author: str = Field(default="", description="Author of the post.")
    timestamp: str = Field(
        default=get_current_timestamp_str(), description="Timestamp of the post."
    )
    text: str = Field(default="", description="Text of the post.")
    attachments: Optional[list[str]] = Field(
        default=None,
        description="Description of attachments (e.g., images, links). Instead of including images, just include description of image.",
    )
    liked_by: Optional[list[str]] = Field(
        default=None, description="List of users who liked the post."
    )
    shared_by: Optional[list[str]] = Field(
        default=None, description="List of users who shared the post."
    )
    comments: Optional[list[str]] = Field(
        default=None, description="List of comments on the post."
    )


class Feed(BaseModel):
    """Container class for a feed."""

    posts: list[FeedPost]

    def __len__(self):
        return len(self.posts)

    def __getitem__(self, index: int) -> FeedPost:
        return self.posts[index]

    def __iter__(self) -> Iterator[FeedPost]:
        return iter(self.posts)


class FeedObservation(BaseModel):
    """Observation/thought that a user has about a post in a feed."""

    metadata: Optional[dict] = Field(
        default=None, description="Metadata about the post."
    )
    observation: Optional[str] = Field(
        default=None, description="Observations about the post, if any."
    )
    desired_actions: Optional[dict] = Field(
        default=None,
        description="Desired action(s), e.g., like/post/comment/follow, etc, and the rationale for each.",
    )
