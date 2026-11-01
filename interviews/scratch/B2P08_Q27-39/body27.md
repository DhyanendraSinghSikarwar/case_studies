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
@@CODE@@

**Follow-ups:**
- *Why not just raise exceptions?* An exception becomes a protocol error the model may never see; an isError result is feedback inside the loop, the same idea as tool-failure handling in Part 3 Q27.
- *Do you trust outputSchema?* Validate the result on the client too; a server can still return nonsense.
- *Where is idempotency?* Annotations can hint at it, but you enforce it with idempotency keys (Part 3 Q28).

**Common mistakes:** treating annotations as security controls; returning stack traces to the model; using protocol errors for business failures; vague descriptions; forgetting that transport failures need their own retry path.
