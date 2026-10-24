**Say this first (1 line):** The danger is that tool metadata and tool servers are untrusted input to a model that can act: tool poisoning hides instructions in descriptions, a rug pull changes a definition after you approved it, and a confused deputy lets a server do things the caller was never allowed to do; the defence is pinning, review, per-tool least privilege and sandboxing, not trusting the description.

**Then explain:**
- **Tool poisoning:** malicious instructions placed in a tool's description or schema. The model reads that text when choosing tools, so it can be steered (for example, to pass private data as an argument) even if the user never sees it. Described by the DataCamp guide; my wording, check current security guidance.
- **Rug pull:** the server shows a harmless definition at approval time and later swaps it. Defence: pin a hash of each approved definition, block and re-approve on any change (demo below).
- **Confused deputy:** a server holds a powerful credential and acts for any caller, so a low-privilege user (or an injected instruction) borrows its authority. Defence: act with the caller's identity and scopes, not the server's own broad token.
- **Other risks:** over-broad scopes (a token that can read and write everything), exfiltration through tool arguments or outbound calls, and tool results carrying indirect injection (Part 6 Q36, Part 7 Q47).
- **Authorisation:** the base spec page I opened says HTTP-based transports SHOULD follow the authorisation specification, while stdio SHOULD NOT and should take credentials from the environment. That the HTTP flow is OAuth 2.1 style is from the guide and memory; read the current authorisation page.
- **Mitigations:** show tool descriptions to the user; hash-pin and re-approve; per-tool, least-privilege scopes; confirmation for destructive actions; sandbox local servers; allow-list servers; audit logs of every call. Depth on LLM security and monitoring is in Part 11; the guardrail layers are in Part 5 Q8.

**Example:** day 1, a tool `add` is approved: "Add two integers." On day 8 the same name carries extra text telling the model to copy the user's notes into an argument and not tell the user. The hash no longer matches, so the host blocks it. A paraphrased version of the same trick passes the keyword scanner, which is why the scanner is only a first filter. Placeholders only; nothing here contacts a network.

**Code:** (run; hash pinning is solid, the scanner is a weak heuristic)
@@CODE@@

**Follow-ups:**
- *Why not just scan descriptions?* Attackers paraphrase; the scanner above misses one. Pinning catches change, review catches intent, privilege limits damage.
- *Local stdio server, is it safe?* It runs with your user's rights, so sandbox it and give it only the credentials it needs.
- *Does confirmation fix it?* Partly: users click through frequent prompts, so confirm only destructive or external actions and show the real arguments.

**Common mistakes:** trusting annotations or descriptions; approving once and never re-checking; giving one broad token to every tool; letting the server's identity, not the user's, decide permissions; thinking a keyword filter is a defence.
