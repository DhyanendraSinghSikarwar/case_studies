# Q40: Ed25519 signed model manifest; tampered file rejected. Fake demo key generated in memory.
import hashlib, json
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.exceptions import InvalidSignature
sk = Ed25519PrivateKey.generate(); pk = sk.public_key()   # in real life the private key lives in an HSM/KMS, the app ships only pk
model = b"fake-onnx-bytes" * 10
manifest = {"name": "fieldnet", "version": 7, "sha256": hashlib.sha256(model).hexdigest(), "min_app": "3.1"}
payload = json.dumps(manifest, sort_keys=True).encode(); sig = sk.sign(payload)
def verify(manifest, sig, blob):
    p = json.dumps(manifest, sort_keys=True).encode()
    try: pk.verify(sig, p)
    except InvalidSignature: return "REJECT bad signature"
    if hashlib.sha256(blob).hexdigest() != manifest["sha256"]: return "REJECT hash mismatch"
    return "ACCEPT"
print("good:", verify(manifest, sig, model))
print("tampered model:", verify(manifest, sig, model + b"x"))
m2 = dict(manifest, version=6); print("rollback manifest edited:", verify(m2, sig, model))
# note: replay of an old VALID manifest still passes; add a monotonic version check
installed = 7
old = dict(manifest, version=5); old_sig = sk.sign(json.dumps(old, sort_keys=True).encode())
print("old valid manifest signature ok:", verify(old, old_sig, model), "-> app must also require version > installed:", old["version"] > installed)
# telemetry/update cost, abstract
devices = 100_000; model_mb = 8; updates_per_year = 6; delta_ratio = 0.2
full = devices * model_mb * updates_per_year; delta = full * delta_ratio
print(f"update traffic units: full {full} MB-units, delta {delta:.0f} ({delta/full:.0%})")
