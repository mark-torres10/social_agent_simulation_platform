"""Given the database of Bluesky profiles and feed posts, create a list of agents."""

from db.db import read_all_profiles, read_all_feed_posts
from db.models import BlueskyProfile, BlueskyFeedPost, GeneratedBio
from ai.agents import SocialMediaAgent
from db.db import read_all_generated_bios


def create_initial_agents() -> list[SocialMediaAgent]:
    """Create a list of agents from the database of Bluesky profiles and feed
    posts and pass into the network."""
    profiles: list[BlueskyProfile] = read_all_profiles()
    feed_posts: list[BlueskyFeedPost] = read_all_feed_posts()
    generated_bios: list[GeneratedBio] = read_all_generated_bios()

    handle_to_feed_posts: dict[str, list[BlueskyFeedPost]] = {
        profile.handle: [
            post for post in feed_posts if post.author_handle == profile.handle
        ]
        for profile in profiles
    }
    handle_to_generated_bio: dict[str, GeneratedBio] = {
        profile.handle: [
            bio for bio in generated_bios if bio.handle == profile.handle
        ][0]
        for profile in profiles
    }
    agents: list[SocialMediaAgent] = []

    for profile in profiles:
        agent = SocialMediaAgent(profile.handle)
        agent.bio = profile.bio
        agent.followers: int = profile.followers_count
        agent.following: int = profile.follows_count
        agent.posts_count: int = profile.posts_count
        agent.posts = handle_to_feed_posts[profile.handle]
        agent.likes = []
        agent.comments = []
        agent.follows = []
        agent.generated_bio = handle_to_generated_bio[profile.handle].generated_bio
        agents.append(agent)
    return agents


if __name__ == "__main__":
    pass
