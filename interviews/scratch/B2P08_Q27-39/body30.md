**Say this first (1 line):** The host runs one client per server connection, merges every server's tools into one registry under server-prefixed names so duplicates cannot collide, and tries hard not to put all those definitions in the model's context: it filters to relevant servers or tools, or loads definitions on demand through tool search.

**Then explain:**
- **Connections:** the DataCamp guide says each client holds one connection to one server and a host can run several clients; the opened spec page names the host/client/server split only at component level. Keep each connection's lifecycle, timeout and restart policy separate, so one slow or dead server does not stall the rest (the demo marks a 2-second server as failed after 0.5 seconds).
- **Aggregation and collisions:** two servers may both expose `search`. Prefix with the server name (`github__search`, `files__search`) and route calls back by the prefix. The prefix also tells the model which system it is touching, and lets you apply per-server permissions.
- **Context bloat:** every definition is prompt text paid on every call, and many similar tools confuse the model. Part 3 Q30 covers the too-many-tools problem; here the host-level fixes are:
  - route by server first (a calendar question never sees GitHub tools);
  - **deferred loading or tool search** (named by the guide; I do not quote its token-saving figure): the model sees a small search tool and pulls full definitions only for matches. Check what your model provider currently supports;
  - short, distinct descriptions.
- **Operational details:** `tools/list` can be paginated with a cursor (from memory), so follow cursors with a limit; apply a timeout per server and per call; re-list when a server signals its tools changed, and re-run approval and hash checks (Q28).
- **Estimate before you ship:** count definition tokens with the real tokenizer. The demo uses a word-count proxy, so its percentages are toy numbers.

**Example:** four mock servers expose 9 usable tools (the slow one is dropped). Names `search` collide between github and files, resolved by prefixes. For "create a calendar event" a crude keyword filter keeps 3 tools; the word-count proxy falls from 108 to 36 words. Note the filter's second pick, `github__create_issue`, matched only the word "create": keyword filters are noisy, so real systems use embeddings or let the model search.

**Code:** (run; all servers are mocks; word count is not a tokenizer)
@@CODE@@

**Follow-ups:**
- *Prefix or let the model disambiguate?* Prefix. Silent overwrite of a same-named tool is a security bug as well as a correctness bug.
- *When does filtering hurt?* When the filter drops the tool the model needed; log misses and keep a fallback "search all tools" step.
- *Trust per server?* Different: a vetted internal server and a community one should have different scopes and approval rules.

**Common mistakes:** loading every server's tools into every request; letting later servers overwrite earlier names; no timeout on startup listing; ignoring pagination; measuring bloat in words instead of tokens and never re-measuring.
