import re, sys, io, contextlib, time
txt = open(sys.argv[1]).read()
parts = re.split(r"#@@ (\w+)\n", txt)
for name, code in zip(parts[1::2], parts[2::2]):
    if len(sys.argv) > 2 and name not in sys.argv[2:]:
        continue
    t = time.time()
    print("==", name, flush=True)
    try:
        exec(compile(code, name, "exec"), {"__name__": "__main__"})
    except Exception as e:
        print("FAILED", repr(e))
    print("   (%.0fs)" % (time.time() - t), flush=True)
