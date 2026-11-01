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
