"""Database operations for the agent simulation platform.

This module contains internal SQLite implementation functions used by the
SQLite adapters. These functions are NOT part of the public API.

External code should use the Repository/Adapter pattern instead:
- ProfileRepository for profile operations
- FeedPostRepository for feed post operations
- GeneratedBioRepository for generated bio operations
- GeneratedFeedRepository for generated feed operations
- RunRepository for run operations

The functions in this module are implementation details and may change
without notice. They are used internally by:
- db.adapters.sqlite.profile_adapter
- db.adapters.sqlite.feed_post_adapter
- db.adapters.sqlite.generated_bio_adapter
- db.adapters.sqlite.generated_feed_adapter
- db.adapters.sqlite.run_adapter
"""

import json
import os
import sqlite3
from typing import Optional

from db.exceptions import RunNotFoundError
from lib.utils import get_current_timestamp
from simulation.core.models.feeds import GeneratedFeed
from simulation.core.models.generated.bio import GeneratedBio
from simulation.core.models.posts import BlueskyFeedPost
from simulation.core.models.profiles import BlueskyProfile
from simulation.core.models.runs import Run

DB_PATH = os.path.join(os.path.dirname(__file__), "db.sqlite")


def get_connection() -> sqlite3.Connection:
    """Get a database connection.

    Returns:
        SQLite connection to db.sqlite
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database() -> None:
    """Initialize the database by creating tables if they don't exist."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS bluesky_profiles (
                handle TEXT PRIMARY KEY,
                did TEXT NOT NULL,
                display_name TEXT NOT NULL,
                bio TEXT NOT NULL,
                followers_count INTEGER NOT NULL,
                follows_count INTEGER NOT NULL,
                posts_count INTEGER NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS bluesky_feed_posts (
                uri TEXT PRIMARY KEY,
                author_display_name TEXT NOT NULL,
                author_handle TEXT NOT NULL,
                text TEXT NOT NULL,
                bookmark_count INTEGER NOT NULL,
                like_count INTEGER NOT NULL,
                quote_count INTEGER NOT NULL,
                reply_count INTEGER NOT NULL,
                repost_count INTEGER NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS agent_bios (
                handle TEXT PRIMARY KEY,
                generated_bio TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS generated_feeds (
                feed_id TEXT NOT NULL,
                run_id TEXT NOT NULL,
                turn_number INTEGER NOT NULL,
                agent_handle TEXT NOT NULL,
                post_uris TEXT NOT NULL,
                created_at TEXT NOT NULL,
                PRIMARY KEY (agent_handle, run_id, turn_number)
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS runs (
                run_id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                total_turns INTEGER NOT NULL CHECK (total_turns > 0),
                total_agents INTEGER NOT NULL CHECK (total_agents > 0),
                started_at TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('running', 'completed', 'failed')),
                completed_at TEXT NULL,
                CHECK (
                    (status = 'completed' AND completed_at IS NOT NULL AND completed_at >= started_at) OR
                    (status != 'completed' AND completed_at IS NULL)
                )
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS turn_metadata (
                run_id TEXT NOT NULL,
                turn_number INTEGER NOT NULL,
                total_actions TEXT NOT NULL,
                created_at TEXT NOT NULL,
                PRIMARY KEY (run_id, turn_number)
            )
        """)

        # Create indexes for frequently queried columns
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_runs_status ON runs(status)
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_runs_created_at ON runs(created_at DESC)
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_bluesky_feed_posts_author_handle 
            ON bluesky_feed_posts(author_handle)
        """)

        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_turn_metadata_run_id ON turn_metadata(run_id)
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_turn_metadata_turn_number ON turn_metadata(turn_number)
        """)

        conn.commit()


def write_profile(profile: BlueskyProfile) -> None:
    """Write a Bluesky profile to the database.

    INTERNAL: This function is an implementation detail used by SQLiteProfileAdapter.
    External code should use ProfileRepository.create_or_update_profile() instead.

    Args:
        profile: BlueskyProfile model to write

    Raises:
        sqlite3.IntegrityError: If handle violates constraints
        sqlite3.OperationalError: If database operation fails
    """
    with get_connection() as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO bluesky_profiles 
            (handle, did, display_name, bio, followers_count, follows_count, posts_count)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                profile.handle,
                profile.did,
                profile.display_name,
                profile.bio,
                profile.followers_count,
                profile.follows_count,
                profile.posts_count,
            ),
        )
        conn.commit()


def write_feed_post(post: BlueskyFeedPost) -> None:
    """Write a Bluesky feed post to the database.

    INTERNAL: This function is an implementation detail used by SQLiteFeedPostAdapter.
    External code should use FeedPostRepository.create_or_update_feed_post() instead.

    Args:
        post: BlueskyFeedPost model to write

    Raises:
        sqlite3.IntegrityError: If uri violates constraints
        sqlite3.OperationalError: If database operation fails
    """
    with get_connection() as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO bluesky_feed_posts
            (uri, author_display_name, author_handle, text, bookmark_count,
             like_count, quote_count, reply_count, repost_count, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                post.uri,
                post.author_display_name,
                post.author_handle,
                post.text,
                post.bookmark_count,
                post.like_count,
                post.quote_count,
                post.reply_count,
                post.repost_count,
                post.created_at,
            ),
        )
        conn.commit()


def write_feed_posts(posts: list[BlueskyFeedPost]) -> None:
    """Write multiple Bluesky feed posts to the database (batch operation).

    INTERNAL: This function is an implementation detail used by SQLiteFeedPostAdapter.
    External code should use FeedPostRepository.create_or_update_feed_posts() instead.

    This function uses executemany for efficient batch insertion. All posts
    are written in a single atomic transaction. If any post fails, the entire
    batch will be rolled back.

    Args:
        posts: List of BlueskyFeedPost models to write. Empty list is allowed
               and will result in no database operations.

    Raises:
        sqlite3.IntegrityError: If any uri violates constraints
        sqlite3.OperationalError: If database operation fails
    """
    if not posts:
        return

    with get_connection() as conn:
        try:
            conn.executemany(
                """
                INSERT OR REPLACE INTO bluesky_feed_posts
                (uri, author_display_name, author_handle, text, bookmark_count,
                 like_count, quote_count, reply_count, repost_count, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                [
                    (
                        post.uri,
                        post.author_display_name,
                        post.author_handle,
                        post.text,
                        post.bookmark_count,
                        post.like_count,
                        post.quote_count,
                        post.reply_count,
                        post.repost_count,
                        post.created_at,
                    )
                    for post in posts
                ],
            )
            conn.commit()
        except Exception:
            conn.rollback()
            raise


def write_generated_bio_to_database(
    handle: str, generated_bio: str, created_at: str | None = None
) -> None:
    """Write a generated bio to the database.

    INTERNAL: This function is an implementation detail used by SQLiteGeneratedBioAdapter.
    External code should use GeneratedBioRepository.create_or_update_generated_bio() instead.

    Args:
        handle: Handle of the profile
        generated_bio: Generated bio string
        created_at: Optional timestamp. If None, uses current timestamp.

    Raises:
        sqlite3.IntegrityError: If handle violates constraints
        sqlite3.OperationalError: If database operation fails
    """
    if created_at is None:
        created_at = get_current_timestamp()
    with get_connection() as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO agent_bios
            (handle, generated_bio, created_at)
            VALUES (?, ?, ?)
        """,
            (handle, generated_bio, created_at),
        )
        conn.commit()


# TODO: we create a feed_id even though the PK for now is
# agent_handle, run_id, turn_number because maybe at some point we'll have
# multiple feeds per agent per run.
def write_generated_feed(feed: GeneratedFeed) -> None:
    """Write a generated feed to the database.

    INTERNAL: This function is an implementation detail used by SQLiteGeneratedFeedAdapter.
    External code should use GeneratedFeedRepository.create_or_update_generated_feed() instead.

    Args:
        feed: GeneratedFeed model to write

    Raises:
        sqlite3.IntegrityError: If composite key (agent_handle, run_id, turn_number) violates constraints
        sqlite3.OperationalError: If database operation fails
    """
    with get_connection() as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO generated_feeds
            (feed_id, run_id, turn_number, agent_handle, post_uris, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                feed.feed_id,
                feed.run_id,
                feed.turn_number,
                feed.agent_handle,
                json.dumps(feed.post_uris),
                feed.created_at,
            ),
        )
        conn.commit()


def write_run(run: Run) -> None:
    """Write a run to the database.

    INTERNAL: This function is an implementation detail used by SQLiteRunAdapter.
    External code should use RunRepository.create_or_update_run() instead.

    This function creates or replaces a single run record within
    its own transaction scope. If you need to perform multi-table
    operations that must succeed or fail together (e.g., creating a run
    and related records in other tables), you are responsible for
    managing the transaction boundaries externally. Use a single
    database connection and control commit/rollback yourself in such cases,
    or refactor to accept an existing connection.

    Args:
        run: Run model to write

    Raises:
        sqlite3.IntegrityError: If run_id violates constraints
        sqlite3.OperationalError: If database operation fails

    Note:
        Uses INSERT OR REPLACE, so this will overwrite existing runs
        with the same run_id.
    """
    with get_connection() as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO runs 
            (run_id, created_at, total_turns, total_agents, started_at, status, completed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                run.run_id,
                run.created_at,
                run.total_turns,
                run.total_agents,
                run.started_at,
                run.status.value,  # Convert enum to string explicitly
                run.completed_at,
            ),
        )
        conn.commit()


def read_generated_feed(
    agent_handle: str, run_id: str, turn_number: int
) -> GeneratedFeed:
    """Read a generated feed by agent_handle, run_id, and turn_number.

    INTERNAL: This function is an implementation detail used by SQLiteGeneratedFeedAdapter.
    External code should use GeneratedFeedRepository.get_generated_feed() instead.

    Args:
        agent_handle: Agent handle to look up
        run_id: Run ID to look up
        turn_number: Turn number to look up

    Returns:
        GeneratedFeed model for the specified agent, run, and turn

    Raises:
        ValueError: If no feed is found for the given agent_handle, run_id, and turn_number
        ValueError: If the feed data is invalid (NULL fields)
        KeyError: If required columns are missing from the database row
        sqlite3.OperationalError: If database operation fails
    """
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM generated_feeds WHERE agent_handle = ? AND run_id = ? AND turn_number = ?",
            (agent_handle, run_id, turn_number),
        ).fetchone()

        if row is None:
            # this isn't supposed to happen, so we want to raise an error if it does.
            raise ValueError(
                f"Generated feed not found for agent {agent_handle}, run {run_id}, turn {turn_number}"
            )

        # Validate required fields are not NULL
        context = f"generated feed agent_handle={agent_handle}, run_id={run_id}, turn_number={turn_number}"
        _validate_generated_feed_row(row, context=context)

        return GeneratedFeed(
            feed_id=row["feed_id"],
            run_id=row["run_id"],
            turn_number=row["turn_number"],
            agent_handle=row["agent_handle"],
            post_uris=json.loads(row["post_uris"]),
            created_at=row["created_at"],
        )


def _validate_generated_feed_row(row: sqlite3.Row, context: str | None = None) -> None:
    """Validate that all required generated feed fields are not NULL.

    Args:
        row: SQLite Row object containing generated feed data
        context: Optional context string to include in error messages
                 (e.g., "generated feed agent_handle=user.bsky.social, run_id=...")

    Raises:
        ValueError: If any required field is NULL. Error message includes
                    the field name and optional context.
    """
    required_fields = [
        "feed_id",
        "run_id",
        "turn_number",
        "agent_handle",
        "post_uris",
        "created_at",
    ]

    for field in required_fields:
        if row[field] is None:
            error_msg = f"{field} cannot be NULL"
            if context:
                error_msg = f"{error_msg} (context: {context})"
            raise ValueError(error_msg)


def _validate_feed_post_row(row: sqlite3.Row, context: str | None = None) -> None:
    """Validate that all required feed post fields are not NULL.

    Args:
        row: SQLite Row object containing feed post data
        context: Optional context string to include in error messages
                 (e.g., "feed post uri=at://did:plc:.../app.bsky.feed.post/...")

    Raises:
        ValueError: If any required field is NULL. Error message includes
                    the field name and optional context.
    """
    required_fields = [
        "uri",
        "author_display_name",
        "author_handle",
        "text",
        "bookmark_count",
        "like_count",
        "quote_count",
        "reply_count",
        "repost_count",
        "created_at",
    ]

    for field in required_fields:
        if row[field] is None:
            error_msg = f"{field} cannot be NULL"
            if context:
                error_msg = f"{error_msg} (context: {context})"
            raise ValueError(error_msg)


def read_profile(handle: str) -> Optional[BlueskyProfile]:
    """Read a Bluesky profile by handle.

    INTERNAL: This function is an implementation detail used by SQLiteProfileAdapter.
    External code should use ProfileRepository.get_profile() instead.

    Args:
        handle: Profile handle to look up

    Returns:
        BlueskyProfile if found, None otherwise

    Raises:
        ValueError: If the profile data is invalid (NULL fields)
        KeyError: If required columns are missing from the database row
        sqlite3.OperationalError: If database operation fails
    """
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM bluesky_profiles WHERE handle = ?", (handle,)
        ).fetchone()

        if row is None:
            return None

        # Validate required fields are not NULL
        if row["handle"] is None:
            raise ValueError("handle cannot be NULL")
        if row["did"] is None:
            raise ValueError("did cannot be NULL")
        if row["display_name"] is None:
            raise ValueError("display_name cannot be NULL")
        if row["bio"] is None:
            raise ValueError("bio cannot be NULL")
        if row["followers_count"] is None:
            raise ValueError("followers_count cannot be NULL")
        if row["follows_count"] is None:
            raise ValueError("follows_count cannot be NULL")
        if row["posts_count"] is None:
            raise ValueError("posts_count cannot be NULL")

        return BlueskyProfile(
            handle=row["handle"],
            did=row["did"],
            display_name=row["display_name"],
            bio=row["bio"],
            followers_count=row["followers_count"],
            follows_count=row["follows_count"],
            posts_count=row["posts_count"],
        )


def read_all_profiles() -> list[BlueskyProfile]:
    """Read all Bluesky profiles from the database.

    INTERNAL: This function is an implementation detail used by SQLiteProfileAdapter.
    External code should use ProfileRepository.list_profiles() instead.

    Returns:
        List of all BlueskyProfile models. Returns empty list if no profiles exist.

    Raises:
        ValueError: If any profile data is invalid (NULL fields)
        KeyError: If required columns are missing from any database row
        sqlite3.OperationalError: If database operation fails
    """
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM bluesky_profiles").fetchall()

        profiles = []
        for row in rows:
            # Validate required fields are not NULL
            if row["handle"] is None:
                raise ValueError("handle cannot be NULL")
            if row["did"] is None:
                raise ValueError("did cannot be NULL")
            if row["display_name"] is None:
                raise ValueError("display_name cannot be NULL")
            if row["bio"] is None:
                raise ValueError("bio cannot be NULL")
            if row["followers_count"] is None:
                raise ValueError("followers_count cannot be NULL")
            if row["follows_count"] is None:
                raise ValueError("follows_count cannot be NULL")
            if row["posts_count"] is None:
                raise ValueError("posts_count cannot be NULL")

            profiles.append(
                BlueskyProfile(
                    handle=row["handle"],
                    did=row["did"],
                    display_name=row["display_name"],
                    bio=row["bio"],
                    followers_count=row["followers_count"],
                    follows_count=row["follows_count"],
                    posts_count=row["posts_count"],
                )
            )

        return profiles


def read_feed_post(uri: str) -> BlueskyFeedPost:
    """Read a Bluesky feed post by URI.

    INTERNAL: This function is an implementation detail used by SQLiteFeedPostAdapter.
    External code should use FeedPostRepository.get_feed_post() instead.

    Args:
        uri: Post URI to look up

    Returns:
        BlueskyFeedPost model if found.

    Raises:
        ValueError: If uri is empty or if no feed post is found for the given URI
        ValueError: If the feed post data is invalid (NULL fields)
        KeyError: If required columns are missing from the database row
        sqlite3.OperationalError: If database operation fails
    """
    if not uri or not uri.strip():
        raise ValueError("uri cannot be empty")

    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM bluesky_feed_posts WHERE uri = ?", (uri,)
        ).fetchone()

        if row is None:
            raise ValueError(f"No feed post found for uri: {uri}")

        # Validate required fields are not NULL
        context = f"feed post uri={uri}"
        _validate_feed_post_row(row, context=context)

        return BlueskyFeedPost(
            id=row["uri"],
            uri=row["uri"],
            author_display_name=row["author_display_name"],
            author_handle=row["author_handle"],
            text=row["text"],
            bookmark_count=row["bookmark_count"],
            like_count=row["like_count"],
            quote_count=row["quote_count"],
            reply_count=row["reply_count"],
            repost_count=row["repost_count"],
            created_at=row["created_at"],
        )


def read_feed_posts_by_author(author_handle: str) -> list[BlueskyFeedPost]:
    """Read all feed posts by a specific author.

    INTERNAL: This function is an implementation detail used by SQLiteFeedPostAdapter.
    External code should use FeedPostRepository.list_feed_posts_by_author() instead.

    Args:
        author_handle: Author handle to filter by

    Returns:
        List of BlueskyFeedPost models for the author

    Raises:
        ValueError: If any feed post data is invalid (NULL fields)
        KeyError: If required columns are missing from any database row
        sqlite3.OperationalError: If database operation fails
    """
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM bluesky_feed_posts WHERE author_handle = ?", (author_handle,)
        ).fetchall()

        posts = []
        for row in rows:
            # Validate required fields are not NULL
            # Try to get uri for context, fallback if uri itself is NULL
            try:
                uri_value = row["uri"] if row["uri"] is not None else "unknown"
                context = f"feed post uri={uri_value}, author_handle={author_handle}"
            except (KeyError, TypeError):
                context = f"feed post (uri unavailable), author_handle={author_handle}"

            _validate_feed_post_row(row, context=context)

            posts.append(
                BlueskyFeedPost(
                    id=row["uri"],
                    uri=row["uri"],
                    author_display_name=row["author_display_name"],
                    author_handle=row["author_handle"],
                    text=row["text"],
                    bookmark_count=row["bookmark_count"],
                    like_count=row["like_count"],
                    quote_count=row["quote_count"],
                    reply_count=row["reply_count"],
                    repost_count=row["repost_count"],
                    created_at=row["created_at"],
                )
            )

        return posts


def read_all_feed_posts() -> list[BlueskyFeedPost]:
    """Read all Bluesky feed posts from the database.

    INTERNAL: This function is an implementation detail used by SQLiteFeedPostAdapter.
    External code should use FeedPostRepository.list_all_feed_posts() instead.

    Returns:
        List of all BlueskyFeedPost models

    Raises:
        ValueError: If any feed post data is invalid (NULL fields)
        KeyError: If required columns are missing from any database row
        sqlite3.OperationalError: If database operation fails
    """
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM bluesky_feed_posts").fetchall()

        posts = []
        for row in rows:
            # Validate required fields are not NULL
            # Try to get uri for context, fallback if uri itself is NULL
            try:
                uri_value = row["uri"] if row["uri"] is not None else "unknown"
                context = f"feed post uri={uri_value}"
            except (KeyError, TypeError):
                context = "feed post (uri unavailable)"

            _validate_feed_post_row(row, context=context)

            posts.append(
                BlueskyFeedPost(
                    id=row["uri"],
                    uri=row["uri"],
                    author_display_name=row["author_display_name"],
                    author_handle=row["author_handle"],
                    text=row["text"],
                    bookmark_count=row["bookmark_count"],
                    like_count=row["like_count"],
                    quote_count=row["quote_count"],
                    reply_count=row["reply_count"],
                    repost_count=row["repost_count"],
                    created_at=row["created_at"],
                )
            )

        return posts


def _validate_generated_bio_row(row: sqlite3.Row, context: str | None = None) -> None:
    """Validate that all required generated bio fields are not NULL.

    Args:
        row: SQLite Row object containing generated bio data
        context: Optional context string to include in error messages
                 (e.g., "generated bio handle=user.bsky.social")

    Raises:
        ValueError: If any required field is NULL. Error message includes
                    the field name and optional context.
    """
    required_fields = [
        "handle",
        "generated_bio",
        "created_at",
    ]

    for field in required_fields:
        if row[field] is None:
            error_msg = f"{field} cannot be NULL"
            if context:
                error_msg = f"{error_msg} (context: {context})"
            raise ValueError(error_msg)


def read_generated_bio(handle: str) -> Optional[GeneratedBio]:
    """Read a generated bio by handle.

    INTERNAL: This function is an implementation detail used by SQLiteGeneratedBioAdapter.
    External code should use GeneratedBioRepository.get_generated_bio() instead.

    Args:
        handle: Profile handle to look up

    Returns:
        GeneratedBio if found, None otherwise

    Raises:
        ValueError: If the bio data is invalid (NULL fields)
        KeyError: If required columns are missing from the database row
        sqlite3.OperationalError: If database operation fails
    """
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM agent_bios WHERE handle = ?", (handle,)
        ).fetchone()

        if row is None:
            return None

        # Validate required fields are not NULL
        context = f"generated bio handle={handle}"
        _validate_generated_bio_row(row, context=context)

        from simulation.core.models.generated.base import GenerationMetadata

        return GeneratedBio(
            handle=row["handle"],
            generated_bio=row["generated_bio"],
            metadata=GenerationMetadata(
                model_used=None,
                generation_metadata=None,
                created_at=row["created_at"],
            ),
        )


def read_all_generated_bios() -> list[GeneratedBio]:
    """Read all generated bios from the database.

    INTERNAL: This function is an implementation detail used by SQLiteGeneratedBioAdapter.
    External code should use GeneratedBioRepository.list_all_generated_bios() instead.

    Returns:
        List of all GeneratedBio models. Returns empty list if no bios exist.

    Raises:
        ValueError: If any bio data is invalid (NULL fields)
        KeyError: If required columns are missing from any database row
        sqlite3.OperationalError: If database operation fails
    """
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM agent_bios").fetchall()

        bios = []
        for row in rows:
            # Validate required fields are not NULL
            handle_value = row["handle"] if row["handle"] is not None else "unknown"
            context = f"generated bio handle={handle_value}"
            _validate_generated_bio_row(row, context=context)

            from simulation.core.models.generated.base import GenerationMetadata

            bios.append(
                GeneratedBio(
                    handle=row["handle"],
                    generated_bio=row["generated_bio"],
                    metadata=GenerationMetadata(
                        model_used=None,
                        generation_metadata=None,
                        created_at=row["created_at"],
                    ),
                )
            )

        return bios


def read_all_generated_feeds() -> list[GeneratedFeed]:
    """Read all generated feeds from the database.

    INTERNAL: This function is an implementation detail used by SQLiteGeneratedFeedAdapter.
    External code should use GeneratedFeedRepository.list_all_generated_feeds() instead.

    Returns:
        List of all GeneratedFeed models

    Raises:
        ValueError: If any feed data is invalid (NULL fields)
        KeyError: If required columns are missing from any database row
        sqlite3.OperationalError: If database operation fails
    """
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM generated_feeds").fetchall()

        feeds = []
        for row in rows:
            # Validate required fields are not NULL
            # Try to get identifying info for context, fallback if unavailable
            try:
                agent_handle_value = (
                    row["agent_handle"]
                    if row["agent_handle"] is not None
                    else "unknown"
                )
                run_id_value = row["run_id"] if row["run_id"] is not None else "unknown"
                turn_number_value = (
                    row["turn_number"] if row["turn_number"] is not None else "unknown"
                )
                context = f"generated feed agent_handle={agent_handle_value}, run_id={run_id_value}, turn_number={turn_number_value}"
            except (KeyError, TypeError):
                context = "generated feed (identifying info unavailable)"

            _validate_generated_feed_row(row, context=context)

            feeds.append(
                GeneratedFeed(
                    feed_id=row["feed_id"],
                    run_id=row["run_id"],
                    turn_number=row["turn_number"],
                    agent_handle=row["agent_handle"],
                    post_uris=json.loads(row["post_uris"]),
                    created_at=row["created_at"],
                )
            )

        return feeds


def read_post_uris_for_run(agent_handle: str, run_id: str) -> set[str]:
    """Read all post URIs from generated feeds for a specific agent and run.

    INTERNAL: This function is an implementation detail used by SQLiteGeneratedFeedAdapter.
    External code should use GeneratedFeedRepository.get_post_uris_for_run() instead.

    Args:
        agent_handle: Agent handle to filter by
        run_id: Run ID to filter by

    Returns:
        Set of post URIs from all generated feeds matching the agent and run.
        Returns empty set if no feeds found.

    Raises:
        ValueError: If agent_handle or run_id is empty
        sqlite3.OperationalError: If database operation fails
    """
    if not agent_handle or not agent_handle.strip():
        raise ValueError("agent_handle cannot be empty")
    if not run_id or not run_id.strip():
        raise ValueError("run_id cannot be empty")

    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT post_uris
            FROM generated_feeds
            WHERE agent_handle = ? AND run_id = ?
        """,
            (agent_handle, run_id),
        ).fetchall()
        return {uri for row in rows for uri in json.loads(row["post_uris"])}


def _row_to_run(row: sqlite3.Row) -> Run:
    """Convert a database row to a Run model.

    Args:
        row: SQLite Row object containing run data

    Returns:
        Run model instance

    Raises:
        ValueError: If required fields are NULL or status is invalid
        KeyError: If required columns are missing from row
    """
    from simulation.core.models.runs import RunStatus

    # Validate required fields are not NULL
    if row["run_id"] is None:
        raise ValueError("run_id cannot be NULL")
    if row["created_at"] is None:
        raise ValueError("created_at cannot be NULL")
    if row["total_turns"] is None:
        raise ValueError("total_turns cannot be NULL")
    if row["total_agents"] is None:
        raise ValueError("total_agents cannot be NULL")
    if row["started_at"] is None:
        raise ValueError("started_at cannot be NULL")
    if row["status"] is None:
        raise ValueError("status cannot be NULL")

    # Convert status string to RunStatus enum, handling invalid values
    try:
        status = RunStatus(row["status"])
    except ValueError as err:
        raise ValueError(
            f"Invalid status value: {row['status']}. Must be one of: {[s.value for s in RunStatus]}"
        ) from err

    return Run(
        run_id=row["run_id"],
        created_at=row["created_at"],
        total_turns=row["total_turns"],
        total_agents=row["total_agents"],
        started_at=row["started_at"],
        status=status,
        completed_at=row["completed_at"],
    )


def read_run(run_id: str) -> Optional[Run]:
    """Read a run by run_id.

    INTERNAL: This function is an implementation detail used by SQLiteRunAdapter.
    External code should use RunRepository.get_run() instead.

    Args:
        run_id: Unique identifier for the run

    Returns:
        Run model if found, None otherwise

    Raises:
        ValueError: If the run data is invalid (NULL fields, invalid status)
        sqlite3.OperationalError: If database operation fails
        KeyError: If required columns are missing from the database row
    """
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM runs WHERE run_id = ?", (run_id,)).fetchone()

        if row is None:
            return None

        return _row_to_run(row)


def read_all_runs() -> list[Run]:
    """Read all runs, ordered by created_at descending.

    INTERNAL: This function is an implementation detail used by SQLiteRunAdapter.
    External code should use RunRepository.list_runs() instead.

    Returns:
        List of Run models, ordered by created_at descending (newest first).
        Returns empty list if no runs exist.

    Raises:
        ValueError: If any run data is invalid (NULL fields, invalid status)
        sqlite3.OperationalError: If database operation fails
        KeyError: If required columns are missing from any database row
    """
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM runs ORDER BY created_at DESC").fetchall()

        return [_row_to_run(row) for row in rows]


def update_run_status(
    run_id: str, status: str, completed_at: Optional[str] = None
) -> None:
    """Update a run's status.

    INTERNAL: This function is an implementation detail used by SQLiteRunAdapter.
    External code should use RunRepository.update_run_status() instead.

    Args:
        run_id: Unique identifier for the run to update
        status: New status value (should be a valid RunStatus enum value as string)
        completed_at: Optional timestamp when the run was completed.
                     Should be set when status is 'completed', None otherwise.

    Raises:
        RunNotFoundError: If no run exists with the given run_id
        sqlite3.OperationalError: If database operation fails
        sqlite3.IntegrityError: If status value violates CHECK constraints
    """
    with get_connection() as conn:
        cursor = conn.execute(
            """
            UPDATE runs 
            SET status = ?, completed_at = ?
            WHERE run_id = ?
        """,
            (status, completed_at, run_id),
        )
        if cursor.rowcount == 0:
            raise RunNotFoundError(run_id)
        conn.commit()
