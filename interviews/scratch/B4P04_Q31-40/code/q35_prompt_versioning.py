import hashlib, json, pathlib, sys, tempfile, mlflow
from mlflow.tracking import MlflowClient

def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()[:12]

work = pathlib.Path(tempfile.mkdtemp())
(work / "prompt.txt").write_text("Answer using only the context.\nContext: {context}\nQuestion: {question}\n")
(work / "eval.jsonl").write_text("\n".join(json.dumps(x) for x in [
    {"q": "Refund window?", "gold": "30 days"}, {"q": "Support hours?", "gold": "9 to 6"}]) + "\n")

def fake_answer(prompt_text, question):          # stand-in for an LLM call: NOT a model, not executed
    return {"Refund window?": "30 days", "Support hours?": "9 to 6" if "only the context" in prompt_text else "24x7"}[question]

def run(tag):
    prompt = (work / "prompt.txt").read_text()
    rows = [json.loads(l) for l in (work / "eval.jsonl").read_text().splitlines()]
    acc = sum(fake_answer(prompt, r["q"]) == r["gold"] for r in rows) / len(rows)
    with mlflow.start_run(run_name=tag):
        mlflow.set_tags({"prompt_sha": sha(work / "prompt.txt"), "evalset_sha": sha(work / "eval.jsonl"),
                         "embedding_model": "example-embedder@rev-abc (placeholder)", "index_build": "idx-2026-10-26 (placeholder)"})
        mlflow.log_artifact(str(work / "prompt.txt")); mlflow.log_artifact(str(work / "eval.jsonl"))
        mlflow.log_metric("exact_match", acc)

mlflow.set_tracking_uri("sqlite:///genai.db"); mlflow.set_experiment("rag-eval")
run("baseline")
(work / "prompt.txt").write_text("Be brief.\nContext: {context}\nQuestion: {question}\n")   # someone edits the prompt
run("after-prompt-edit")
df = mlflow.search_runs(experiment_names=["rag-eval"], order_by=["start_time ASC"])
print(df[["tags.mlflow.runName", "metrics.exact_match", "tags.prompt_sha", "tags.evalset_sha"]].to_string(index=False))
a, b = df.iloc[0], df.iloc[1]
print("\nprompt changed :", a["tags.prompt_sha"] != b["tags.prompt_sha"])
print("eval set same  :", a["tags.evalset_sha"] == b["tags.evalset_sha"])
print("metric delta   :", b["metrics.exact_match"] - a["metrics.exact_match"])
