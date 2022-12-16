# Name: Maya D'Souza
# OSU Email: dsouzam@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 8/8/2022
# Description: Hash Map Implementation Using Separate Chaining


from a6_include import (DynamicArray, LinkedList, hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        Adds key-value pair to hash map. (Will overwrite existing values).
        """
        # set index based on key and go to the proper bucket
        hash = self._hash_function(key)
        index = hash % self._buckets.length()
        bucket = self._buckets[index]

        # find node in bucket and add value to node
        node = bucket.contains(key)
        if node:
            node.value = value  # matching key, overwrite value
        else:
            bucket.insert(key, value)  # no matching key, insert value
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Returns number of empty buckets in hash map.
        """
        counter = 0
        for i in range(0, self._buckets.length()):  # iterate through buckets
            bucket = self._buckets[i]
            if not bucket.length():
                counter += 1  # increment for empty buckets
        return counter

    def table_load(self) -> float:
        """
        Returns load factor of hash table.
        """
        m = self._buckets.length()
        n = self._size
        return n/m

    def clear(self) -> None:
        """
        Clears hash map contents, maintains capacity.
        """
        for i in range(0, self._buckets.length()):
            self._buckets[i] = LinkedList()
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Change capacity of hash table.
        """
        if new_capacity < 1:  # invalid capacity
            return
        if not self._is_prime(new_capacity):  # set capacity to next prime number if not prime
            new_capacity = self._next_prime(new_capacity)

        # store hashmap in old hashmap
        old_hash_map = DynamicArray()
        self._size = 0
        for i in range(0, self._buckets.length()):
            old_hash_map.append(self._buckets[i])

        # create new empty hash map with proper capacity
        self._buckets = DynamicArray()
        for _ in range(new_capacity):  # add buckets to dynamic array to update capacity
            self._buckets.append(LinkedList())
        self._capacity = new_capacity

        # rehash values from old hash map
        for i in range(0, old_hash_map.length()):
            for node in old_hash_map[i]:
                self.put(node.key, node.value)

    def get(self, key: str) -> object:
        """
        Returns value associated with key.
        """
        for i in range(0, self._buckets.length()):  # iterate through buckets
            node = self._buckets[i].contains(key)  # look for node with matching key
            if node:
                return node.value  # return node's value
        return None  # no node with matching key found

    def contains_key(self, key: str) -> bool:
        """
        Found node with matching key.
        """
        for i in range(0, self._buckets.length()):  # iterate through buckets
            node = self._buckets[i].contains(key)  # look for node with matching key
            if node:
                return True
        return False

    def remove(self, key: str) -> None:
        """
        Removes key if in hash map.
        """
        for i in range(0, self._buckets.length()):  # iterate through buckets
            node = self._buckets[i].contains(key)  # look for node with matching key
            if node:
                self._buckets[i].remove(key)
                self._size -= 1
                return

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns dynamic array of tuples with key/value pairs of all nodes in hash map.
        """
        output = DynamicArray()
        for i in range(0, self._buckets.length()):
            for node in self._buckets[i]:
                output.append((node.key, node.value))
        return output

    def get_values(self) -> DynamicArray:
        """
        Returns dynamic array of values of all nodes in hash map.
        """
        output = DynamicArray()
        for i in range(0, self._buckets.length()):
            for node in self._buckets[i]:
                output.append(node.value)
        return output

    def find_mode_put(self, key: str) -> None:
        """
        Helper for find-mode. Key is value from input array, value is frequency.
        """
        hash = self._hash_function(key)
        index = hash % self._buckets.length()
        bucket = self._buckets[index]
        node = bucket.contains(key)
        if node:
            node.value += 1
        else:
            bucket.insert(key, 1)
            self._size += 1

    def find_mode_bucket_value(self, index, mode, frequency):
        """Helper for find-mode. Finds mode so far by checking the bucket against the previous ones."""
        bucket = self._buckets[index]
        for node in bucket:  # iterate through bucket
            key, value = node.key, node.value
            if value > frequency:  # update frequency when exceeded
                frequency = value
                mode = DynamicArray()
                mode.append(key)
            elif value == frequency:  # add to mode when frequency is matched
                mode.append(key)
        return mode, frequency


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Find mode of an array.
    """
    # create hash map where keys are values in da and values are their frequency.
    map = HashMap()
    for i in range(0, da.length()):
        map.find_mode_put(da[i])

    # initializes mode as empty array and frequency based on first element
    mode = DynamicArray()
    frequency = 0

    # Find mode and frequency using hash map
    for i in range(0, map.get_capacity()):
        mode, frequency = map.find_mode_bucket_value(i, mode, frequency)

    return mode, frequency
