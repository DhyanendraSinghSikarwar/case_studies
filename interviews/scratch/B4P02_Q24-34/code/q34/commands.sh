# NOT EXECUTED: needs a cluster node or a daemon.
crictl ps                      # on a node: list containers through the CRI, no Docker involved
crictl images
ctr -n k8s.io images ls        # containerd's own CLI (namespace k8s.io holds Kubernetes images)
kubectl get nodes -o wide      # CONTAINER-RUNTIME column shows containerd://... or cri-o://...
