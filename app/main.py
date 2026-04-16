from typing import Any, Optional, List, Tuple


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        if not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("The capacity must be a positive integer.")

        self.capacity: int = capacity
        self.size: int = 0
        self.load_factor: float = 2 / 3
        self.table: List[Optional[Tuple[Any, int, Any]]] = [None] * self.capacity
        self.capacity: int = capacity
        self.size: int = 0
        self.load_factor: float = 2 / 3
        self.table: List[Optional[Tuple[Any, int, Any]]] = (
            [None] * self.capacity
        )

    def _hash(self, key: Any) -> int:
        return hash(key)

    def _find_slot(self, key: Any, full_hash: int) -> int:
        index: int = full_hash % self.capacity
        while self.table[index] is not None:
            node = self.table[index]
            if node is not None and node[1] == full_hash and node[0] == key:
                return index
            index = (index + 1) % self.capacity
        return index

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size / self.capacity >= self.load_factor:
            self._resize()

        full_hash: int = self._hash(key)
        index: int = self._find_slot(key, full_hash)

        if self.table[index] is None:
            self.size += 1

        self.table[index] = (key, full_hash, value)

    def __getitem__(self, key: Any) -> Any:
        full_hash: int = self._hash(key)
        index: int = self._find_slot(key, full_hash)
        node = self.table[index]

        if node is not None and node[1] == full_hash and node[0] == key:
            return node[2]

        raise KeyError(f"Key {key} not found")

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for item in old_table:
            if item is not None:
                index = self._find_slot(item[0], item[1])
                self.table[index] = item
                self.size += 1

    def __len__(self) -> int:
        return self.size
