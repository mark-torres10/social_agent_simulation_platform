"""Base adapter interfaces."""

from abc import ABC, abstractmethod
from typing import Optional

from db.models import BlueskyFeedPost, BlueskyProfile, GeneratedFeed, Run


class RunDatabaseAdapter(ABC):
    """Abstract interface for run database operations.
    
    This interface is database-agnostic. Concrete implementations should document
    the specific exceptions they raise, which may be database-specific.
    """
    
    @abstractmethod
    def write_run(self, run: Run) -> None:
        """Write a run to the database.
        
        Args:
            run: Run model to write
            
        Raises:
            Exception: Database-specific exception if constraints are violated or
                      the operation fails. Implementations should document the
                      specific exception types they raise.
        """
        raise NotImplementedError
    
    @abstractmethod
    def read_run(self, run_id: str) -> Optional[Run]:
        """Read a run by ID.
        
        Args:
            run_id: Unique identifier for the run
            
        Returns:
            Run model if found, None otherwise
            
        Raises:
            ValueError: If the run data is invalid (NULL fields, invalid status)
            KeyError: If required columns are missing from the database row
            Exception: Database-specific exception if the operation fails.
                      Implementations should document the specific exception types
                      they raise.
        """
        raise NotImplementedError
    
    @abstractmethod
    def read_all_runs(self) -> list[Run]:
        """Read all runs.
        
        Returns:
            List of Run models, ordered by created_at descending (newest first).
            Returns empty list if no runs exist.
            
        Raises:
            ValueError: If any run data is invalid (NULL fields, invalid status)
            KeyError: If required columns are missing from any database row
            Exception: Database-specific exception if the operation fails.
                      Implementations should document the specific exception types
                      they raise.
        """
        raise NotImplementedError
    
    @abstractmethod
    def update_run_status(self, run_id: str, status: str, completed_at: Optional[str] = None) -> None:
        """Update a run's status.
        
        Args:
            run_id: Unique identifier for the run to update
            status: New status value (should be a valid RunStatus enum value as string)
            completed_at: Optional timestamp when the run was completed.
                         Should be set when status is 'completed', None otherwise.
        
        Raises:
            RunNotFoundError: If no run exists with the given run_id
            Exception: Database-specific exception if constraints are violated or
                      the operation fails. Implementations should document the
                      specific exception types they raise.
        """
        raise NotImplementedError


class ProfileDatabaseAdapter(ABC):
    """Abstract interface for profile database operations.
    
    This interface is database-agnostic. Currently works with BlueskyProfile.
    Concrete implementations should document the specific exceptions they raise,
    which may be database-specific.
    """
    
    @abstractmethod
    def write_profile(self, profile: BlueskyProfile) -> None:
        """Write a profile to the database.
        
        Args:
            profile: BlueskyProfile model to write
            
        Raises:
            Exception: Database-specific exception if constraints are violated or
                      the operation fails. Implementations should document the
                      specific exception types they raise.
        """
        raise NotImplementedError
    
    @abstractmethod
    def read_profile(self, handle: str) -> Optional[BlueskyProfile]:
        """Read a profile by handle.
        
        Args:
            handle: Profile handle to look up
            
        Returns:
            BlueskyProfile model if found, None otherwise.
            
        Raises:
            ValueError: If the profile data is invalid (NULL fields)
            KeyError: If required columns are missing from the database row
            Exception: Database-specific exception if the operation fails.
                      Implementations should document the specific exception types
                      they raise.
        """
        raise NotImplementedError
    
    @abstractmethod
    def read_all_profiles(self) -> list[BlueskyProfile]:
        """Read all profiles.
        
        Returns:
            List of BlueskyProfile models. Returns empty list if no profiles exist.
            
        Raises:
            ValueError: If any profile data is invalid (NULL fields)
            KeyError: If required columns are missing from any database row
            Exception: Database-specific exception if the operation fails.
                      Implementations should document the specific exception types
                      they raise.
        """
        raise NotImplementedError


class FeedPostDatabaseAdapter(ABC):
    """Abstract interface for feed post database operations.
    
    This interface is database-agnostic. Currently works with BlueskyFeedPost.
    Concrete implementations should document the specific exceptions they raise,
    which may be database-specific.
    """
    
    @abstractmethod
    def write_feed_post(self, post: BlueskyFeedPost) -> None:
        """Write a feed post to the database.
        
        Args:
            post: BlueskyFeedPost model to write
            
        Raises:
            Exception: Database-specific exception if constraints are violated or
                      the operation fails. Implementations should document the
                      specific exception types they raise.
        """
        raise NotImplementedError
    
    @abstractmethod
    def write_feed_posts(self, posts: list[BlueskyFeedPost]) -> None:
        """Write multiple feed posts to the database (batch operation).
        
        Args:
            posts: List of BlueskyFeedPost models to write
            
        Raises:
            Exception: Database-specific exception if constraints are violated or
                      the operation fails. Implementations should document the
                      specific exception types they raise.
        """
        raise NotImplementedError
    
    @abstractmethod
    def read_feed_post(self, uri: str) -> Optional[BlueskyFeedPost]:
        """Read a feed post by URI.
        
        Args:
            uri: Post URI to look up
            
        Returns:
            BlueskyFeedPost model if found, None otherwise.
            
        Raises:
            ValueError: If the feed post data is invalid (NULL fields)
            KeyError: If required columns are missing from the database row
            Exception: Database-specific exception if the operation fails.
                      Implementations should document the specific exception types
                      they raise.
        """
        raise NotImplementedError
    
    @abstractmethod
    def read_feed_posts_by_author(self, author_handle: str) -> list[BlueskyFeedPost]:
        """Read all feed posts by a specific author.
        
        Args:
            author_handle: Author handle to filter by
            
        Returns:
            List of BlueskyFeedPost models for the author.
            
        Raises:
            ValueError: If any feed post data is invalid (NULL fields)
            KeyError: If required columns are missing from any database row
            Exception: Database-specific exception if the operation fails.
                      Implementations should document the specific exception types
                      they raise.
        """
        raise NotImplementedError
    
    @abstractmethod
    def read_all_feed_posts(self) -> list[BlueskyFeedPost]:
        """Read all feed posts.
        
        Returns:
            List of all BlueskyFeedPost models. Returns empty list if no posts exist.
            
        Raises:
            ValueError: If any feed post data is invalid (NULL fields)
            KeyError: If required columns are missing from any database row
            Exception: Database-specific exception if the operation fails.
                      Implementations should document the specific exception types
                      they raise.
        """
        raise NotImplementedError


class GeneratedFeedDatabaseAdapter(ABC):
    """Abstract interface for generated feed database operations.
    
    This interface is database-agnostic. Currently works with GeneratedFeed.
    Concrete implementations should document the specific exceptions they raise,
    which may be database-specific.
    """
    
    @abstractmethod
    def write_generated_feed(self, feed: GeneratedFeed) -> None:
        """Write a generated feed to the database.
        
        Args:
            feed: GeneratedFeed model to write
            
        Raises:
            Exception: Database-specific exception if constraints are violated or
                      the operation fails. Implementations should document the
                      specific exception types they raise.
        """
        raise NotImplementedError
    
    @abstractmethod
    def read_generated_feed(self, agent_handle: str, run_id: str, turn_number: int) -> GeneratedFeed:
        """Read a generated feed by composite key.
        
        Args:
            agent_handle: Agent handle to look up
            run_id: Run ID to look up
            turn_number: Turn number to look up
            
        Returns:
            GeneratedFeed model for the specified agent, run, and turn.
            
        Raises:
            ValueError: If no feed is found for the given composite key
            ValueError: If the feed data is invalid (NULL fields)
            KeyError: If required columns are missing from the database row
            Exception: Database-specific exception if the operation fails.
                      Implementations should document the specific exception types
                      they raise.
        """
        raise NotImplementedError
    
    @abstractmethod
    def read_all_generated_feeds(self) -> list[GeneratedFeed]:
        """Read all generated feeds.
        
        Returns:
            List of all GeneratedFeed models. Returns empty list if no feeds exist.
            
        Raises:
            ValueError: If any feed data is invalid (NULL fields)
            KeyError: If required columns are missing from any database row
            Exception: Database-specific exception if the operation fails.
                      Implementations should document the specific exception types
                      they raise.
        """
        raise NotImplementedError

