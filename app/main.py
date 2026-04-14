from typing import Any, Optional, List, Tuple


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity: int = capacity
        self.size: int = 0
        self.load_factor: float = 2 / 3
        self.table: List[Optional[Tuple[Any, Any]]] = [None] * self.capacity

    def _hash(self, key: Any) -> int:
        return hash(key) % self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size / self.capacity >= self.load_factor:
            self._resize()

        index: int = self._hash(key)
        while self.table[index] is not None:
            if self.table[index][0] == key:
                self.table[index] = (key, value)
                return
            index = (index + 1) % self.capacity

        self.table[index] = (key, value)
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        index: int = self._hash(key)
        start_index: int = index

        while self.table[index] is not None:
            if self.table[index][0] == key:
                return self.table[index][1]
            index = (index + 1) % self.capacity
            if index == start_index:
                break

        raise KeyError(f"Key {key} not found")

    def _resize(self) -> None:
        old_table: List[Optional[Tuple[Any, Any]]] = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for item in old_table:
            if item is not None:
                self.__setitem__(item[0], item[1])

    def __len__(self) -> int:
        return self.size
