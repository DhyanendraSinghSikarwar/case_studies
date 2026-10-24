### Q27 ⭐⭐ 🟡 What does an MCP tool definition contain (name, description, input schema, output schema, annotations), and how are errors reported at the protocol and application levels?
**Asked at:** product, GenAI startups, agent-building teams
**Say this first (1 line):** An MCP tool is a JSON object with a unique name, a human-readable description, an inputSchema (JSON Schema) and optionally an outputSchema and annotations; failures come at three levels: transport (the connection), protocol (a JSON-RPC error object) and tool execution (a normal result with isError set to true so the model can see it and recover).

**Then explain:**
- **Definition fields:** `name`, `description` (what the model reads to decide whether to call it), `inputSchema` (JSON Schema for the arguments), optional `outputSchema` (a guide reports structured output arrived in the 2025-06-18 revision) and optional `annotations` such as read-only or destructive hints. The tools page itself was not opened for this answer; the field list is from the DataCamp guide and memory, so check the current spec.
- **Annotations are hints, not guarantees.** A server saying `readOnlyHint: true` is a claim. Treat annotations from an untrusted server as untrusted (see Q28); use them to pick a UI (confirm before destructive) but enforce safety yourself.
- **Why the description matters:** it is prompt text. Good descriptions say what the tool does, when not to use it and the argument format (Part 3 Q30 on tool design; Anthropic's post says to prompt-engineer tool definitions like prompts).
- **Error level 1, transport:** process died, pipe closed, HTTP failure. The client sees an exception or timeout, never a JSON-RPC message. Handle with retry or reconnect.
- **Error level 2, protocol:** the request itself is wrong (unknown method, unknown tool, malformed params). It comes back as a JSON-RPC `error` object with a code (for example -32601 method not found, -32602 invalid params; codes from the JSON-RPC convention, from memory). The base spec page I opened states a response has a `result` or an `error`, not both.
- **Error level 3, tool execution:** the tool ran (or tried) and failed: bad business input, API down, no such order. Return a normal result with `isError: true` and a text explanation. The model reads it and can fix arguments or tell the user. A protocol error is usually not shown to the model in a useful way.
- **Design choice:** I validate arguments against the schema and report violations as `isError` results, because the model can self-correct. Some servers raise a protocol error for that instead; check what your host does.

**Example:** `get_order_status` takes `order_id` matching `ORD-dddd`. A call with `42` returns an isError result "42 is not of type 'string'", the model retries with a string. A call to a tool that does not exist returns a JSON-RPC error -32602. If the server process is killed mid-call, neither happens: the client's read times out, and that is the transport level.

**Code:** (run; simplified handler, not the official SDK; validates with jsonschema)
```python
# MCP-style tool definition + handler: protocol errors (JSON-RPC error) vs tool execution errors (isError result).
# Simplified illustration; error-code choices follow common practice (from memory), check the current spec.
import json
from jsonschema import Draft202012Validator

TOOL = {
    "name": "get_order_status",
    "description": "Look up the shipping status of one order by its id. Read-only.",
    "inputSchema": {
        "type": "object",
        "properties": {"order_id": {"type": "string", "pattern": "^ORD-[0-9]{4}$"}},
        "required": ["order_id"], "additionalProperties": False},
    "outputSchema": {  # optional structured output (reported by a guide as added in 2025-06-18)
        "type": "object", "properties": {"status": {"type": "string"}}, "required": ["status"]},
    "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True,
                    "openWorldHint": False},   # hints only, NOT guarantees
}
ORDERS = {"ORD-0001": "shipped", "ORD-0002": "processing"}
validator = Draft202012Validator(TOOL["inputSchema"])

def handle(request):
    """One JSON-RPC 2.0 request dict -> response dict."""
    rid, method, params = request.get("id"), request.get("method"), request.get("params", {})
    if method != "tools/call":
        return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "Method not found"}}
    if params.get("name") != TOOL["name"]:           # protocol level: the call itself is wrong
        return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32602, "message": "Unknown tool: " + str(params.get("name"))}}
    args = params.get("arguments", {})
    errs = sorted(e.message for e in validator.iter_errors(args))
    if errs:                                          # execution level: model can read this and retry
        return {"jsonrpc": "2.0", "id": rid, "result": {"isError": True,
                "content": [{"type": "text", "text": "Invalid arguments: " + "; ".join(errs)}]}}
    status = ORDERS.get(args["order_id"])
    if status is None:                                # business failure, also visible to the model
        return {"jsonrpc": "2.0", "id": rid, "result": {"isError": True,
                "content": [{"type": "text", "text": "No such order: " + args["order_id"]}]}}
    return {"jsonrpc": "2.0", "id": rid, "result": {"isError": False,
            "content": [{"type": "text", "text": json.dumps({"status": status})}],
            "structuredContent": {"status": status}}}

def call(i, name, args):
    return handle({"jsonrpc": "2.0", "id": i, "method": "tools/call", "params": {"name": name, "arguments": args}})

cases = [("ok", "get_order_status", {"order_id": "ORD-0001"}),
         ("bad args", "get_order_status", {"order_id": 42}),
         ("extra arg", "get_order_status", {"order_id": "ORD-0001", "x": 1}),
         ("missing order", "get_order_status", {"order_id": "ORD-9999"}),
         ("unknown tool", "delete_everything", {})]
for i, (label, name, args) in enumerate(cases, 1):
    r = call(i, name, args)
    kind = "PROTOCOL ERROR" if "error" in r else ("isError=True" if r["result"]["isError"] else "ok")
    print(f"{label:14}{kind:16}", (r.get("error") or r["result"])["message" if "error" in r else "content"] if "error" in r else r["result"]["content"][0]["text"])
# the transport level (process died, connection dropped) never reaches handle(): the client sees an exception/timeout
assert "error" in call(9, "nope", {}) and call(9, "get_order_status", {"order_id": "bad"})["result"]["isError"]
Draft202012Validator.check_schema(TOOL["inputSchema"]); Draft202012Validator.check_schema(TOOL["outputSchema"])
print("tests passed")
```
Output (my run):
```
ok            ok               {"status": "shipped"}
bad args      isError=True     Invalid arguments: 42 is not of type 'string'
extra arg     isError=True     Invalid arguments: Additional properties are not allowed ('x' was unexpected)
missing order isError=True     No such order: ORD-9999
unknown tool  PROTOCOL ERROR   Unknown tool: delete_everything
tests passed
```

**Follow-ups:**
- *Why not just raise exceptions?* An exception becomes a protocol error the model may never see; an isError result is feedback inside the loop, the same idea as tool-failure handling in Part 3 Q27.
- *Do you trust outputSchema?* Validate the result on the client too; a server can still return nonsense.
- *Where is idempotency?* Annotations can hint at it, but you enforce it with idempotency keys (Part 3 Q28).

**Common mistakes:** treating annotations as security controls; returning stack traces to the model; using protocol errors for business failures; vague descriptions; forgetting that transport failures need their own retry path.
