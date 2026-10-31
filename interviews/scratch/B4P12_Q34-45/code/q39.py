# Q39: LLM boundary threat model; every threat needs a control and an owner.
M = [
 ("prompt injection via retrieved HR text", "tool call is low-priv; human approval for writes; retrieved text marked untrusted", "platform security"),
 ("over-broad ticketing tool permission", "tool scope = create ticket only, per-user identity", "platform team"),
 ("data exfil via logs", "redact PII before logging; log retention limit", "data protection office"),
 ("data exfil via answers", "output filter + egress allow-list", "platform security"),
 ("cross-user retrieval leak", "identity-propagated retrieval, ACL filter at query time", "search/RAG team"),
 ("API key theft", "secret manager, short-lived creds, rotation", "platform team"),
 ("supply-chain (model/lib)", "pinned hashes, signed artifacts, scan in CI", "platform security"),
]
def validate(rows):
    errs = [r[0] for r in rows if not r[1].strip() or not r[2].strip()]
    assert not errs, errs
    return len(rows)
print("threats with control and owner:", validate(M))
for r in M: print(f"- {r[0]:40s} owner: {r[2]}")
try: validate(M + [("model weights leaked", "", "")])
except AssertionError as e: print("rejected incomplete row:", e)
# tiny retrieval ACL test
docs = [("d1", {"hr"}), ("d2", {"all"}), ("d3", {"payroll"})]
def retrieve(groups): return [d for d, acl in docs if acl & (groups | {"all"})]
assert retrieve({"hr"}) == ["d1", "d2"] and "d3" not in retrieve({"hr"})
print("ACL test ok: hr user sees", retrieve({"hr"}))
