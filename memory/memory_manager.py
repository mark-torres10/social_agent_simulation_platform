"""Class to manage memories."""

import os
import sqlite3
from typing import Optional

from agent.models import UserAgent
from lib.helper import get_current_timestamp_str
from memory.models import Memory

MEMORY_TYPES = [
    "profile",
    "personality",
    "beliefs",
    "worldview",
    "political_views",
    "engagement_preferences",
    "history",
]

# Current directory + tmp/
TMP_DATA_PATH = ""

DEFAULT_BATCH_CHUNK_SIZE = 1000
DEFAULT_BATCH_WRITE_SIZE = 25


class MemoryManager:
    """Manages all the memories for a given memory type."""

    def __init__(self, memory_type: str):
        self.db_name = f"{memory_type}.db"
        self.db_path = os.path.join(TMP_DATA_PATH, self.db_name)
        self._init_memory_manager_db()

    def _init_memory_manager_db(self, init_memories: list[dict]):
        """Initialize the memory manager with the first memories from
        initializing the agents."""
        self.batch_add_items_to_db(init_memories)

    def add_item_to_db():
        pass

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
                    INSERT INTO {self.db_name} (user_id, values)
                    VALUES (?, ?)
                    """,
                    chunk,
                )
            conn.commit()

    def load_memory(storage_type: str) -> Memory:
        pass

    def load_memories():
        pass

    def save_memory(memory: Memory, type: str):
        pass

    def save_memories(memories: list[Memory], type: str):
        pass


class AgentMemoryManager:
    """Manages all the memories for a given agent, across all types."""

    pass


class GlobalMemoryManager:
    """Global memory manager, manages memories across all agents and all
    memory types.

    It's easier to save all memories of the same type (e.g., "beliefs") in the
    same storage/partitioning format, so we'll load all of them into memory,
    one by one, and split them across all the agents.
    """

    def __init__(self):
        self.created_at_timestamp: str = get_current_timestamp_str()

    def init_memory_managers(self, agents: list[UserAgent]):
        """Initialize the SQLite-based memory managers for the given session."""
        memory_type_to_manager_map: dict[str, MemoryManager] = {}
        memory_type_to_agent_memories_map: dict[str, list] = {}

        # iterate through all the agents and unpack their information.
        for agent in agents:
            for memory_type in MEMORY_TYPES:
                if memory_type not in memory_type_to_agent_memories_map:
                    memory_type_to_agent_memories_map[memory_type] = []
                memory_type_to_agent_memories_map[memory_type].append(
                    {"user_id": agent.user_id, "value": agent.getattr(memory_type)}
                )

        # init DBs based on each of these agent types.
        for memory_type in MEMORY_TYPES:
            memory_manager = MemoryManager(memory_type=memory_type)
            memory_manager._init_memory_manager_db(
                init_memories=memory_type_to_agent_memories_map[memory_type]
            )
            memory_type_to_manager_map[memory_type] = memory_manager

        print("Completed initializing memory managers for all memory types.")

        self.memory_type_to_manager_map: dict[str, MemoryManager] = (
            memory_type_to_manager_map
        )
