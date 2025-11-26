from db.models import BlueskyFeedPost, Like, Comment, Follow, GeneratedFeed

class SocialMediaAgent:
    def __init__(self, handle: str):
        """
        Initialize a SocialMediaAgent with a handle and default empty profile and activity state.
        
        Parameters:
            handle (str): Unique identifier for the agent (the agent's social handle).
        
        Attributes:
            handle (str): The agent's handle.
            bio (str): Visible biography text.
            generated_bio (str): AI-generated biography text.
            followers (int): Number of followers the agent has.
            following (int): Number of accounts the agent follows.
            posts_count (int): Number of posts created by the agent.
            posts (list[BlueskyFeedPost]): Agent-created posts.
            likes (list[Like]): Likes made by the agent.
            comments (list[Comment]): Comments made by the agent.
            follows (list[Follow]): Follow actions performed by the agent.
        """
        self.handle: str = handle
        self.bio: str = ""
        self.generated_bio: str = ""
        self.followers: int = 0
        self.following: int = 0
        self.posts_count: int = 0
        self.posts: list[BlueskyFeedPost] = []
        self.likes: list[Like] = []
        self.comments: list[Comment] = []
        self.follows: list[Follow] = []

    def get_feed(self) -> GeneratedFeed:
        return []


    def like_posts(self, feed: GeneratedFeed) -> list[Like]:
        return []


    def comment_posts(self, feed: GeneratedFeed) -> list[Comment]:
        return []

    
    def follow_users(self, feed: GeneratedFeed) -> list[Follow]:
        return []


def record_agent_actions(actions: dict):
    """Record and persist the agent actions into a database."""
    pass