from typing import Any, Optional, List, Tuple


class Dictionary:
    """
    Custom Dictionary implementation using hash table with open addressing.
    Each node in the table is a tuple: (key, stored_hash, value).
    """

    def __init__(self, capacity: int = 8) -> None:
        self.capacity: int = capacity
        self.size: int = 0
        self.load_factor: float = 2 / 3
        self.table: List[Optional[Tuple[Any, int, Any]]] = [None] * self.capacity

    def _hash(self, key: Any) -> int:
        return hash(key)

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size / self.capacity >= self.load_factor:
            self._resize()

        full_hash: int = self._hash(key)
        index: int = full_hash % self.capacity

        while self.table[index] is not None:
            node = self.table[index]
            # Безопасная проверка: node уже не None благодаря циклу
            if node is not None and node[1] == full_hash and node[0] == key:
                self.table[index] = (key, full_hash, value)
                return
            index = (index + 1) % self.capacity

        self.table[index] = (key, full_hash, value)
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        full_hash: int = self._hash(key)
        index: int = full_hash % self.capacity
        start_index: int = index

        while self.table[index] is not None:
            node = self.table[index]
            if node is not None and node[1] == full_hash and node[0] == key:
                return node[2]
            index = (index + 1) % self.capacity
            if index == start_index:
                break

        raise KeyError(f"Key {key} not found")

    def _resize(self) -> None:
        old_table: List[Optional[Tuple[Any, int, Any]]] = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for item in old_table:
            if item is not None:
                self._insert_during_resize(item[0], item[1], item[2])

    def _insert_during_resize(
        self, key: Any, full_hash: int, value: Any
    ) -> None:
        index: int = full_hash % self.capacity
        while self.table[index] is not None:
            index = (index + 1) % self.capacity

        self.table[index] = (key, full_hash, value)
        self.size += 1

    def __len__(self) -> int:
        return self.size
