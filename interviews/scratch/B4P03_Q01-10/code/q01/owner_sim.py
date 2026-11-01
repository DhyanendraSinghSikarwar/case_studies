"""Toy ReplicaSet reconcile loop: 'desired 3 pods' is restored after a delete."""
import itertools

ids = itertools.count(1)

class ReplicaSet:
    def __init__(self, name, replicas):
        self.name, self.replicas, self.pods = name, replicas, []
    def reconcile(self):
        while len(self.pods) < self.replicas:           # too few: create
            self.pods.append(f"{self.name}-{next(ids):02d}")
        while len(self.pods) > self.replicas:           # too many: delete
            self.pods.pop()

rs = ReplicaSet("ml-api-7d9f", 3)      # Deployment owns this ReplicaSet
rs.reconcile()
print("start      :", rs.pods)
rs.pods.remove(rs.pods[1])             # kubectl delete pod <one>
print("after kill :", rs.pods, "(2 pods, 1 missing)")
rs.reconcile()                         # controller notices the gap
print("reconciled :", rs.pods, "(new name, same count)")

bare = ["bare-pod"]                    # a bare Pod has no controller
bare.remove("bare-pod")
print("bare pod after delete:", bare, "(nobody recreates it)")
