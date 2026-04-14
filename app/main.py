class Dictionary:
    def __init__(self, capacity=8):
        self.capacity = capacity
        self.size = 0
        self.load_factor = 2 / 3
        self.table = [None] * self.capacity

    def _hash(self, key):
        return hash(key) % self.capacity

    def __setitem__(self, key, value):
        if self.size / self.capacity >= self.load_factor:
            self._resize()

        index = self._hash(key)

        while self.table[index] is not None:
            if self.table[index][0] == key:
                self.table[index] = (key, value)
                return
            index = (index + 1) % self.capacity

        self.table[index] = (key, value)
        self.size += 1

    def __getitem__(self, key):
        index = self._hash(key)
        start_index = index

        while self.table[index] is not None:
            if self.table[index][0] == key:
                return self.table[index][1]
            index = (index + 1) % self.capacity
            if index == start_index:
                break

        raise KeyError(f"Key {key} not found")

    def _resize(self):
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for item in old_table:
            if item is not None:
                self.__setitem__(item[0], item[1])

    def __len__(self):
        return self.size