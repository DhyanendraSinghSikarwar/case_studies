"""Q34: toy operator. A 'ModelServer' custom resource is desired state; reconcile() drives actual state to it.
Pure Python, runs for real. The 'cluster' is a dict; failures are injected to show self-healing."""
import copy

desired = {"ModelServer/churn": {"replicas": 3, "image": "churn:1.0"}}   # the custom resources (spec)
actual = {}                                                              # pods that exist: name -> image

def reconcile(cr_name, spec):
    """Level-based: look at the whole picture, do the minimum to converge, safe to run again."""
    base = cr_name.split("/")[1]
    want = {f"{base}-{i}": spec["image"] for i in range(spec["replicas"])}
    actions = []
    for pod in sorted(set(actual) - set(want)):
        del actual[pod]; actions.append(f"delete {pod}")
    for pod, img in want.items():
        if pod not in actual:
            actual[pod] = img; actions.append(f"create {pod} ({img})")
        elif actual[pod] != img:
            actual[pod] = img; actions.append(f"replace {pod} -> {img}")
    return actions

def tick(label):
    acts = []
    for cr, spec in desired.items():
        acts += reconcile(cr, spec)
    print(f"[{label}] actions={acts or 'none (converged)'} actual={dict(sorted(actual.items()))}")

tick("t0 first run")
tick("t1 nothing changed")
del actual["churn-1"]                                   # a pod dies
tick("t2 pod churn-1 killed")
desired["ModelServer/churn"]["replicas"] = 2            # user edits the CR: scale down
tick("t3 replicas 3->2")
desired["ModelServer/churn"]["image"] = "churn:1.1"     # user edits the CR: new image
tick("t4 image 1.0->1.1")
tick("t5 idempotent re-run")
del desired["ModelServer/churn"]                        # CR deleted (a real operator uses finalizers; here: cleanup by hand)
actual.clear()
tick("t6 CR deleted, cleaned up")
