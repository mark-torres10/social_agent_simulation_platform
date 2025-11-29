"""SQLite implementation of profile database adapter."""

from typing import Optional

from db.adapters.base import ProfileDatabaseAdapter
from db.models import BlueskyProfile


class SQLiteProfileAdapter(ProfileDatabaseAdapter):
    """SQLite implementation of ProfileDatabaseAdapter.
    
    Uses functions from db.db module to interact with SQLite database.
    
    This implementation raises SQLite-specific exceptions. See method docstrings
    for details on specific exception types.
    """
    
    def write_profile(self, profile: BlueskyProfile) -> None:
        """Write a profile to SQLite.
        
        Args:
            profile: BlueskyProfile model to write
        
        Raises:
            sqlite3.IntegrityError: If handle violates constraints
            sqlite3.OperationalError: If database operation fails
        """
        from db.db import write_profile
        write_profile(profile)
    
    def read_profile(self, handle: str) -> Optional[BlueskyProfile]:
        """Read a profile from SQLite.
        
        Args:
            handle: Profile handle to look up
            
        Returns:
            BlueskyProfile if found, None otherwise.
        
        Raises:
            ValueError: If the profile data is invalid (NULL fields)
            sqlite3.OperationalError: If database operation fails
            KeyError: If required columns are missing from the database row
        """
        from db.db import read_profile
        return read_profile(handle)
    
    def read_all_profiles(self) -> list[BlueskyProfile]:
        """Read all profiles from SQLite.
        
        Returns:
            List of BlueskyProfile models.
        
        Raises:
            ValueError: If any profile data is invalid (NULL fields)
            sqlite3.OperationalError: If database operation fails
            KeyError: If required columns are missing from any database row
        """
        from db.db import read_all_profiles
        return read_all_profiles()

