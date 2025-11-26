"""Container logic for different feed generation algorithms"""

# TODO: for now, we'll generate the feeds in real-time during the simulations,
# but in practice we would generate them offline.
from db.models import GeneratedFeed
from ai.agents import SocialMediaAgent
from db.models import BlueskyFeedPost

from lib.utils import get_current_timestamp


MAX_POSTS_PER_FEED = 20

def generate_chronological_feed(
    candidate_posts: list[BlueskyFeedPost],
    agent: SocialMediaAgent,
    limit: int = MAX_POSTS_PER_FEED
) -> dict:
    """
    Create a chronological feed for an agent from candidate posts.
    
    Returns:
        dict: A mapping with:
            - feed_id: unique identifier for the generated feed.
            - agent_handle: the agent's handle.
            - post_uris: list of post URIs ordered from newest to oldest.
    """
    # TODO: fast follow: insert randomness so that the feed isn't always the
    # same across rounds.
    sorted_posts = sorted(candidate_posts, key=lambda p: p.created_at, reverse=True)
    sorted_posts = sorted_posts[:limit]
    feed_id = GeneratedFeed.generate_feed_id()
    return {
        "feed_id": feed_id,
        "agent_handle": agent.handle,
        "post_uris": [p.uri for p in sorted_posts]
    }


# TODO: placeholder for next ticket.
def generate_rag_feed() -> GeneratedFeed:
    """
    Constructs a retrieval-augmented generation (RAG) feed that combines agent context with externally retrieved content.
    
    This function is a placeholder for the RAG-based feed generation algorithm and is currently unimplemented. When implemented, it should return a GeneratedFeed containing the assembled feed metadata and post references produced by the RAG process.
    
    Returns:
        GeneratedFeed: The generated feed configured using the RAG strategy.
    """
    pass