import json
example = {
  "messages": [
    {"role": "user", "content": "Refund order 4471, it arrived broken."},
    {"role": "assistant", "tool_calls": [
        {"type": "function", "function": {"name": "issue_refund", "arguments": {"order_id": "4471", "reason": "damaged"}}}]},
    {"role": "tool", "name": "issue_refund", "content": "{\"status\": \"ok\"}"},
    {"role": "assistant", "content": "Done: your refund for order 4471 has been issued."},
  ],
  "tools": [{"type": "function", "function": {
      "name": "issue_refund", "description": "Refund a delivered order.",
      "parameters": {"type": "object", "properties": {"order_id": {"type": "string"}, "reason": {"type": "string"}},
                     "required": ["order_id", "reason"]}}}],
}
assert json.loads(json.dumps(example))["messages"][1]["tool_calls"][0]["function"]["name"] == "issue_refund"
print("structure serialises to valid JSON")   # structure check only; field names follow my reading of the TRL docs
