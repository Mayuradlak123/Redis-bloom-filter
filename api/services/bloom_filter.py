import hashlib
import redis

class BloomFilter:
    def __init__(self, redis_client, key, size=10000000, hash_count=7):
        """
        :param redis_client: Redis client instance
        :param key: Redis key for the bitset
        :param size: Number of bits in the filter (m)
        :param hash_count: Number of hash functions (k)
        """
        self.redis = redis_client
        self.key = key
        self.size = size
        self.hash_count = hash_count

    def _hashes(self, value):
        """Generates k hash values for a given string."""
        hashes = []
        for i in range(self.hash_count):
            # Create a unique hash for each function using a salt
            hash_val = int(hashlib.sha256(f"{i}:{value}".encode()).hexdigest(), 16)
            hashes.append(hash_val % self.size)
        return hashes

    def add(self, value):
        """Adds a value to the bloom filter."""
        for position in self._hashes(value):
            self.redis.setbit(self.key, position, 1)

    def exists(self, value):
        """Checks if a value might be in the bloom filter."""
        for position in self._hashes(value):
            if not self.redis.getbit(self.key, position):
                return False
        return True
