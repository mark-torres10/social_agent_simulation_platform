"""Class to manage memories."""

import aiosqlite3
import json
import os
import sqlite3
from typing import Iterable, Optional

from pydantic import BaseModel

from agent.agent import Agent
from lib.helper import get_current_timestamp_str


# Current directory + tmp/
current_dir = os.path.dirname(os.path.abspath(__file__))
current_timestamp_str = get_current_timestamp_str()
TMP_DATA_PATH = os.path.join(current_dir, "tmp", current_timestamp_str)

DEFAULT_BATCH_CHUNK_SIZE = 1000
DEFAULT_BATCH_WRITE_SIZE = 25


class MemoryItem(BaseModel):
    """A single memory item."""

    id: int
    agent_id: str
    value: str
    turn_number: int
    timestamp: str
    metadata: str


class MemoryManager:
    """Manages all the memories for a given memory type."""

    def __init__(self, memory_type: str, create_new_queue: bool = True):
        self.db_name = f"{memory_type}.db"
        self.db_path = os.path.join(TMP_DATA_PATH, self.db_name)
        if os.path.exists(self.db_path) and create_new_queue:
            print(
                f"DB for memory type {memory_type} already exists. Not overwriting, using existing DB..."
            )
        if not os.path.exists(self.db_path):
            if create_new_queue:
                print(f"Creating new SQLite DB for memory type {memory_type}...")
                self._init_queue_db()
            else:
                raise ValueError(
                    f"DB for memory type {memory_type} doesn't exist. Need to pass in `create_new_queue` if creating a new queue is intended."
                )
        else:
            print(f"Loading existing SQLite DB for memory type {memory_type}...")
            count = self.get_queue_length()
            print(f"Current queue size: {count} items")

        self.table_name = f"{memory_type}_table"

    def __repr__(self):
        return f"MemoryManager(name={self.db_name}, db_path={self.db_path})"

    def __str__(self):
        return f"MemoryManager(name={self.db_name}, db_path={self.db_path})"

    def _init_queue_db(self):
        """Initialize queue database with WAL mode and optimized settings."""
        with sqlite3.connect(self.db_path, timeout=30.0) as conn:
            # Enable WAL mode before creating tables
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
            conn.execute("PRAGMA busy_timeout=30000")  # 30 second timeout
            conn.execute("PRAGMA cache_size=-64000")  # 64MB cache
            conn.execute("PRAGMA mmap_size=268435456")  # 256MB memory mapped I/O
            conn.execute("PRAGMA page_size=8192")  # Double the current size

            # Add compression if you're using SQLite 3.38.0 or later
            try:
                conn.execute("PRAGMA journal_mode=WAL")
                conn.execute("PRAGMA zip_compression=true")  # Enable compression
            except sqlite3.OperationalError:
                # Older SQLite version, compression not available
                pass

            # Create the main table with an additional column for the primary key
            conn.execute(f"""
                CREATE TABLE {self.table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_id TEXT,
                    value TEXT,
                    turn_number INTEGER,
                    timestamp TEXT,
                    metadata TEXT
                )
            """)

            # Ensure WAL mode is persisted
            conn.execute("PRAGMA journal_mode=WAL")
            conn.commit()

    def _get_connection(self) -> sqlite3.Connection:
        """Get an optimized SQLite connection with retry logic."""
        conn = sqlite3.connect(self.db_path, timeout=30.0)

        # Configure connection for optimal performance
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.execute("PRAGMA busy_timeout=30000")
        conn.execute("PRAGMA cache_size=-64000")
        conn.execute("PRAGMA mmap_size=268435456")
        conn.execute("PRAGMA temp_store=MEMORY")

        return conn

    async def _async_get_connection(self) -> sqlite3.Connection:
        """Get an optimized SQLite connection with retry logic."""
        conn = await aiosqlite3.connect(self.db_path)

        # Configure connection for optimal performance
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.execute("PRAGMA busy_timeout=30000")
        conn.execute("PRAGMA cache_size=-64000")
        conn.execute("PRAGMA mmap_size=268435456")
        conn.execute("PRAGMA temp_store=MEMORY")

        return conn

    def get_queue_length(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(f"SELECT COUNT(*) FROM {self.db_name}")
            return cursor.fetchone()[0]

    def batch_add_items_to_db(
        self,
        items: list[dict],
        metadata: Optional[dict] = None,
        batch_size: Optional[int] = DEFAULT_BATCH_CHUNK_SIZE,
    ) -> None:
        """Add multiple items to queue, processing in chunks for memory
        efficiency.
        See https://markptorres.com/research/2025-01-31-effectiveness-of-sqlite
        for writeup.
        """
        if metadata is None:
            metadata = {}
        chunks: list[list[dict]] = [
            items[i : i + batch_size] for i in range(0, len(items), batch_size)
        ]
        total_chunks = len(chunks)
        for i, chunk in enumerate(chunks):
            if i % 10 == 0:
                print(f"Processing batch {i + 1}/{total_chunks}...")
            chunk = [{**item, **{"metadata": metadata}} for item in chunk]
            with sqlite3.connect(self.db_path) as conn:
                conn.executemany(
                    f"""
                    INSERT INTO {self.db_name} (agent_id, value, turn_number, timestamp)
                    VALUES (?, ?, ?, ?)
                    """,
                    chunk,
                )
            conn.commit()

    def batch_delete_items_by_ids(self, ids: Iterable[str]) -> int:
        """Delete multiple items from queue by their ids.

        Args:
            ids: List of queue item IDs to delete

        Returns:
            int: Number of items actually deleted
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                f"DELETE FROM {self.table_name} WHERE id IN ({','.join(map(str, ids))})"
            )
            deleted_count = cursor.rowcount
            print(f"Deleted {deleted_count} items from queue.")
            return deleted_count

    def load_items_from_queue(
        self,
        limit: Optional[int] = None,
        min_turn_number: Optional[int] = None,
        max_turn_number: Optional[int] = None,
        min_id: Optional[int] = None,
        min_timestamp: Optional[str] = None,
    ) -> list[MemoryItem]:
        """Load multiple items from queue.

        Supports a variety of filters:
        - status: filter by status
        - min_id: filter to grab all rows whose autoincremented id is greater
        than the provided id. Strictly greater than.
        - min_timestamp: filter to grab all rows whose created_at is greater
        than the provided timestamp. Strictly greater than.

        When "limit" is provided, it will return the first "limit" number of items
        that match the filters.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            query = "SELECT id, agent_id, value, turn_number, timestamp, metadata FROM queue"
            conditions = []
            params = []

            if min_id:
                conditions.append("id > ?")
                params.append(min_id)

            if min_timestamp:
                conditions.append("timestamp > ?")
                params.append(min_timestamp)

            if min_turn_number:
                conditions.append("turn_number > ?")
                params.append(min_turn_number)

            if max_turn_number:
                conditions.append("turn_number < ?")
                params.append(max_turn_number)

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            if limit:
                query += " LIMIT ?"
                params.append(limit)

            cursor.execute(query, params)
            rows = cursor.fetchall()

            items = []
            for row in rows:
                item = MemoryItem(
                    id=row[0],
                    agent_id=row[1],
                    value=row[2],
                    turn_number=row[3],
                    timestamp=row[4],
                    metadata=row[5],
                )
                items.append(item)

            return items

    def get_latest_memories(self, agent_id: str, memory_type: str):
        """Get the latest memories for a given agent and memory type."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                f"SELECT * FROM {self.table_name} WHERE agent_id = ? AND memory_type = ? ORDER BY timestamp DESC LIMIT 1",
                (agent_id, memory_type),
            )
            return cursor.fetchone()


class GlobalMemoryManager:
    """Global memory manager, manages memories across all agents and all
    memory types.

    It's easier to save all memories of the same type (e.g., "beliefs") in the
    same storage/partitioning format, so we'll load all of them into memory,
    one by one, and split them across all the agents.
    """

    def __init__(self):
        self.created_at_timestamp: str = get_current_timestamp_str()

    def init_memory_managers(self, agents: list[Agent]):
        """Initialize the SQLite-based memory managers for the given session."""
        profile_manager = MemoryManager(memory_type="profile")
        history_manager = MemoryManager(memory_type="history")

        profiles = []
        histories = []

        # iterate through all the agents and unpack their information.
        for agent in agents:
            # get their profile
            profile = agent.profile.get_profile()

            # get their history.
            history = agent.profile.history.get_history()

            profiles.append(
                {
                    "agent_id": agent.agent_id,
                    "value": profile,
                    "turn_number": 0,
                    "timestamp": get_current_timestamp_str(),
                    "metadata": json.dumps({"type": "profile"}),
                }
            )
            histories.append(
                {
                    "agent_id": agent.agent_id,
                    "value": history,
                    "turn_number": 0,
                    "timestamp": get_current_timestamp_str(),
                    "metadata": json.dumps({"type": "history"}),
                }
            )

        profile_manager.batch_add_items_to_db(profiles)
        history_manager.batch_add_items_to_db(histories)

    def update_global_memory_manager(self, agents: list[Agent]):
        """Updates the global memory manager with the latest memories and
        histories from the given agents."""
        print(f"Updating global memory manager with {len(agents)} agents...")
        pass
