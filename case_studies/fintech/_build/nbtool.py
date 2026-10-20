"""Build tooling for the case-study notebooks (not part of the analysis).

Usage (run from the project root):
  python _build/nbtool.py src2nb  SOURCE.src  NOTEBOOK.ipynb   # '#%% md' / '#%% code' cells; '@@INCLUDE path' inlines a file
  python _build/nbtool.py run     NOTEBOOK.ipynb               # execute in place (kernel 'fintech-cases'), retry kernel start
  python _build/nbtool.py dump    NOTEBOOK.ipynb               # print text outputs of every code cell
  python _build/nbtool.py fill    NOTEBOOK.ipynb FILLS.py      # replace «MARKERS» in markdown with R[...] from FILLS.py
  python _build/nbtool.py verify  NOTEBOOK.ipynb ...           # errors, unexecuted cells, leftover markers, chart takeaways
  python _build/nbtool.py adddec  ENTRIES.md ROWS.md           # add decision entries + summary rows to decision.md
  python _build/nbtool.py mark    CASE_NUMBER                  # mark a case notebook as built in the reference file and README
"""
import re
import runpy
import sys
import time

import nbformat


def src2nb(src, out):
    cells, kind, buf = [], None, []
    def flush():
        if kind:
            text = "\n".join(buf).strip("\n")
            cells.append(nbformat.v4.new_markdown_cell(text) if kind == "md" else nbformat.v4.new_code_cell(text))
    for line in open(src, encoding="utf-8").read().splitlines():
        m = re.match(r"^#%% (md|code)\s*$", line)
        if m:
            flush(); kind, buf = m.group(1), []
        elif line.startswith("@@INCLUDE "):
            buf.extend(open(line[10:].strip(), encoding="utf-8").read().rstrip("\n").splitlines())
        else:
            buf.append(line)
    flush()
    nb = nbformat.v4.new_notebook(cells=cells)
    nb.metadata["kernelspec"] = {"name": "fintech-cases", "display_name": "fintech-cases", "language": "python"}
    nbformat.write(nb, out)
    print(f"{out}: {len(cells)} cells")


def run(path):
    from nbconvert.preprocessors import ExecutePreprocessor, CellExecutionError
    for attempt in range(1, 6):
        nb = nbformat.read(path, as_version=4); t0 = time.time()
        try:
            ExecutePreprocessor(timeout=-1, kernel_name="fintech-cases").preprocess(nb, {"metadata": {"path": "."}})
            nbformat.write(nb, path); print(f"{path}: executed OK in {time.time() - t0:.0f}s (attempt {attempt})"); return
        except CellExecutionError as e:
            nbformat.write(nb, path); print(f"{path}: CELL ERROR\n{str(e)[-3000:]}"); sys.exit(1)
        except RuntimeError as e:
            if "Kernel died" in str(e) or "kernel_info" in str(e):
                print(f"kernel start failed (attempt {attempt}); retrying in 60s"); time.sleep(60); continue
            raise
    print(f"{path}: failed after 5 attempts"); sys.exit(1)


def dump(path):
    nb = nbformat.read(path, as_version=4)
    for i, c in enumerate(nb.cells):
        if c.cell_type != "code":
            continue
        print(f"--- cell {i} (exec {c.get('execution_count')}) ---")
        for o in c.get("outputs", []):
            if o.output_type == "stream":
                print(o.text.rstrip())
            elif o.output_type in ("execute_result", "display_data"):
                if "image/png" in o.data:
                    print("[image]")
                elif "text/plain" in o.data:
                    print(o.data["text/plain"].rstrip())
            elif o.output_type == "error":
                print("ERROR", o.ename, o.evalue)


def fill(path, fp):
    R = runpy.run_path(fp)["R"]; nb = nbformat.read(path, as_version=4); used = set()
    for c in nb.cells:
        if c.cell_type == "markdown":
            for k, v in R.items():
                if k in c.source:
                    c.source = c.source.replace(k, v.strip("\n")); used.add(k)
    nbformat.write(nb, path); missing = set(R) - used
    print(f"filled {len(used)} markers" + (f"; NOT FOUND: {sorted(missing)}" if missing else ""))


def verify(paths):
    ok = True
    for path in paths:
        nb = nbformat.read(path, as_version=4); cells = nb.cells; probs = []; n_code = n_img = 0
        for i, c in enumerate(cells):
            if c.cell_type == "markdown":
                if "TBD" in c.source or "«" in c.source:
                    probs.append(f"cell {i}: marker left in markdown")
                continue
            n_code += 1
            if c.get("execution_count") is None:
                probs.append(f"cell {i}: not executed")
            outs = c.get("outputs", [])
            if not outs:
                probs.append(f"cell {i}: no output")
            for o in outs:
                if o.output_type == "error":
                    probs.append(f"cell {i}: ERROR {o.ename}: {o.evalue}")
                if o.output_type == "stream" and o.name == "stderr" and "Warning" in o.text:
                    probs.append(f"cell {i}: warning on stderr")
            if any("data" in o and "image/png" in o.data for o in outs):
                n_img += 1
                if "set_title" not in c.source or (("set_xlabel" not in c.source or "set_ylabel" not in c.source) and "heatmap" not in c.source):
                    probs.append(f"cell {i}: chart may be missing title/axis labels")
                nxt = cells[i + 1] if i + 1 < len(cells) else None
                if nxt is None or nxt.cell_type != "markdown" or "takeaway" not in nxt.source.lower():
                    probs.append(f"cell {i}: chart not followed by a markdown takeaway")
        print(f"{path}: {len(cells)} cells, {n_code} code, {n_img} charts -> " + ("OK" if not probs else "PROBLEMS"))
        for p in probs:
            print("   ", p)
        ok &= not probs
    sys.exit(0 if ok else 1)


def adddec(entries, rows, log="decision.md"):
    s = open(log, encoding="utf-8").read(); e = open(entries, encoding="utf-8").read().strip("\n"); r = open(rows, encoding="utf-8").read().strip("\n")
    anchor = "---\n\n# Summary table"
    assert anchor in s and e.startswith("---")
    head = re.search(r"^# Case Study .*$", e, re.M).group(0)
    if head in s:
        print("already present:", head); return
    s = s.replace(anchor, e.lstrip("-").lstrip("\n").join(["---\n\n", "\n\n"]) + anchor, 1).rstrip("\n") + "\n" + r + "\n"
    open(log, "w", encoding="utf-8").write(s); print(f"added {head} | {len(r.splitlines())} summary rows")


def mark(case, ref="indian_fintech_data_science_case_studies.md", readme="README.md"):
    case = str(int(case))
    s = open(ref, encoding="utf-8").read()
    row = re.search(rf"^\| {case} \| [^\n]*$", s, re.M); assert row, "index row not found"
    nbname = re.search(r"`([^`]+\.ipynb)`", row.group(0)).group(1)
    s = s.replace(row.group(0), row.group(0).replace("| ⏳ |", "| ✅ |"))
    s = s.replace(f"`{nbname}` (⏳ notebook pending)", f"`{nbname}` (✅ notebook built)")
    open(ref, "w", encoding="utf-8").write(s)
    t = open(readme, encoding="utf-8").read()
    rrow = re.search(rf"^\| {case} \| [^\n]*$", t, re.M); assert rrow, "README row not found"
    t = t.replace(rrow.group(0), rrow.group(0).replace("| ⏳ pending |", "| ✅ built & verified |"))
    open(readme, "w", encoding="utf-8").write(t)
    built = len(re.findall(r"\| ✅ built & verified \|", t))
    print(f"case {case} ({nbname}) marked built | README: {built} of 30 built")


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    {"src2nb": lambda: src2nb(*args), "run": lambda: run(*args), "dump": lambda: dump(*args), "fill": lambda: fill(*args),
     "verify": lambda: verify(args), "adddec": lambda: adddec(*args), "mark": lambda: mark(*args)}[cmd]()
