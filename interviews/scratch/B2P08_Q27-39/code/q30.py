# MCP host managing many servers: one client per server, namespaced aggregation, collision handling,
# relevance filtering, per-server timeouts, and a token-cost proxy (word count, NOT a real tokenizer). All servers are MOCKS.
import re, time, concurrent.futures as cf

class MockServer:
    def __init__(self, name, tools, delay=0.0): self.name, self.tools, self.delay = name, tools, delay
    def list_tools(self, cursor=None, page=2):    # pagination: 2 tools per page, cursor = offset
        time.sleep(self.delay); start = int(cursor or 0)
        nxt = start + page if start + page < len(self.tools) else None
        return self.tools[start:start + page], nxt
    def call(self, tool, args): return f"{self.name}:{tool}({args})"

def T(n, d): return {"name": n, "description": d}
SERVERS = [
    MockServer("github", [T("search", "Search issues and pull requests in a repository by keyword or label"), T("create_issue", "Create a new issue in a repository with title and body"),
                          T("list_prs", "List open pull requests for a repository"), T("merge_pr", "Merge a pull request after checks pass")]),
    MockServer("files", [T("search", "Search files on disk by name pattern"), T("read_file", "Read the contents of a file from disk"), T("write_file", "Write text to a file on disk")]),
    MockServer("calendar", [T("list_events", "List calendar events for a date range"), T("create_event", "Create a calendar event with attendees")]),
    MockServer("slow", [T("ping", "A server that takes too long to answer")], delay=2.0),
]

def fetch_all(server, timeout):
    """Follow pagination cursors; the whole listing is bounded by a per-server timeout."""
    def run():
        out, cur = [], None
        while True:
            page, cur = server.list_tools(cur); out += page
            if cur is None: return out
    ex = cf.ThreadPoolExecutor(1)
    try: return ex.submit(run).result(timeout=timeout)
    finally: ex.shutdown(wait=False)       # do NOT join the stuck worker (a `with` block would wait for it)

class Host:
    def __init__(self, servers, timeout=0.5):
        self.clients = {s.name: s for s in servers}      # one client/connection per server
        self.registry, self.failed = {}, []
        for name, s in self.clients.items():
            try: tools = fetch_all(s, timeout)
            except cf.TimeoutError: self.failed.append(name); continue   # one bad server must not block the host
            for t in tools:
                self.registry[f"{name}__{t['name']}"] = dict(t, server=name)  # prefix avoids collisions
    def call(self, qualified, args): 
        t = self.registry[qualified]; return self.clients[t["server"]].call(t["name"], args)

def cost(tools):  # crude proxy: words in name + description (a real count needs the model's tokenizer)
    return sum(len(re.findall(r"\w+", t.get("qname", "") + " " + t["description"])) + 3 for t in tools)

t0 = time.time(); host = Host(SERVERS); elapsed = time.time() - t0
print("servers failed/timed out:", host.failed, "| host start took under 1.5s (slow server is 2s):", elapsed < 1.5)
print("naive names would collide on:", sorted({t["name"] for t in host.registry.values() if sum(u["name"] == t["name"] for u in host.registry.values()) > 1}))
print("aggregated:", sorted(host.registry))
all_tools = [dict(t, qname=q) for q, t in host.registry.items()]
def relevant(query, tools, k=3):   # crude keyword filter standing in for tool search / server routing
    q = set(re.findall(r"\w+", query.lower()))
    scored = sorted(tools, key=lambda t: -len(q & set(re.findall(r"\w+", (t["qname"] + " " + t["description"]).lower()))))
    return [t for t in scored[:k] if q & set(re.findall(r"\w+", (t["qname"] + " " + t["description"]).lower()))]
sel = relevant("create a calendar event", all_tools)
print("query: 'create a calendar event' ->", [t["qname"] for t in sel])
print(f"tool-definition cost proxy (words): all={cost(all_tools)} filtered={cost(sel)} ({100*(1-cost(sel)/cost(all_tools)):.0f}% less, toy numbers)")
print(host.call("calendar__create_event", {"title": "demo"}))
assert elapsed < 1.5 and "slow" in host.failed and "github__search" in host.registry and "files__search" in host.registry
assert sel[0]["qname"] == "calendar__create_event" and cost(sel) < cost(all_tools)
print("tests passed")
