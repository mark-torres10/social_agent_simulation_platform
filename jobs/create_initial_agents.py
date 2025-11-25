"""Given the database of Bluesky profiles and feed posts, create a list of agents."""

from db.db import read_all_profiles, read_all_feed_posts
from db.models import BlueskyProfile, BlueskyFeedPost
from ai.agents import SocialMediaAgent


def generate_bio() -> str:
    pass


def create_initial_agents() -> list[SocialMediaAgent]:
    """Create a list of agents from the database of Bluesky profiles and feed
    posts and pass into the network."""
    profiles = read_all_profiles()
    feed_posts = read_all_feed_posts()
    agents: list[SocialMediaAgent] = []
    for profile in profiles:
        agent = SocialMediaAgent(profile.handle)
        agent.bio = profile.bio
        agent.followers = profile.followers_count
        agent.following = profile.follows_count
        agent.posts_count = profile.posts_count
        agent.posts = [
            post for post in feed_posts if post.author_handle == profile.handle
        ]
        agent.likes = []
        agent.comments = []
        agent.follows = []
        agent.generated_bio = generate_bio()
        agents.append(agent)
    return agents


if __name__ == "__main__":
    # create initial AI-generated bios, 