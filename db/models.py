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


class FeedItem(BaseModel):
    feed_item_id: str
    text: str
    created_at: str


class Feed(BaseModel):
    feed_id: str
    agent_id: str
    created_at: str
    items: list[FeedItem]


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


class GeneratedFeed(BaseModel):
    """A feed generated for an AI agent."""
    pass
