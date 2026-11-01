# check_repo.py REPO : layout + config text parses + dims match the ONNX file. Triton itself is NOT run.
import sys, pathlib, onnx
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from pbtxt import parse
repo = pathlib.Path(sys.argv[1]); ok = True
def check(cond, msg):
    global ok; ok &= bool(cond); print(("PASS " if cond else "FAIL ") + msg)
for mdir in sorted(p for p in repo.iterdir() if p.is_dir()):
    cfg = parse((mdir / "config.pbtxt").read_text())
    check(cfg["name"][0] == mdir.name, f"config name equals folder name ({mdir.name})")
    versions = [p.name for p in mdir.iterdir() if p.is_dir()]
    check(versions and all(v.isdigit() for v in versions), f"version folders are numeric: {versions}")
    mf = mdir / versions[0] / "model.onnx"
    check(mf.exists(), "default ONNX file name is <version>/model.onnx")
    check(cfg["backend"][0] == "onnxruntime", "backend onnxruntime")
    mb = cfg["max_batch_size"][0]
    g = onnx.load(str(mf)).graph
    shapes = lambda vs: {v.name: [d.dim_value if d.dim_value else -1 for d in v.type.tensor_type.shape.dim] for v in vs}
    onx_in, onx_out = shapes(g.input), shapes(g.output)
    for t in cfg["input"]:
        want = onx_in[t["name"][0]]
        check(mb > 0 and want[1:] == t["dims"], f"input {t['name'][0]}: ONNX {want} = batch dim + config dims {t['dims']}")
    for t in cfg["output"]:
        want = onx_out[t["name"][0]]
        dims = t["dims"]; rs = "reshape" in t   # empty shape [] parses to an empty message
        # a per-item scalar is declared dims [1] with reshape [] (check current Triton docs)
        check(want[1:] == dims or (want[1:] == [] and dims == [1] and rs),
              f"output {t['name'][0]}: ONNX {want}, config dims {dims}")
    check(cfg["instance_group"][0]["kind"][0] == "KIND_CPU", "instance_group kind KIND_CPU")
print("ALL OK" if ok else "PROBLEMS"); sys.exit(0 if ok else 1)
