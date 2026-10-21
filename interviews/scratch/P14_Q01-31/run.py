import sys, io, contextlib, warnings
warnings.filterwarnings("ignore")
txt = open("snips.txt", encoding="utf8").read()
parts = txt.split("#### ")[1:]
for p in parts:
    name, code = p.split("\n", 1)
    print("=====", name)
    try:
        exec(compile(code, name, "exec"), {})
    except Exception as e:
        print("FAILED", repr(e))
