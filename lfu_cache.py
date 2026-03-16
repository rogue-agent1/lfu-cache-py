"""LFU Cache — Least Frequently Used eviction."""
from collections import defaultdict

class LFUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.cache = {}
        self.freq = {}
        self.freq_to_keys = defaultdict(list)
        self.min_freq = 0
    def get(self, key):
        if key not in self.cache: return -1
        self._update_freq(key)
        return self.cache[key]
    def put(self, key, value):
        if self.cap <= 0: return
        if key in self.cache:
            self.cache[key] = value
            self._update_freq(key)
            return
        if len(self.cache) >= self.cap:
            evict = self.freq_to_keys[self.min_freq].pop(0)
            del self.cache[evict]; del self.freq[evict]
        self.cache[key] = value
        self.freq[key] = 1
        self.freq_to_keys[1].append(key)
        self.min_freq = 1
    def _update_freq(self, key):
        f = self.freq[key]
        self.freq[key] = f + 1
        self.freq_to_keys[f].remove(key)
        if not self.freq_to_keys[f] and f == self.min_freq:
            self.min_freq += 1
        self.freq_to_keys[f + 1].append(key)

if __name__ == "__main__":
    lfu = LFUCache(3)
    lfu.put(1, "a"); lfu.put(2, "b"); lfu.put(3, "c")
    lfu.get(1); lfu.get(1); lfu.get(2)
    lfu.put(4, "d")  # evicts 3 (least frequent)
    assert lfu.get(3) == -1
    assert lfu.get(1) == "a"
    assert lfu.get(4) == "d"
    print("LFU cache: eviction works correctly")
    print("All tests passed!")
