"""Two checks that explain 'exec format error'. Teaching tool, not a Docker API."""
import json, platform, struct, sys

E_MACHINE = {0x3E: "amd64 (x86-64)", 0xB7: "arm64 (aarch64)", 0x28: "arm (32-bit)"}

def elf_arch(path):
    with open(path, "rb") as f:
        head = f.read(20)
    if head[:4] != b"\x7fELF":
        return "not an ELF binary (script or other format)"
    (machine,) = struct.unpack_from("<H", head, 18)   # e_machine, little-endian files
    return E_MACHINE.get(machine, hex(machine))

def pick(manifest_list, os_, arch):
    for m in manifest_list["manifests"]:
        p = m["platform"]
        if p["os"] == os_ and p["architecture"] == arch:
            return m["digest"]
    return None

# Hand-written sample shaped like an OCI index (digests are fake).
SAMPLE = json.loads("""{
 "schemaVersion": 2,
 "mediaType": "application/vnd.oci.image.index.v1+json",
 "manifests": [
  {"digest": "sha256:aaaa", "platform": {"os": "linux", "architecture": "amd64"}},
  {"digest": "sha256:bbbb", "platform": {"os": "linux", "architecture": "arm64"}}
 ]}""")
ARM_ONLY = {"manifests": [SAMPLE["manifests"][1]]}

print("this machine, python platform.machine():", platform.machine())
print("ELF header of", sys.executable, "->", elf_arch(sys.executable))
print("ELF header of /bin/sh ->", elf_arch("/bin/sh"))
print("ELF header of this .py file ->", elf_arch(__file__))
for name, idx in [("multi-arch index", SAMPLE), ("arm64-only index (built on a Mac)", ARM_ONLY)]:
    print(f"{name}: amd64 pick = {pick(idx, 'linux', 'amd64')}, arm64 pick = {pick(idx, 'linux', 'arm64')}")
