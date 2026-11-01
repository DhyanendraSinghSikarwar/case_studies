"""Write the lineage record stored next to every trained model (values passed in by CI)."""
import json, sys, hashlib, datetime
def record(image_digest, git_commit, data_version, model_path_bytes):
    return {"image_digest": image_digest, "git_commit": git_commit, "data_version": data_version,
            "model_sha256": hashlib.sha256(model_path_bytes).hexdigest()[:16],
            "note": "repeatable behaviour needs seeds + data version too, not only the image"}
print(json.dumps(record("sha256:" + "ab" * 32, "9f2c1e7", "dvc:rev-2026-10", b"weights"), indent=2))
