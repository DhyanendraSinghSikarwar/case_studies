"""Q44: confirm every command and flag in the drill exists, using only --help (no daemon).
Run: python3 -I drill_check.py"""
import re, subprocess

DRILL = [  # (subcommand words, flags that must appear in its --help)
    (["run"], ["-d", "-p", "-v", "--rm", "-i", "-t", "--name", "--gpus", "-e"]),
    (["exec"], ["-i", "-t"]), (["logs"], ["-f", "--tail"]), (["ps"], ["-a"]),
    (["stop"], ["-t"]), (["kill"], ["-s"]), (["rm"], ["-f", "-v"]), (["rmi"], ["-f"]),
    (["inspect"], ["--format"]), (["cp"], []), (["stats"], ["--no-stream"]),
    (["tag"], []), (["push"], []), (["build"], ["-t", "-f", "--target", "--build-arg"]),
    (["history"], ["--no-trunc"]), (["save"], ["-o"]), (["load"], ["-i"]),
    (["system", "prune"], ["-a", "--volumes"]),
]
ok_all = True
for words, flags in DRILL:
    text = subprocess.run(["docker", *words, "--help"], capture_output=True, text=True).stdout
    missing = [f for f in flags if not re.search(r"(^|[\s,])" + re.escape(f) + r"([\s,=\[]|$)", text, re.M)]
    ok_all &= not missing and bool(text)
    print(f"docker {' '.join(words):<13} help ok={bool(text)!s:<5} flags {flags} missing={missing}")
print("ALL OK" if ok_all else "SOMETHING MISSING")
