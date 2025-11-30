from simulation.core.models.actions import Like, Comment, Follow, TurnAction
from simulation.core.models.posts import Post
from simulation.core.models.feeds import GeneratedFeed

class SocialMediaAgent:
    def __init__(self, handle: str):
        self.handle: str = handle
        self.bio: str = ""
        self.generated_bio: str = ""
        self.followers: int = 0
        self.following: int = 0
        self.posts_count: int = 0
        self.posts: list[Post] = []
        self.likes: list[Like] = []
        self.comments: list[Comment] = []
        self.follows: list[Follow] = []

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

    def like_posts(self, feed: list[Post]) -> list[Like]:
        return []

    def comment_posts(self, feed: list[Post]) -> list[Comment]:
        return []

    def follow_users(self, feed: list[Post]) -> list[Follow]:
        return []
