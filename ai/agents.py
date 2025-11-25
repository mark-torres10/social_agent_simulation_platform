from db.models import Feed, Like, Comment, Follow

class SocialMediaAgent:
    def __init__(self, name: str):
        self.name = name
        self.bio = ""
        self.followers = 0
        self.following = 0
        self.posts = []
        self.likes = 0
        self.comments = 0
        self.follows = 0

    def get_feed(self) -> Feed:
        pass


    def like_posts(self) -> list[Like]:
        pass


    def comment_posts(self) -> list[Comment]:
        pass

    
    def follow_users(self) -> list[Follow]:
        pass


def load_agents():
    pass


def record_agent_actions(actions: dict):
    """Record and persist the agent actions into a database."""
    pass
