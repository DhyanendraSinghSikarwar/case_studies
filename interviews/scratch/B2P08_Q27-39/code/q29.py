# Minimal MCP-STYLE server and client, plain Python, line-delimited JSON-RPC 2.0 over subprocess pipes.
# SIMPLIFIED: not full spec compliance, not the official SDK. initialize parameter names are from memory.
# One file: `python3 q29.py --server` runs the server; with no flag it runs the client + tests.
import json, subprocess, sys

# ---------------- server ----------------
TOOLS = [{"name": "add", "description": "Add two integers.",
          "inputSchema": {"type": "object", "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}}, "required": ["a", "b"]}}]

def handle(msg):
    if "id" not in msg:                               # notification: no id, no response
        return None
    rid, method, p = msg["id"], msg.get("method"), msg.get("params") or {}
    def ok(result): return {"jsonrpc": "2.0", "id": rid, "result": result}
    def err(code, text): return {"jsonrpc": "2.0", "id": rid, "error": {"code": code, "message": text}}
    if method == "initialize":
        return ok({"protocolVersion": p.get("protocolVersion", "2025-06-18"),
                   "capabilities": {"tools": {}}, "serverInfo": {"name": "toy-server", "version": "0.1"}})
    if method == "tools/list":
        return ok({"tools": TOOLS})
    if method == "tools/call":
        if p.get("name") != "add": return err(-32602, "Unknown tool")
        a = p.get("arguments", {})
        if not all(isinstance(a.get(k), int) for k in ("a", "b")):
            return ok({"isError": True, "content": [{"type": "text", "text": "a and b must be integers"}]})
        return ok({"isError": False, "content": [{"type": "text", "text": str(a["a"] + a["b"])}]})
    return err(-32601, "Method not found")

def serve():
    for line in sys.stdin:                            # stdout carries ONLY protocol messages; logs go to stderr
        line = line.strip()
        if not line: continue
        try: msg = json.loads(line)
        except json.JSONDecodeError:
            out = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}}
        else: out = handle(msg)
        if out is not None:
            sys.stdout.write(json.dumps(out) + "\n"); sys.stdout.flush()

# ---------------- client ----------------
class Client:
    def __init__(self):
        self.proc = subprocess.Popen([sys.executable, "-I", __file__, "--server"], stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE, text=True)
        self.next_id = 0
    def request(self, method, params=None):
        self.next_id += 1                             # unique non-null id per request
        self.proc.stdin.write(json.dumps({"jsonrpc": "2.0", "id": self.next_id, "method": method, "params": params or {}}) + "\n")
        self.proc.stdin.flush()
        resp = json.loads(self.proc.stdout.readline())
        assert resp["id"] == self.next_id and ("result" in resp) != ("error" in resp)   # result XOR error
        return resp
    def notify(self, method, params=None):
        self.proc.stdin.write(json.dumps({"jsonrpc": "2.0", "method": method, "params": params or {}}) + "\n"); self.proc.stdin.flush()
    def close(self): self.proc.stdin.close(); self.proc.wait(timeout=10)

if __name__ == "__main__":
    if "--server" in sys.argv: serve(); sys.exit(0)
    c = Client()
    init = c.request("initialize", {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "toy-client", "version": "0.1"}})
    c.notify("notifications/initialized")
    print("initialize ->", init["result"]["serverInfo"], init["result"]["protocolVersion"])
    tools = c.request("tools/list")["result"]["tools"]
    print("tools/list ->", [t["name"] for t in tools])
    r = c.request("tools/call", {"name": "add", "arguments": {"a": 2, "b": 3}})
    print("tools/call add(2,3) ->", r["result"]["content"][0]["text"])
    bad = c.request("tools/call", {"name": "add", "arguments": {"a": "x", "b": 3}})
    print("bad args -> isError =", bad["result"]["isError"])
    unk = c.request("tools/call", {"name": "nope", "arguments": {}})
    print("unknown tool -> error", unk["error"]["code"])
    meth = c.request("nope/nothing")
    print("unknown method -> error", meth["error"]["code"])
    c.close()
    # tests
    assert r["result"]["content"][0]["text"] == "5" and bad["result"]["isError"] is True
    assert unk["error"]["code"] == -32602 and meth["error"]["code"] == -32601 and tools[0]["inputSchema"]["type"] == "object"
    assert handle({"jsonrpc": "2.0", "method": "notifications/initialized"}) is None   # notifications get no reply
    print("tests passed")
