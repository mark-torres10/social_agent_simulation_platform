from simulation.core.models.feeds import GeneratedFeed
from simulation.core.models.generated.comment import GeneratedComment
from simulation.core.models.generated.follow import GeneratedFollow
from simulation.core.models.generated.like import GeneratedLike
from simulation.core.models.posts import BlueskyFeedPost


class SocialMediaAgent:
    def __init__(self, handle: str):
        self.handle: str = handle
        self.bio: str = ""
        self.generated_bio: str = ""
        self.followers: int = 0
        self.following: int = 0
        self.posts_count: int = 0
        self.posts: list[BlueskyFeedPost] = []
        self.likes: list[GeneratedLike] = []
        self.comments: list[GeneratedComment] = []
        self.follows: list[GeneratedFollow] = []

    def get_feed(self) -> GeneratedFeed:
        from lib.utils import get_current_timestamp

        return GeneratedFeed(
            feed_id=GeneratedFeed.generate_feed_id(),
            run_id="",
            turn_number=0,
            agent_handle=self.handle,
            post_uris=[],
            created_at=get_current_timestamp(),
        )

    def like_posts(self, feed: list[BlueskyFeedPost]) -> list[GeneratedLike]:
        return []

    def comment_posts(self, feed: list[BlueskyFeedPost]) -> list[GeneratedComment]:
        return []

    def follow_users(self, feed: list[BlueskyFeedPost]) -> list[GeneratedFollow]:
        return []
