import logging
from typing import Callable

from db.repositories.feed_post_repository import FeedPostRepository
from db.repositories.generated_feed_repository import GeneratedFeedRepository
from feeds.algorithms import generate_chronological_feed
from feeds.candidate_generation import load_candidate_posts
from lib.utils import get_current_timestamp
from simulation.core.models.agents import SocialMediaAgent
from simulation.core.models.feeds import GeneratedFeed
from simulation.core.models.posts import BlueskyFeedPost


logger = logging.getLogger(__name__)

_FEED_ALGORITHMS: dict[str, Callable] = {
    "chronological": generate_chronological_feed,
    # "rag": generate_rag_feed,  # TODO: Add in future PR
}

def generate_feed(
    agent: SocialMediaAgent,
    candidate_posts: list[BlueskyFeedPost],
    run_id: str,
    turn_number: int,
    feed_algorithm: str,
) -> GeneratedFeed:
    """Generate a feed for an agent."""
    if feed_algorithm not in _FEED_ALGORITHMS:
        raise ValueError(f"Unknown feed algorithm: {feed_algorithm}")
    algorithm = _FEED_ALGORITHMS[feed_algorithm]
    feed_dict = algorithm(candidate_posts=candidate_posts, agent=agent)
    return GeneratedFeed(
        feed_id=feed_dict["feed_id"],
        run_id=run_id,
        turn_number=turn_number,
        agent_handle=feed_dict["agent_handle"],
        post_uris=feed_dict["post_uris"],
        created_at=get_current_timestamp(),
    )


def generate_feeds(
    agents: list[SocialMediaAgent],
    run_id: str,
    turn_number: int,
    generated_feed_repo: GeneratedFeedRepository,
    feed_post_repo: FeedPostRepository,
    feed_algorithm: str,
) -> dict[str, list[BlueskyFeedPost]]:
    """Generate feeds for all the agents.

    Returns a dictionary of agent handles to lists of hydrated BlueskyFeedPost models.

    Does the following:
    1. Generates a feed for each agent.
    2. Writes the unhydrated feeds to the database.
    3. Hydrates the posts for each feed.
    4. Returns a dictionary of agent handles to lists of hydrated BlueskyFeedPost models.
    """
    feeds: dict[str, GeneratedFeed] = {}
    for agent in agents:
        # TODO: right now we load all posts per agent, but obviously
        # can optimize and personalize later to save on queries.
        candidate_posts: list[BlueskyFeedPost] = load_candidate_posts(
            agent=agent, run_id=run_id
        )
        feed: GeneratedFeed = generate_feed(
            agent=agent,
            candidate_posts=candidate_posts,
            run_id=run_id,
            turn_number=turn_number,
            feed_algorithm=feed_algorithm,
        )
        generated_feed_repo.create_or_update_generated_feed(feed)
        feeds[agent.handle] = feed

    # iterate through feeds, grab only the unique URIs, and hydrate
    all_post_uris: set[str] = set()
    for feed in feeds.values():
        all_post_uris.update(feed.post_uris)

    hydrated_posts: list[BlueskyFeedPost] = feed_post_repo.read_feed_posts_by_uris(all_post_uris)
    uri_to_post: dict[str, BlueskyFeedPost] = {p.uri: p for p in hydrated_posts}

    # now iterate through feeds and hydrate the posts.
    agent_to_hydrated_feeds: dict[str, list[BlueskyFeedPost]] = {}
    for agent_handle, feed in feeds.items():
        hydrated_posts: list[BlueskyFeedPost] = []
        for post_uri in feed.post_uris:
            # Skip silently if missing. Currently OK and matches other specs
            # related to graceful handling of missing posts. Can be
            # revisited as a fast follow later. Curently, missing posts are an
            # edge case.
            if post_uri not in uri_to_post:
                logger.warning(
                    f"Missing post URI in feed: agent_handle={agent_handle}, "
                    f"feed_id={feed.feed_id}, missing_uri={post_uri}"
                )
                continue
            hydrated_posts.append(uri_to_post[post_uri])
        agent_to_hydrated_feeds[agent_handle] = hydrated_posts

    return agent_to_hydrated_feeds
