"""Abstraction for generated feed repositories."""

from abc import ABC, abstractmethod

from db.adapters.base import GeneratedFeedDatabaseAdapter
from db.models import GeneratedFeed


class GeneratedFeedRepository(ABC):
    """Abstract base class defining the interface for generated feed repositories."""
    
    @abstractmethod
    def create_or_update_generated_feed(self, feed: GeneratedFeed) -> GeneratedFeed:
        """Create or update a generated feed.
        
        Args:
            feed: GeneratedFeed model to create or update
            
        Returns:
            The created or updated GeneratedFeed object
        """
        raise NotImplementedError
    
    @abstractmethod
    def get_generated_feed(self, agent_handle: str, run_id: str, turn_number: int) -> GeneratedFeed:
        """Get a generated feed by composite key.
        
        Args:
            agent_handle: Agent handle to look up
            run_id: Run ID to look up
            turn_number: Turn number to look up
            
        Returns:
            GeneratedFeed model for the specified agent, run, and turn.
            
        Raises:
            ValueError: If no feed is found for the given composite key
        """
        raise NotImplementedError
    
    @abstractmethod
    def list_all_generated_feeds(self) -> list[GeneratedFeed]:
        """List all generated feeds.
        
        Returns:
            List of all GeneratedFeed models.
        """
        raise NotImplementedError


class SQLiteGeneratedFeedRepository(GeneratedFeedRepository):
    """SQLite implementation of GeneratedFeedRepository.
    
    Uses dependency injection to accept a database adapter,
    decoupling it from concrete implementations.
    """
    
    def __init__(self, db_adapter: GeneratedFeedDatabaseAdapter):
        """Initialize repository with injected dependencies.
        
        Args:
            db_adapter: Database adapter for generated feed operations
        """
        self._db_adapter = db_adapter
    
    def create_or_update_generated_feed(self, feed: GeneratedFeed) -> GeneratedFeed:
        """Create or update a generated feed in SQLite.
        
        Args:
            feed: GeneratedFeed model to create or update
            
        Returns:
            The created or updated GeneratedFeed object
            
        Raises:
            ValueError: If agent_handle, run_id, or turn_number is empty
            sqlite3.IntegrityError: If composite key violates constraints (from adapter)
            sqlite3.OperationalError: If database operation fails (from adapter)
        """
        if not feed.agent_handle or not feed.agent_handle.strip():
            raise ValueError("agent_handle cannot be empty")
        if not feed.run_id or not feed.run_id.strip():
            raise ValueError("run_id cannot be empty")
        if feed.turn_number is None:
            raise ValueError("turn_number cannot be None")
        
        self._db_adapter.write_generated_feed(feed)
        return feed
    
    def get_generated_feed(self, agent_handle: str, run_id: str, turn_number: int) -> GeneratedFeed:
        """Get a generated feed from SQLite.
        
        Args:
            agent_handle: Agent handle to look up
            run_id: Run ID to look up
            turn_number: Turn number to look up
            
        Returns:
            GeneratedFeed model for the specified agent, run, and turn.
            
        Raises:
            ValueError: If agent_handle, run_id, or turn_number is empty/None
            ValueError: If no feed is found for the given composite key (from adapter)
        """
        if not agent_handle or not agent_handle.strip():
            raise ValueError("agent_handle cannot be empty")
        if not run_id or not run_id.strip():
            raise ValueError("run_id cannot be empty")
        if turn_number is None:
            raise ValueError("turn_number cannot be None")
        
        return self._db_adapter.read_generated_feed(agent_handle, run_id, turn_number)
    
    def list_all_generated_feeds(self) -> list[GeneratedFeed]:
        """List all generated feeds from SQLite.
        
        Returns:
            List of all GeneratedFeed models.
        """
        return self._db_adapter.read_all_generated_feeds()


def create_sqlite_generated_feed_repository() -> SQLiteGeneratedFeedRepository:
    """Factory function to create a SQLiteGeneratedFeedRepository with default dependencies.
    
    Returns:
        SQLiteGeneratedFeedRepository configured with SQLite adapter
    """
    from db.adapters.sqlite import SQLiteGeneratedFeedAdapter
    return SQLiteGeneratedFeedRepository(
        db_adapter=SQLiteGeneratedFeedAdapter()
    )

