"""SQLite implementation of feed post database adapter."""

from db.adapters.base import FeedPostDatabaseAdapter
from db.db import _validate_feed_post_row, get_connection
from simulation.core.models.posts import BlueskyFeedPost


class SQLiteFeedPostAdapter(FeedPostDatabaseAdapter):
    """SQLite implementation of FeedPostDatabaseAdapter.

    Uses functions from db.db module to interact with SQLite database.

    This implementation raises SQLite-specific exceptions. See method docstrings
    for details on specific exception types.
    """

    def write_feed_post(self, post: BlueskyFeedPost) -> None:
        """Write a feed post to SQLite.

        Args:
            post: BlueskyFeedPost model to write

        Raises:
            sqlite3.IntegrityError: If uri violates constraints
            sqlite3.OperationalError: If database operation fails
        """
        from db.db import write_feed_post

        write_feed_post(post)

    def write_feed_posts(self, posts: list[BlueskyFeedPost]) -> None:
        """Write multiple feed posts to SQLite (batch operation).

        Args:
            posts: List of BlueskyFeedPost models to write

        Raises:
            sqlite3.IntegrityError: If any uri violates constraints
            sqlite3.OperationalError: If database operation fails
        """
        from db.db import write_feed_posts

        write_feed_posts(posts)

    def read_feed_post(self, uri: str) -> BlueskyFeedPost:
        """Read a feed post from SQLite.

        Args:
            uri: Post URI to look up

        Returns:
            BlueskyFeedPost model if found.

        Raises:
            ValueError: If uri is empty or if no feed post is found for the given URI
            ValueError: If the feed post data is invalid (NULL fields)
            sqlite3.OperationalError: If database operation fails
            KeyError: If required columns are missing from the database row
        """
        from db.db import read_feed_post

        return read_feed_post(uri)

    def read_feed_posts_by_author(self, author_handle: str) -> list[BlueskyFeedPost]:
        """Read all feed posts by a specific author from SQLite.

        Args:
            author_handle: Author handle to filter by

        Returns:
            List of BlueskyFeedPost models for the author.

        Raises:
            ValueError: If any feed post data is invalid (NULL fields)
            sqlite3.OperationalError: If database operation fails
            KeyError: If required columns are missing from any database row
        """
        from db.db import read_feed_posts_by_author

        return read_feed_posts_by_author(author_handle)

    def read_all_feed_posts(self) -> list[BlueskyFeedPost]:
        """Read all feed posts from SQLite.

        Returns:
            List of BlueskyFeedPost models.

        Raises:
            ValueError: If any feed post data is invalid (NULL fields)
            sqlite3.OperationalError: If database operation fails
            KeyError: If required columns are missing from any database row
        """
        from db.db import read_all_feed_posts

        return read_all_feed_posts()

    def read_feed_posts_by_uris(self, uris: list[str]) -> list[BlueskyFeedPost]:
        """Read feed posts by URIs.

        Args:
            uris: List of post URIs to look up

        Returns:
            List of BlueskyFeedPost models for the given URIs.
            Returns empty list if no URIs provided or if no posts found.
            Missing URIs are silently skipped (only existing posts are returned).

        Raises:
            ValueError: If the feed post data is invalid (NULL fields)
            KeyError: If required columns are missing from the database row
            sqlite3.OperationalError: If database operation fails
        """
        with get_connection() as conn:
            if not uris:
                rows = []
            else:
                q_marks = ",".join("?" for _ in uris)
                sql = f"SELECT * FROM bluesky_feed_posts WHERE uri IN ({q_marks})"
                result_rows = conn.execute(sql, tuple(uris)).fetchall()
                # Validate all returned rows before filtering (catches data integrity issues)
                for row in result_rows:
                    context = f"feed posts for uri={row.get('uri', 'unknown')}"
                    _validate_feed_post_row(row, context=context)
                # Re-map rows by uri and restore input order
                row_by_uri = {row["uri"]: row for row in result_rows}
                rows = [row_by_uri[uri] for uri in uris if uri in row_by_uri]

            if len(rows) == 0:
                return []

            posts = []
            for row in rows:
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
