"""Tiny lint: flag devel images in the last stage and unpinned/latest nvidia tags."""
import re, sys
froms = re.findall(r"^FROM\s+(\S+)", open(sys.argv[1]).read(), re.M)
final = froms[-1]
print("final image:", final)
if "nvidia/cuda" in final:
    flavour = next((f for f in ("devel", "runtime", "base") if f in final), "unknown")
    print("flavour:", flavour)
    if flavour == "devel": print("WARN: devel in the final stage (compilers, headers, big)")
    if final.endswith(":latest") or ":" not in final: print("WARN: unpinned tag")
else:
    print("not an nvidia/cuda image; CUDA libs must come from the wheel")
