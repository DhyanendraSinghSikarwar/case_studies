# Q15: lint a Dockerfile and a compose file for common networking mistakes (regex/pyyaml; not a full parser).
import re, sys, yaml

def check_dockerfile(path):
    out, text = [], open(path).read()
    exposed = {int(p) for m in re.finditer(r"^EXPOSE\s+(.+)$", text, re.M) for p in re.findall(r"\d+", m.group(1))}
    cmd = re.search(r"^(?:CMD|ENTRYPOINT)\s+(.+)$", text, re.M)
    line = cmd.group(1) if cmd else ""
    host = re.search(r"--host[ =\"',]+([0-9.a-z]+)", line)
    port = re.search(r"--port[ =\"',]+(\d+)", line)
    if host and host.group(1) in ("127.0.0.1", "localhost"):
        out.append(f"{path}: server binds {host.group(1)} inside the container; -p will not reach it, use 0.0.0.0")
    if not host and "uvicorn" in line:
        out.append(f"{path}: uvicorn without --host defaults to 127.0.0.1; add --host 0.0.0.0")
    if port and exposed and int(port.group(1)) not in exposed:
        out.append(f"{path}: app listens on {port.group(1)} but EXPOSE says {sorted(exposed)} (EXPOSE is only documentation)")
    return out

def check_compose(path):
    out, d = [], yaml.safe_load(open(path))
    for n, s in d["services"].items():
        for k, v in (s.get("environment") or {}).items():
            if re.search(r"(localhost|127\.0\.0\.1)", str(v)):
                out.append(f"{path}: {n}.{k} points at localhost; inside a container that is the container itself, use the service name")
        if s.get("network_mode") == "host" and s.get("ports"):
            out.append(f"{path}: {n} uses network_mode: host AND ports; ports are ignored with host networking")
        for p in s.get("ports", []):
            if str(p).count(":") == 1 and re.search(r"postgres|mysql|redis|mongo", str(s.get("image", ""))):
                out.append(f"{path}: {n} publishes {p} on all host interfaces; use 127.0.0.1:{p} or drop it")
    return out

findings = check_dockerfile(sys.argv[1]) + check_compose(sys.argv[2])
print("\n".join(findings) or "no findings"); print(f"{len(findings)} finding(s)")
