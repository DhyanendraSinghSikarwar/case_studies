import json, fnmatch
policy = json.load(open("trust_policy.json"))
cond = policy["Statement"][0]["Condition"]
PIN = cond["StringLike"]["token.actions.githubusercontent.com:sub"]
AUD = cond["StringEquals"]["token.actions.githubusercontent.com:aud"]

def allowed(claims, sub_pattern, aud=AUD):
    # StringLike semantics: * and ? wildcards, case-sensitive
    return claims["aud"] == aud and fnmatch.fnmatchcase(claims["sub"], sub_pattern)

samples = {
  "prod deploy job":      {"aud": "sts.amazonaws.com", "sub": "repo:acme/churn-model:environment:production"},
  "feature branch job":   {"aud": "sts.amazonaws.com", "sub": "repo:acme/churn-model:ref:refs/heads/feature/x"},
  "PR job":               {"aud": "sts.amazonaws.com", "sub": "repo:acme/churn-model:pull_request"},
  "staging env job":      {"aud": "sts.amazonaws.com", "sub": "repo:acme/churn-model:environment:staging"},
  "other repo job":   {"aud": "sts.amazonaws.com", "sub": "repo:attacker/churn-model:environment:production"},
  "wrong audience":       {"aud": "sts.example.com",   "sub": "repo:acme/churn-model:environment:production"},
}
policies = {"pinned": PIN, "repo-wide": "repo:acme/churn-model:*", "unpinned": "repo:*"}
print(f"{'claims':22}" + "".join(f"{k:>10}" for k in policies))
for name, c in samples.items():
    print(f"{name:22}" + "".join(f"{('ALLOW' if allowed(c, p) else 'deny'):>10}" for p in policies.values()))
