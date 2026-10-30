import subprocess, sys, pathlib
base = pathlib.Path(__file__).parent
for n in range(11, 21):
    r = subprocess.run([sys.executable, "-I", str(base / "code" / f"q{n}.py")], capture_output=True, text=True)
    (base / "out" / f"q{n}.txt").write_text(r.stdout)
    print(n, "rc", r.returncode, r.stderr[-300:])
