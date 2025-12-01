"""SQLite implementation of generated feed database adapter."""

import json

from db.adapters.base import GeneratedFeedDatabaseAdapter
from db.db import _validate_generated_feed_row, get_connection
from simulation.core.models.feeds import GeneratedFeed


class SQLiteGeneratedFeedAdapter(GeneratedFeedDatabaseAdapter):
    """SQLite implementation of GeneratedFeedDatabaseAdapter.

    Uses functions from db.db module to interact with SQLite database.

    This implementation raises SQLite-specific exceptions. See method docstrings
    for details on specific exception types.
    """

    def write_generated_feed(self, feed: GeneratedFeed) -> None:
        """Write a generated feed to SQLite.

        Args:
            feed: GeneratedFeed model to write

        Raises:
            sqlite3.IntegrityError: If composite key violates constraints
            sqlite3.OperationalError: If database operation fails
        """
        from db.db import write_generated_feed

        write_generated_feed(feed)

    def read_generated_feed(
        self, agent_handle: str, run_id: str, turn_number: int
    ) -> GeneratedFeed:
        """Read a generated feed from SQLite.

        Args:
            agent_handle: Agent handle to look up
            run_id: Run ID to look up
            turn_number: Turn number to look up

        Returns:
            GeneratedFeed model for the specified agent, run, and turn.

        Raises:
            ValueError: If no feed is found for the given composite key
            ValueError: If the feed data is invalid (NULL fields)
            sqlite3.OperationalError: If database operation fails
            KeyError: If required columns are missing from the database row
        """
        from db.db import read_generated_feed

        return read_generated_feed(agent_handle, run_id, turn_number)

    def read_all_generated_feeds(self) -> list[GeneratedFeed]:
        """Read all generated feeds from SQLite.

        Returns:
            List of GeneratedFeed models.

        Raises:
            ValueError: If any feed data is invalid (NULL fields)
            sqlite3.OperationalError: If database operation fails
            KeyError: If required columns are missing from any database row
        """
        from db.db import read_all_generated_feeds

        return read_all_generated_feeds()

    def read_post_uris_for_run(self, agent_handle: str, run_id: str) -> set[str]:
        """Read all post URIs from generated feeds for a specific agent and run.

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
        from db.db import read_post_uris_for_run

        return read_post_uris_for_run(agent_handle, run_id)

    def read_feeds_for_turn(self, run_id: str, turn_number: int) -> list[GeneratedFeed]:
        """Read all generated feeds for a specific run and turn.

        Args:
            run_id: The ID of the run
            turn_number: The turn number (0-indexed)

        Returns:
            List of GeneratedFeed models for the specified run and turn.
            Returns empty list if no feeds found.
        
        Raises:
            ValueError: If the feed data is invalid (NULL fields, invalid JSON)
            KeyError: If required columns are missing from the database row
            sqlite3.OperationalError: If database operation fails
        """
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM generated_feeds WHERE run_id = ? AND turn_number = ?",
                (run_id, turn_number),
            ).fetchall()

            if len(rows) == 0:
                return []

            # Validate required fields are not NULL
            context = f"generated feeds for run {run_id}, turn {turn_number}"
            for row in rows:
                _validate_generated_feed_row(row, context=context)

            feeds = []
            for row in rows:
                feeds.append(GeneratedFeed(
                    feed_id=row["feed_id"],
                    run_id=row["run_id"],
                    turn_number=row["turn_number"],
                    agent_handle=row["agent_handle"],
                    post_uris=json.loads(row["post_uris"]),
                    created_at=row["created_at"],
                ))
            return feeds
