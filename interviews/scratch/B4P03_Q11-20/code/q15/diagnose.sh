# NOT EXECUTED (no cluster). Run in this order; each step narrows the cause.
kubectl describe pod train-big -n ml | sed -n '/Events:/,$p'          # the scheduler's one-line reason is here
kubectl get pod train-big -n ml -o jsonpath='{.spec.containers[*].resources}'   # GPU limit on the RIGHT container?
kubectl get nodes -o custom-columns='NODE:.metadata.name,GPU:.status.allocatable.nvidia\.com/gpu'
kubectl describe node gpu-d | grep -A8 -i -E 'Taints|Allocatable|Allocated resources'
kubectl get pods -n gpu-operator -o wide                               # device plugin / driver pods Running on every GPU node?
kubectl get resourcequota -n ml                                        # quota on requests.nvidia.com/gpu used up?
kubectl get pods -A -o wide --field-selector spec.nodeName=gpu-a       # who is actually holding the GPUs
kubectl exec -n ml notebook-ravi -- nvidia-smi                         # is the held GPU doing any work?
