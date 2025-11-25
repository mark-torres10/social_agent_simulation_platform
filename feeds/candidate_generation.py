"""Generate candidate posts for the feeds."""

from ai.agents import SocialMediaAgent
from db.db import read_all_feed_posts
from db.models import BlueskyFeedPost


# TODO: we can get arbitrarily complex with how we do this later
# on, but as a first pass it's easy enough to just load all the posts.
def load_posts() -> list[BlueskyFeedPost]:
    """Load the posts for the feeds."""
    return read_all_feed_posts()


def load_seen_post_uris(agent: SocialMediaAgent) -> set[str]:
    """Load the posts that the agent has already seen.
    
    Returns a set of URIs"""
    return set()


def filter_candidate_posts(
    posts: list[BlueskyFeedPost],
    agent: SocialMediaAgent
) -> list[BlueskyFeedPost]:
    """Filter the posts that are candidates for the feeds.
    
    Remove posts that:
    - The agent has already seen.
    - The agent themselves posted (or their original Bluesky profile posted)
    """

    seen_post_uris: set[str] = load_seen_post_uris(agent)
    candidate_posts = [
        p for p in posts
        if p.uri not in seen_post_uris
        and p.author_handle != agent.handle
    ]

    return candidate_posts


def load_candidate_posts(agent: SocialMediaAgent) -> list[BlueskyFeedPost]:
    """Load the candidate posts for the feeds.
    
    Remove posts that:
    - The agent has already seen.
    - The agent themselves posted (or their original Bluesky profile posted)
    """
    candidate_posts: list[BlueskyFeedPost] = load_posts()
    candidate_posts = filter_candidate_posts(candidate_posts, agent)
    return candidate_posts
