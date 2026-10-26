import os, sys
LIMIT = 5 * 1024 * 1024
bad = [f for f in sys.argv[1:] if os.path.getsize(f) > LIMIT]
for f in bad:
    print(f"{f}: {os.path.getsize(f)/1024/1024:.1f} MB > 5 MB (use DVC or Git LFS instead)")
sys.exit(1 if bad else 0)
