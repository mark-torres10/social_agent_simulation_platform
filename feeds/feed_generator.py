from ai.agents import SocialMediaAgent
from db.models import GeneratedFeed, BlueskyFeedPost
from feeds.algorithms import generate_chronological_feed


def generate_feed(
    agent: SocialMediaAgent, posts: list[BlueskyFeedPost], feed_type: str
) -> GeneratedFeed:
    """Generate a feed for an agent."""
    if feed_type == "chronological":
        return generate_chronological_feed(agent)
    else:
        raise NotImplementedError(f"Feed type {feed_type} not implemented")
