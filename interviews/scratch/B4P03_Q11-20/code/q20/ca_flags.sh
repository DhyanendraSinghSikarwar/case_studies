# NOT EXECUTED. Example Cluster Autoscaler container args (self-managed install). Flag names exist in the
# upstream project but defaults and cloud-specific flags change; check the current FAQ for your version.
CA_ARGS=(
  --nodes=0:3:gpu-pool   # min:max:node-group-name  (0 = pool may be empty)
  --scale-down-unneeded-time=10m   # how long a node must look removable before it is deleted
  --scale-down-utilization-threshold=0.5   # below this share of requests, a node is a removal candidate
  --balance-similar-node-groups=false
  --skip-nodes-with-local-storage=true   # nodes with emptyDir/hostPath pods are skipped unless the pod is marked safe
  --skip-nodes-with-system-pods=true
)
