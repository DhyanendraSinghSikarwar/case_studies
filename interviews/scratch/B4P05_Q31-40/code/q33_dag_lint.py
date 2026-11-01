"""Static DAG linter (AST only, never imports the DAG): tags, owner, retries, no top-level network calls."""
import ast, sys, pathlib

NET_MODULES = {"requests", "urllib", "urllib3", "httpx", "boto3", "psycopg2", "pymysql", "socket", "snowflake"}

def kw(call, name):
    for k in call.keywords:
        if k.arg == name: return k.value
    return None

def dag_calls(tree):
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            f = n.func
            nm = f.id if isinstance(f, ast.Name) else f.attr if isinstance(f, ast.Attribute) else ""
            if nm == "dag" or nm == "DAG":
                yield n

def default_args_keys(call):
    da = kw(call, "default_args")
    return {k.value for k in da.keys if isinstance(k, ast.Constant)} if isinstance(da, ast.Dict) else set()

def top_level_net(tree):
    hits = []
    class V(ast.NodeVisitor):                        # skip function bodies: they run at task time
        def visit_FunctionDef(self, n): pass
        visit_AsyncFunctionDef = visit_FunctionDef
        def visit_Call(self, n):
            root = n.func
            while isinstance(root, (ast.Attribute, ast.Call)):
                root = root.value if isinstance(root, ast.Attribute) else root.func
            if isinstance(root, ast.Name) and root.id in NET_MODULES:
                hits.append((n.lineno, root.id))
            self.generic_visit(n)
    V().visit(tree)
    return hits

def lint(path):
    tree = ast.parse(pathlib.Path(path).read_text()); errs = []
    calls = list(dag_calls(tree))
    if not calls: return ["no DAG found"]
    for c in calls:
        da = default_args_keys(c)
        tags = kw(c, "tags")
        if not (isinstance(tags, ast.List) and tags.elts): errs.append(f"line {c.lineno}: missing tags")
        if "owner" not in da: errs.append(f"line {c.lineno}: default_args has no owner")
        if "retries" not in da: errs.append(f"line {c.lineno}: default_args has no retries")
    for ln, mod in sorted(set(top_level_net(tree))): errs.append(f"line {ln}: top-level call into {mod}")
    return errs

if __name__ == "__main__":
    bad = 0
    for p in sorted(pathlib.Path(sys.argv[1]).glob("*.py")):
        e = lint(p); bad += bool(e)
        print(f"{p.name}: {'OK' if not e else 'FAIL'}")
        for m in e: print("   ", m)
    sys.exit(1 if bad else 0)
