from __future__ import annotations
from dataclasses import dataclass
from typing import Any, List, Optional, Iterable
from datetime import datetime

@dataclass
class Record:
    mode: str  # "Product" or "Item"
    id: int
    name: str
    price: Optional[float] = None   # para sa Product
    description: Optional[str] = None  # para sa Item
    key: Optional[int] = None  # Hidden from UI, used internally
    hash_index: Optional[int] = None  # Slot index after probing
    inserted_at: Optional[int] = None  # Insertion order counter

class HashTable:
    """
    Hash table with linear probing for collision resolution.
    h(k) = k mod m
    When collision occurs, probe forward: (h(k) + i) mod m
    """
    def __init__(self, initial_capacity: int = 11, max_load_factor: float = 0.75) -> None:
        self._capacity = self._next_prime(max(11, initial_capacity))
        self._buckets: List[Optional[Record]] = [None] * self._capacity
        self._size = 0  # Number of occupied slots
        self._max_load = max_load_factor
        self._insert_counter = 0  # Track insertion order

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def size(self) -> int:
        """Returns the number of occupied slots in the hashtable."""
        return self._size

    @property
    def load_factor(self) -> float:
        return self._size / self._capacity if self._capacity else 0.0

    def _hash(self, k: int) -> int:
        """Compute initial hash index."""
        return k % self._capacity

    def _find_slot(self, key: int, for_insertion: bool = False) -> Optional[int]:
        """
        Find the slot for a given key using linear probing.
        
        Args:
            key: The key to search for
            for_insertion: If True, return first available slot (None or matching key)
                          If False, return slot only if key matches
        
        Returns:
            Slot index if found, None otherwise
        """
        initial_idx = self._hash(key)
        idx = initial_idx
        probes = 0
        
        while probes < self._capacity:
            current_record = self._buckets[idx]
            
            if current_record is None:
                # Empty slot found
                return idx if for_insertion else None
            
            if current_record.id == key:
                # Key found
                return idx
            
            # Collision: probe forward
            idx = (idx + 1) % self._capacity
            probes += 1
        
        # Table is full or key not found
        return None if not for_insertion else None

    def insert(self, key: int, record: Record) -> None:
        """
        Insert a record using linear probing.
        If key exists, update the record.
        If collision occurs, probe forward to next available slot.
        """
        if key is None:
            raise ValueError("Key must not be None")
        
        # Check if we need to resize
        if self.load_factor >= self._max_load:
            self._resize(self._next_prime(self._capacity * 2))
        
        # Find slot for insertion
        idx = self._find_slot(key, for_insertion=True)
        
        if idx is None:
            raise RuntimeError("Hash table is full - cannot insert")
        
        # Check if this is an update or new insertion
        is_update = self._buckets[idx] is not None and self._buckets[idx].id == key
        
        # Update record metadata
        record.key = key
        record.hash_index = idx
        self._insert_counter += 1
        record.inserted_at = self._insert_counter
        
        # Insert/update the record
        self._buckets[idx] = record
        
        # Increment size only for new insertions
        if not is_update:
            self._size += 1

    def get(self, key: int) -> Optional[Record]:
        """Retrieve a record by key using linear probing."""
        idx = self._find_slot(key, for_insertion=False)
        return self._buckets[idx] if idx is not None else None

    def remove(self, key: int) -> bool:
        """
        Remove a record by key.
        After removal, rehash subsequent entries to maintain probe chain integrity.
        """
        idx = self._find_slot(key, for_insertion=False)
        
        if idx is None:
            return False
        
        # Mark slot as deleted
        self._buckets[idx] = None
        self._size -= 1
        
        # Rehash subsequent entries in the probe chain
        next_idx = (idx + 1) % self._capacity
        while self._buckets[next_idx] is not None:
            # Re-insert this record to fix probe chain
            record_to_reinsert = self._buckets[next_idx]
            self._buckets[next_idx] = None
            self._size -= 1
            
            # Re-insert (will find correct position)
            self.insert(record_to_reinsert.id, record_to_reinsert)
            
            next_idx = (next_idx + 1) % self._capacity
        
        return True

    def search_by_id(self, id_val: int) -> Optional[Record]:
        """Search for a record by ID (same as get)."""
        return self.get(id_val)

    def search_by_name(self, name: str) -> List[Record]:
        """
        Search for records by name (case-insensitive partial match).
        Returns all matching records.
        """
        name_lower = name.lower()
        results = []
        
        for record in self._buckets:
            if record is not None and name_lower in record.name.lower():
                results.append(record)
        
        return results

    def search_by_hash(self, hash_number: int) -> List[Record]:
        """
        Search for all records at a specific hash index.
        This includes records that may have been probed to adjacent slots
        but originally hashed to this index.
        """
        results = []
        
        for record in self._buckets:
            if record is not None:
                # Calculate the original hash for this record's key
                original_hash = self._hash(record.id)
                if original_hash == hash_number:
                    results.append(record)
        
        return results

    def get_hashtable_size(self) -> int:
        """Return the number of occupied slots."""
        return self._size

    def items(self) -> Iterable[Record]:
        """Iterate over all records in the table."""
        for record in self._buckets:
            if record is not None:
                yield record

    def clear(self) -> None:
        """Clear all records from the table."""
        self._buckets = [None] * self._capacity
        self._size = 0
        self._insert_counter = 0

    def _resize(self, new_capacity: int) -> None:
        """Resize the hash table and rehash all existing records."""
        old_items = list(self.items())
        self._capacity = new_capacity
        self._buckets = [None] * self._capacity
        self._size = 0
        # Keep insert counter to maintain ordering
        
        for rec in old_items:
            self.insert(rec.id, rec)

    @staticmethod
    def _next_prime(n: int) -> int:
        """Find the next prime number >= n."""
        def is_prime(x: int) -> bool:
            if x < 2:
                return False
            if x % 2 == 0:
                return x == 2
            i = 3
            while i * i <= x:
                if x % i == 0:
                    return False
                i += 2
            return True
        
        candidate = n if n % 2 else n + 1
        while not is_prime(candidate):
            candidate += 2
        return candidate

    def get_table_state(self) -> List[dict]:
        """
        Get a detailed view of the hash table state for debugging.
        Returns information about each slot including empty slots.
        """
        state = []
        for idx, record in enumerate(self._buckets):
            if record is None:
                state.append({
                    "slot": idx,
                    "status": "empty",
                    "record": None
                })
            else:
                original_hash = self._hash(record.id)
                state.append({
                    "slot": idx,
                    "status": "occupied",
                    "record": {
                        "id": record.id,
                        "name": record.name,
                        "original_hash": original_hash,
                        "current_slot": idx,
                        "probes": (idx - original_hash) % self._capacity,
                        "inserted_at": record.inserted_at
                    }
                })
        return state
