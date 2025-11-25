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
