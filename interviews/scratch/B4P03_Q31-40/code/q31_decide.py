"""Q31: toy decision helper. Rules are a teaching aid, not a product. Runs offline."""
import pathlib, subprocess, sys

def decide(team):
    why = []
    if not team["has_k8s_platform_team"]:
        why.append("no one to run a cluster")
        if team["wants_managed"]:
            return "managed service (SageMaker / Vertex / Azure ML)", why
    if team["pipelines_only"] and team["has_k8s_platform_team"]:
        why.append("only pipelines needed: take Argo / Airflow / KFP alone, not the platform")
        return "plain Jobs + Argo or Airflow (or KFP alone)", why
    if team["multi_user_notebooks"] and team["hp_search"] and team["has_k8s_platform_team"] and team["data_scientists"] >= 20:
        why.append("many users, notebooks, search and serving on one cluster")
        return "Kubeflow pieces (Notebooks + Training Operator + Katib + KServe)", why
    why.append("small scope, simple batch training")
    return "plain Kubernetes Jobs (+ a scheduler)", why

cases = {
 "A: 4 DS, no platform team, on AWS":   dict(has_k8s_platform_team=False, wants_managed=True, pipelines_only=False, multi_user_notebooks=False, hp_search=False, data_scientists=4),
 "B: 8 DS, platform team, DAGs only":    dict(has_k8s_platform_team=True, wants_managed=False, pipelines_only=True, multi_user_notebooks=False, hp_search=False, data_scientists=8),
 "C: 40 DS, platform team, notebooks":   dict(has_k8s_platform_team=True, wants_managed=False, pipelines_only=False, multi_user_notebooks=True, hp_search=True, data_scientists=40),
 "D: 6 DS, platform team, nightly job":  dict(has_k8s_platform_team=True, wants_managed=False, pipelines_only=False, multi_user_notebooks=False, hp_search=False, data_scientists=6),
}
for name, t in cases.items():
    pick, why = decide(t)
    print(f"{name}\n   -> {pick}\n   because: {'; '.join(why)}")

here = pathlib.Path(__file__).resolve().parent
r = subprocess.run([sys.executable, "-I", "-m", "kubernetes_validate", "--strict", str(here / "q31_job.yaml")], capture_output=True, text=True)
print("\nkubernetes-validate --strict q31_job.yaml (exit", r.returncode, ")\n" + (r.stdout + r.stderr).strip())
