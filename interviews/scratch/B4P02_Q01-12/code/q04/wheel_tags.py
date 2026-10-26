"""Which wheel tags would pip accept on this machine? glibc -> manylinux, musl -> musllinux."""
import platform
from packaging import tags
libc = platform.libc_ver()
print("libc:", libc)
accepted = [str(t) for t in tags.sys_tags() if t.interpreter == "cp313" and t.abi == "cp313"]
plats = sorted({a.split("-")[-1] for a in accepted})
print("cp313 platform tags accepted here (first 6):", plats[:6])
many = [p for p in plats if p.startswith("manylinux")]
musl = [p for p in plats if p.startswith("musllinux")]
print("manylinux tags:", len(many) > 0, "| musllinux tags:", len(musl) > 0)

# what an alpine (musl) box would accept, built explicitly
alp = [str(t) for t in tags.cpython_tags(python_version=(3, 11), platforms=["musllinux_1_2_x86_64"])]
print("alpine example:", alp[0], "-> a wheel tagged manylinux2014_x86_64 would NOT match")
fake = "examplepkg-1.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl"
from packaging.utils import parse_wheel_filename
_, _, _, wtags = parse_wheel_filename(fake)
print("manylinux wheel (examplepkg) installable on alpine:", any(t in set(tags.cpython_tags(python_version=(3, 11), platforms=["musllinux_1_2_x86_64"])) for t in wtags))
mly = set(tags.cpython_tags(python_version=(3, 11), platforms=["manylinux_2_28_x86_64", "manylinux_2_17_x86_64", "manylinux2014_x86_64"]))
print("same wheel installable on a glibc distro (emulated tags):", any(t in mly for t in wtags))
