"""SQLite implementation of generated feed database adapter."""

from db.adapters.base import GeneratedFeedDatabaseAdapter
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
