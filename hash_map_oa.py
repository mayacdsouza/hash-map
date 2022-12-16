# Name: Maya D'Souza
# OSU Email: dsouzam@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 8/8/2022
# Description: Hash Map Implementation Using Open Addressing


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Add value to hash map.
        """
        if self.table_load() >= .5:  # if load factor >= 0.5, resize table
            self.resize_table(self._capacity*2)

        # set index of key, and variables for quadratic probing if needed
        hash = self._hash_function(key)
        index = hash % self._buckets.length()
        i_initial = index
        j = 1

        # put key/value pair at index if open
        if not self._buckets[index]:
            self._buckets[index] = HashEntry(key, value)
            self._size += 1
            return

        # overwrite key/value pair with matching key with new value
        if self._buckets[index].key == key:
            self._buckets[index].value = value
            if self._buckets[index].is_tombstone:
                self._buckets[index].is_tombstone = False  # no longer a tombstone
                self._size += 1
            return
        else:
            while True:  # keep probing till space is found
                index = (i_initial + j**2) % self._buckets.length()
                j += 1
                if not self._buckets[index]:
                    self._buckets[index] = HashEntry(key, value)
                    self._size += 1
                    return
                if self._buckets[index].key == key:
                    self._buckets[index].value = value
                    if self._buckets[index].is_tombstone:
                        self._buckets[index].is_tombstone = False
                        self._size += 1
                    return

    def table_load(self) -> float:
        """
        Returns table load of hash map.
        """
        m = self._buckets.length()
        n = self._size
        return n/m

    def empty_buckets(self) -> int:
        """
        Returns number of empty buckets.
        """
        counter = 0
        for i in range(0, self._buckets.length()):  # iterate through buckets
            if not self._buckets[i]:
                counter += 1  # increment for empty buckets
        return counter

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes table to new capacity. Rehashs values.
        """
        if new_capacity < self._size:  # invalid capacity
            return
        if not self._is_prime(new_capacity):  # set capacity to next prime number if not prime
            new_capacity = self._next_prime(new_capacity)

        # store hash map in old-hashmap
        old_hash_map = DynamicArray()
        self._size = 0
        for i in range(0, self._buckets.length()):
            old_hash_map.append(self._buckets[i])

        # create new hash map of updated capacity
        self._buckets = DynamicArray()
        for _ in range(new_capacity):  # add buckets to dynamic array to update capacity
            self._buckets.append(None)
        self._capacity = new_capacity
        for i in range(0, old_hash_map.length()):  # rehash values
            if old_hash_map[i]:
                self.put(old_hash_map[i].key, old_hash_map[i].value)

    def get(self, key: str) -> object:
        """
        Returns value associated with key.
        """
        for i in range(0, self._buckets.length()):
            if self._buckets[i]:
                if self._buckets[i].key == key:  # key matches
                    if not self._buckets[i].is_tombstone:  # check not a tombstone
                        return self._buckets[i].value  # return value

    def contains_key(self, key: str) -> bool:
        """
        Checks if key in hash map.
        """
        for i in range(0, self._buckets.length()):
            if self._buckets[i]:
                if self._buckets[i].key == key:  # key matches
                    if not self._buckets[i].is_tombstone:  # not a tombstone
                        return True
        return False  # key not found

    def remove(self, key: str) -> None:
        """
        Delete key from hashmap.
        """
        for i in range(0, self._buckets.length()):
            if self._buckets[i]:
                if self._buckets[i].key == key:
                    if not self._buckets[i].is_tombstone:
                        self._buckets[i].is_tombstone = True  # delete by setting to tombstone
                        self._size -= 1  # size is now one less
                        return  # exit loop after key is found

    def clear(self) -> None:
        """
        Clears hash map.
        """
        for i in range(0, self._buckets.length()):  # replace each bucket contents with None
            self._buckets[i] = None
        self._size = 0  # update size

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns Dynamic Array of tuples of key value pairs in hash map.
        """
        output = DynamicArray()
        for i in range(0, self._buckets.length()):
            if self._buckets[i]:
                if not self._buckets[i].is_tombstone:
                    output.append((self._buckets[i].key, self._buckets[i].value))
        return output
