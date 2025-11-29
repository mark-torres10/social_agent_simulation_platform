"""Abstraction for profile repositories."""

from abc import ABC, abstractmethod
from typing import Optional

from db.adapters.base import ProfileDatabaseAdapter
from db.models import BlueskyProfile


class ProfileRepository(ABC):
    """Abstract base class defining the interface for profile repositories."""
    
    @abstractmethod
    def create_or_update_profile(self, profile: BlueskyProfile) -> BlueskyProfile:
        """Create or update a profile.
        
        Args:
            profile: BlueskyProfile model to create or update
            
        Returns:
            The created or updated BlueskyProfile object
        """
        raise NotImplementedError
    
    @abstractmethod
    def get_profile(self, handle: str) -> Optional[BlueskyProfile]:
        """Get a profile by handle.
        
        Args:
            handle: Profile handle to look up
            
        Returns:
            BlueskyProfile model if found, None otherwise.
        """
        raise NotImplementedError
    
    @abstractmethod
    def list_profiles(self) -> list[BlueskyProfile]:
        """List all profiles.
        
        Returns:
            List of all BlueskyProfile models.
        """
        raise NotImplementedError


class SQLiteProfileRepository(ProfileRepository):
    """SQLite implementation of ProfileRepository.
    
    Uses dependency injection to accept a database adapter,
    decoupling it from concrete implementations.
    """
    
    def __init__(self, db_adapter: ProfileDatabaseAdapter):
        """Initialize repository with injected dependencies.
        
        Args:
            db_adapter: Database adapter for profile operations
        """
        self._db_adapter = db_adapter
    
    def create_or_update_profile(self, profile: BlueskyProfile) -> BlueskyProfile:
        """Create or update a profile in SQLite.
        
        Args:
            profile: BlueskyProfile model to create or update
            
        Returns:
            The created or updated BlueskyProfile object
            
        Raises:
            ValueError: If profile.handle is empty
            RuntimeError: If the profile cannot be created/updated due to a database error
        """
        if not profile.handle or not profile.handle.strip():
            raise ValueError("profile.handle cannot be empty")
        
        try:
            self._db_adapter.write_profile(profile)
        except Exception as e:
            raise RuntimeError(
                f"Failed to create/update profile '{profile.handle}': {e}"
            ) from e
        return profile
    
    def get_profile(self, handle: str) -> Optional[BlueskyProfile]:
        """Get a profile from SQLite.
        
        Args:
            handle: Unique identifier for the profile
            
        Returns:
            BlueskyProfile model if found, None otherwise.
            
        Raises:
            ValueError: If handle is empty or None
        """
        if not handle or not handle.strip():
            raise ValueError("handle cannot be empty")
        return self._db_adapter.read_profile(handle)
    
    def list_profiles(self) -> list[BlueskyProfile]:
        """List all profiles from SQLite.
        
        Returns:
            List of all BlueskyProfile models.
        """
        return self._db_adapter.read_all_profiles()


def create_sqlite_profile_repository() -> SQLiteProfileRepository:
    """Factory function to create a SQLiteProfileRepository with default dependencies.
    
    Returns:
        SQLiteProfileRepository configured with SQLite adapter
    """
    from db.adapters.sqlite import SQLiteProfileAdapter
    return SQLiteProfileRepository(
        db_adapter=SQLiteProfileAdapter()
    )

