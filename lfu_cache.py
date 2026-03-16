#!/usr/bin/env python3
"""LFU Cache — O(1) get/put with frequency tracking."""
from collections import defaultdict

class LFUCache:
    def __init__(self, capacity):
        self.cap=capacity;self.min_freq=0
        self.key_val={};self.key_freq={};self.freq_keys=defaultdict(list)
        self.freq_pos={}
    def _touch(self,key):
        freq=self.key_freq[key]
        self.freq_keys[freq].remove(key)
        if not self.freq_keys[freq] and freq==self.min_freq: self.min_freq+=1
        self.key_freq[key]=freq+1;self.freq_keys[freq+1].append(key)
    def get(self,key):
        if key not in self.key_val: return -1
        self._touch(key);return self.key_val[key]
    def put(self,key,val):
        if self.cap<=0: return
        if key in self.key_val:
            self.key_val[key]=val;self._touch(key);return
        if len(self.key_val)>=self.cap:
            evict=self.freq_keys[self.min_freq].pop(0)
            del self.key_val[evict];del self.key_freq[evict]
        self.key_val[key]=val;self.key_freq[key]=1
        self.freq_keys[1].append(key);self.min_freq=1

def main():
    c=LFUCache(2);c.put(1,1);c.put(2,2);print(c.get(1))
    c.put(3,3);print(c.get(2));print(c.get(3))

if __name__=="__main__":main()
