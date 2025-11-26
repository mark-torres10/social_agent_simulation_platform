"""Generate candidate posts for the feeds."""

from ai.agents import SocialMediaAgent
from db.db import read_all_feed_posts, load_feed_post_uris_from_current_run
from db.models import BlueskyFeedPost


# TODO: we can get arbitrarily complex with how we do this later
# on, but as a first pass it's easy enough to just load all the posts.
def load_posts() -> list[BlueskyFeedPost]:
    """
    Load all available Bluesky feed posts.
    
    Returns:
        posts (list[BlueskyFeedPost]): All stored feed posts.
    """
    return read_all_feed_posts()


def load_seen_post_uris(
    agent: SocialMediaAgent,
    run_id: str
) -> set[str]:
    """
    Retrieve the URIs of feed posts the agent has already seen in the specified run.
    
    Parameters:
        agent (SocialMediaAgent): The agent whose seen posts to load.
        run_id (str): Identifier of the run to query seen posts for.
    
    Returns:
        set[str]: URIs of posts the agent has seen during the given run.
    """
    return load_feed_post_uris_from_current_run(
        agent_handle=agent.handle,
        run_id=run_id
    )


def filter_candidate_posts(
    candidate_posts: list[BlueskyFeedPost],
    agent: SocialMediaAgent,
    run_id: str
) -> list[BlueskyFeedPost]:
    """
    Filter out feed posts the agent has already seen or that were authored by the agent.
    
    Parameters:
        candidate_posts (list[BlueskyFeedPost]): Candidate feed posts to be filtered.
        agent (SocialMediaAgent): Agent whose seen post URIs and handle are used to exclude posts.
        run_id (str): Identifier of the current run used to determine which posts the agent has already seen.
    
    Returns:
        list[BlueskyFeedPost]: Posts from `candidate_posts` excluding any with a URI the agent has seen for `run_id` or with an author handle equal to `agent.handle`.
    """

    seen_post_uris: set[str] = load_seen_post_uris(agent=agent, run_id=run_id)
    candidate_posts = [
        p for p in candidate_posts
        if p.uri not in seen_post_uris
        and p.author_handle != agent.handle
    ]

    return candidate_posts


def load_candidate_posts(agent: SocialMediaAgent, run_id: str) -> list[BlueskyFeedPost]:
    """
    Load feed candidate posts and filter out posts the agent has already seen or authored.
    
    Parameters:
        agent (SocialMediaAgent): The agent for whom candidate posts are being loaded.
        run_id (str): Identifier of the current run used to determine which posts are considered seen.
    
    Returns:
        list[BlueskyFeedPost]: Candidate posts excluding those whose URI the agent has already seen in the given run and posts authored by the agent.
    """
    candidate_posts: list[BlueskyFeedPost] = load_posts()
    candidate_posts = filter_candidate_posts(
        candidate_posts=candidate_posts,
        agent=agent,
        run_id=run_id
    )
    return candidate_posts