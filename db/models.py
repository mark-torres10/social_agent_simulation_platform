import uuid
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

class BlueskyProfile(BaseModel):
    """Relevant information from a Bluesky profile."""
    handle: str
    did: str
    display_name: str
    bio: str
    followers_count: int
    follows_count: int
    posts_count: int


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
    agent_handle: str
    created_at: str
    items: list[BlueskyFeedPost]

    @classmethod
    def generate_feed_id(cls) -> str:
        return f"feed_{str(uuid.uuid4())}"
