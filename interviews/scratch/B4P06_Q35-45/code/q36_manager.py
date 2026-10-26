# Q36: bounded LRU of ONNX sessions, lazy load, per-model locks, no double load.
import threading, time
from collections import OrderedDict
import onnxruntime as ort

class ModelManager:
    def __init__(self, registry_lookup, max_models=3):
        self.lookup = registry_lookup            # tenant -> path of .onnx (the "registry")
        self.max_models = max_models
        self._cache = OrderedDict()              # tenant -> session, oldest first
        self._lock = threading.Lock()            # protects _cache and _locks only (short holds)
        self._locks = {}                         # tenant -> lock held during that tenant's load
        self.loads = {}                          # tenant -> times loaded (for tests)
        self.evictions = []

    def get(self, tenant):
        with self._lock:
            if tenant in self._cache:
                self._cache.move_to_end(tenant)  # mark most recently used
                return self._cache[tenant]
            tlock = self._locks.setdefault(tenant, threading.Lock())
        with tlock:                              # only callers for THIS tenant wait here
            with self._lock:                     # someone may have loaded it while we waited
                if tenant in self._cache:
                    self._cache.move_to_end(tenant)
                    return self._cache[tenant]
            path = self.lookup(tenant)           # KeyError -> unknown tenant, nothing cached
            sess = ort.InferenceSession(path, providers=["CPUExecutionProvider"])  # slow part, outside the global lock
            with self._lock:
                self.loads[tenant] = self.loads.get(tenant, 0) + 1
                self._cache[tenant] = sess
                while len(self._cache) > self.max_models:
                    old, _ = self._cache.popitem(last=False)   # evict least recently used
                    self.evictions.append(old)
            return sess

    def cached(self):
        with self._lock:
            return list(self._cache)
