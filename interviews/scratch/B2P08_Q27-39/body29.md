**Say this first (1 line):** An MCP-style server is a loop that reads one JSON-RPC 2.0 message per line, dispatches on `method` (initialize, tools/list, tools/call), and writes a response with the same `id`; the client sends requests with unique ids, matches responses, and sends notifications without an id.

**Then explain:**
- **Message shapes (from the opened spec page, 2025-06-18):** a request has a non-null, unique `id`, a `method` and optional `params`; a response carries that `id` and either `result` or `error`, never both; a notification has no `id` and gets no reply.
- **Lifecycle:** the client sends `initialize` (protocol version, capabilities, client info), the server replies with its version, capabilities and server info, and the client sends an `initialized` notification. The exact parameter names here are from memory and the lifecycle page was not opened: check the current spec.
- **Then:** `tools/list` returns tool definitions (Q27), `tools/call` runs one. Unknown method or tool is a JSON-RPC error; a tool that ran and failed is a result with `isError: true`.
- **Stdio rule:** over a subprocess pipe, stdout must carry only protocol messages. Logging to stdout corrupts the stream, a classic bug (reported by the guide); log to stderr.
- **Honest label:** this is a simplified teaching version. No capability negotiation, pagination, version negotiation, cancellation, timeouts or schema validation (Q27 shows validation). In a real project use the official SDK.

**Example:** the client starts the server as a child process, initializes, lists one tool `add`, calls `add(2, 3)` and gets "5", then makes three bad calls: wrong argument type (isError result), unknown tool (-32602) and unknown method (-32601). All checked by assertions in the run below.

**Code:** (run; stdlib only; the server runs as a subprocess of the same file; simplified, not full spec compliance, not the official SDK)
@@CODE@@

**Follow-ups:**
- *What changes for HTTP?* The same JSON-RPC messages travel over HTTP (the guide describes a Streamable HTTP transport) and authorisation applies; the opened page says HTTP transports SHOULD follow the authorisation spec.
- *How would you add concurrency?* Ids already allow out-of-order responses: keep a dict of pending futures keyed by id and read responses on a separate thread.
- *What if the server hangs?* Per-request timeouts and a kill-and-restart path (Q30).

**Common mistakes:** printing debug text to stdout; reusing or omitting ids; sending a response to a notification; mixing up protocol errors and isError results; claiming a toy like this is spec-compliant.
