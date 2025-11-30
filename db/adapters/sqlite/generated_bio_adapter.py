"""SQLite implementation of generated bio database adapter."""

from typing import Optional

from db.adapters.base import GeneratedBioDatabaseAdapter
from db.models import GeneratedBio


class SQLiteGeneratedBioAdapter(GeneratedBioDatabaseAdapter):
    """SQLite implementation of GeneratedBioDatabaseAdapter.
    
    Uses functions from db.db module to interact with SQLite database.
    
    This implementation raises SQLite-specific exceptions. See method docstrings
    for details on specific exception types.
    """
    
    def write_generated_bio(self, bio: GeneratedBio) -> None:
        """Write a generated bio to SQLite.
        
        Args:
            bio: GeneratedBio model to write
        
        Raises:
            sqlite3.IntegrityError: If handle violates constraints
            sqlite3.OperationalError: If database operation fails
        """
        from db.db import write_generated_bio_to_database
        write_generated_bio_to_database(bio.handle, bio.generated_bio)
    
    def read_generated_bio(self, handle: str) -> Optional[GeneratedBio]:
        """Read a generated bio from SQLite.
        
        Args:
            handle: Profile handle to look up
            
        Returns:
            GeneratedBio if found, None otherwise.
        
        Raises:
            ValueError: If the bio data is invalid (NULL fields)
            sqlite3.OperationalError: If database operation fails
            KeyError: If required columns are missing from the database row
        """
        from db.db import read_generated_bio
        return read_generated_bio(handle)
    
    def read_all_generated_bios(self) -> list[GeneratedBio]:
        """Read all generated bios from SQLite.
        
        Returns:
            List of GeneratedBio models.
        
        Raises:
            ValueError: If any bio data is invalid (NULL fields)
            sqlite3.OperationalError: If database operation fails
            KeyError: If required columns are missing from any database row
        """
        from db.db import read_all_generated_bios
        return read_all_generated_bios()

