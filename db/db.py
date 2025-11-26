"""Database operations for the agent simulation platform.

Provides read/write operations for Bluesky profiles and feed posts
using SQLite.
"""

import json
import os
import sqlite3
from typing import Optional

from db.models import BlueskyFeedPost, BlueskyProfile, GeneratedBio, GeneratedFeed
from lib.utils import get_current_timestamp

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
    """
    Create the SQLite schema required by the application if it is missing.
    
    Creates these tables when they do not already exist:
    - bluesky_profiles: handle (PK), did, display_name, bio, followers_count, follows_count, posts_count
    - bluesky_feed_posts: uri (PK), author_display_name, author_handle, text, bookmark_count, like_count, quote_count, reply_count, repost_count, created_at
    - agent_bios: handle (PK), generated_bio, created_at
    - generated_feeds: feed_id, run_id, turn_number, agent_handle, post_uris, created_at with a composite primary key (agent_handle, run_id, turn_number)
    
    Commits the schema changes to the database.
    """
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

        conn.commit()


def write_profile(profile: BlueskyProfile) -> None:
    """Write a Bluesky profile to the database.
    
    Args:
        profile: BlueskyProfile model to write
    """
    with get_connection() as conn:
        conn.execute("""
            INSERT OR REPLACE INTO bluesky_profiles 
            (handle, did, display_name, bio, followers_count, follows_count, posts_count)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            profile.handle,
            profile.did,
            profile.display_name,
            profile.bio,
            profile.followers_count,
            profile.follows_count,
            profile.posts_count,
        ))
        conn.commit()


def write_feed_post(post: BlueskyFeedPost) -> None:
    """Write a Bluesky feed post to the database.
    
    Args:
        post: BlueskyFeedPost model to write
    """
    with get_connection() as conn:
        conn.execute("""
            INSERT OR REPLACE INTO bluesky_feed_posts
            (uri, author_display_name, author_handle, text, bookmark_count,
             like_count, quote_count, reply_count, repost_count, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
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
        ))
        conn.commit()


def write_feed_posts(posts: list[BlueskyFeedPost]) -> None:
    """Write multiple Bluesky feed posts to the database.
    
    Args:
        posts: List of BlueskyFeedPost models to write
    """
    with get_connection() as conn:
        conn.executemany("""
            INSERT OR REPLACE INTO bluesky_feed_posts
            (uri, author_display_name, author_handle, text, bookmark_count,
             like_count, quote_count, reply_count, repost_count, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
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
        ])
        conn.commit()


def write_generated_bio_to_database(handle: str, generated_bio: str) -> None:
    """
    Store or update the generated bio for a profile handle in the agent_bios table and record the current timestamp.
    
    Parameters:
        handle (str): Profile handle to associate the generated bio with.
        generated_bio (str): Generated biography text to store.
    """
    with get_connection() as conn:
        conn.execute("""
            INSERT OR REPLACE INTO agent_bios
            (handle, generated_bio, created_at)
            VALUES (?, ?, ?)
        """, (handle, generated_bio, get_current_timestamp()))
        conn.commit()


# TODO: we create a feed_id even though the PK for now is
# agent_handle, run_id, turn_number because maybe at some point we'll have
# multiple feeds per agent per run.
def write_generated_feed(feed: GeneratedFeed) -> None:
    """
    Insert or replace a GeneratedFeed record in the database.
    
    Stores the feed's fields into the generated_feeds table; the `post_uris` list is JSON-encoded before storage. If a record exists for the same (agent_handle, run_id, turn_number) it will be replaced.
    
    Parameters:
        feed (GeneratedFeed): The generated feed to persist.
    """
    with get_connection() as conn:
        conn.execute("""
            INSERT OR REPLACE INTO generated_feeds
            (feed_id, run_id, turn_number, agent_handle, post_uris, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            feed.feed_id,
            feed.run_id,
            feed.turn_number,
            feed.agent_handle,
            json.dumps(feed.post_uris),
            feed.created_at,
        ))
        conn.commit()

def read_generated_feed(agent_handle: str, run_id: str, turn_number: int) -> GeneratedFeed:
    """
    Retrieve the GeneratedFeed for the given agent, run, and turn.
    
    Parameters:
        agent_handle (str): Agent handle to look up.
        run_id (str): Run ID to look up.
        turn_number (int): Turn number to look up.
    
    Returns:
        GeneratedFeed: The generated feed for the specified agent, run, and turn.
    
    Raises:
        ValueError: If no feed is found for the given agent_handle, run_id, and turn_number.
    """
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM generated_feeds WHERE agent_handle = ? AND run_id = ? AND turn_number = ?",
            (agent_handle, run_id, turn_number)
        ).fetchone()
        
        if row is None:
            # this isn't supposed to happen, so we want to raise an error if it does.
            raise ValueError(f"Generated feed not found for agent {agent_handle}, run {run_id}, turn {turn_number}")
        
        return GeneratedFeed(
            feed_id=row["feed_id"],
            run_id=row["run_id"],
            turn_number=row["turn_number"],
            agent_handle=row["agent_handle"],
            post_uris=json.loads(row["post_uris"]),
            created_at=row["created_at"],
        )

def read_profile(handle: str) -> Optional[BlueskyProfile]:
    """Read a Bluesky profile by handle.
    
    Args:
        handle: Profile handle to look up
        
    Returns:
        BlueskyProfile if found, None otherwise
    """
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM bluesky_profiles WHERE handle = ?",
            (handle,)
        ).fetchone()
        
        if row is None:
            return None
        
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
    
    Returns:
        List of all BlueskyProfile models
    """
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM bluesky_profiles").fetchall()
        
        return [
            BlueskyProfile(
                handle=row["handle"],
                did=row["did"],
                display_name=row["display_name"],
                bio=row["bio"],
                followers_count=row["followers_count"],
                follows_count=row["follows_count"],
                posts_count=row["posts_count"],
            )
            for row in rows
        ]


def read_feed_post(uri: str) -> Optional[BlueskyFeedPost]:
    """Read a Bluesky feed post by URI.
    
    Args:
        uri: Post URI to look up
        
    Returns:
        BlueskyFeedPost if found, None otherwise
    """
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM bluesky_feed_posts WHERE uri = ?",
            (uri,)
        ).fetchone()
        
        if row is None:
            return None
        
        return BlueskyFeedPost(
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
    
    Args:
        author_handle: Author handle to filter by
        
    Returns:
        List of BlueskyFeedPost models for the author
    """
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM bluesky_feed_posts WHERE author_handle = ?",
            (author_handle,)
        ).fetchall()
        
        return [
            BlueskyFeedPost(
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
            for row in rows
        ]


def read_all_feed_posts() -> list[BlueskyFeedPost]:
    """Read all Bluesky feed posts from the database.
    
    Returns:
        List of all BlueskyFeedPost models
    """
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM bluesky_feed_posts").fetchall()
        
        return [
            BlueskyFeedPost(
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
            for row in rows
        ]


def read_all_generated_bios() -> list[GeneratedBio]:
    """
    Retrieve all generated bios stored in the database.
    
    Returns:
        list[GeneratedBio]: All GeneratedBio models present in the agent_bios table.
    """
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM agent_bios").fetchall()
        return [
            GeneratedBio(
                handle=row["handle"],
                generated_bio=row["generated_bio"],
                created_at=row["created_at"],
            )
            for row in rows
        ]

def load_feed_post_uris_from_current_run(
    agent_handle: str, run_id: str
) -> set[str]:
    """Load the feed post URIs from the current run.
    
    Args:
        agent_handle: Agent handle to look up
        run_id: Run ID to look up
        
    Returns:
        Set of feed post URIs
    """
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT post_uris
            FROM generated_feeds
            WHERE agent_handle = ? AND run_id = ?
            GROUP BY post_uris
        """, (agent_handle, run_id)).fetchall()
        return set(json.loads(row["post_uris"]) for row in rows)