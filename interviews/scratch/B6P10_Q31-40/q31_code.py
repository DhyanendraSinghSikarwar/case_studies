import math
items, dim, bytes_per = 20_000_000, 128, 4
peak_qps, node_gb, usable, replica_qps = 3000, 8, 0.60, 1200
index_bytes = items * dim * bytes_per
usable_per_node = node_gb * 1e9 * usable
nodes_per_replica = math.ceil(index_bytes / usable_per_node)
replicas = math.ceil(peak_qps / replica_qps)
total = nodes_per_replica * replicas
print("index GB", index_bytes / 1e9, "usable per node GB", usable_per_node / 1e9)
print("nodes/replica", nodes_per_replica, "replicas", replicas, "total nodes", total)
assert index_bytes == 10_240_000_000 and usable_per_node == 4.8e9
assert nodes_per_replica == 3 and replicas == 3 and total == 9
# headroom view: 3 replicas serve 3,600 qps, so peak uses 3000/3600
util = peak_qps / (replicas * replica_qps)
print("replica utilisation at peak", round(util, 3))
assert round(util, 3) == 0.833
# losing one replica (N+1): 4 replicas = 12 nodes
assert math.ceil((peak_qps) / replica_qps) + 1 == 4 and 4 * nodes_per_replica == 12
# trade-off: int8 quantisation cuts the index 4x (editor knowledge, recall must be measured)
q_bytes = items * dim * 1
q_nodes = math.ceil(q_bytes / usable_per_node)
print("int8 index GB", q_bytes / 1e9, "nodes/replica", q_nodes, "total", q_nodes * replicas)
assert q_bytes == 2_560_000_000 and q_nodes == 1 and q_nodes * replicas == 3
