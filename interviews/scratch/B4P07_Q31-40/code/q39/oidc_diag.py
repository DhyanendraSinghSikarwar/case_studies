"""Explain why a cloud trust policy rejected a GitHub OIDC token, using sub/aud/iss only."""
from fnmatch import fnmatchcase

def sub_shape(sub):
    parts = sub.split(":")
    return parts[2] if len(parts) > 2 else "unknown"    # ref | environment | pull_request

def diagnose(claims, trust):
    """claims: decoded token claims. trust: {'sub': [patterns], 'aud': str, 'iss': str}. Returns list of findings."""
    findings = []
    if claims.get("iss") != trust["iss"]:
        findings.append(f"iss mismatch: token {claims.get('iss')!r} vs trust {trust['iss']!r}")
    if claims.get("aud") != trust["aud"]:
        findings.append(f"aud mismatch: token {claims.get('aud')!r} vs trust {trust['aud']!r} (check the audience input of the login action)")
    sub = claims["sub"]
    if not any(fnmatchcase(sub, p) for p in trust["sub"]):
        shape = sub_shape(sub)
        want_repo = trust["sub"][0].split(":")[1]
        got_repo = sub.split(":")[1]
        if got_repo != want_repo:
            findings.append(f"sub repo {got_repo!r} is not {want_repo!r} (renamed, moved or forked repo?)")
        elif shape == "environment":
            findings.append(f"sub {sub!r} uses the environment form; a job with `environment:` no longer sends ref:..., "
                            f"so a trust pinned to a branch will not match")
        elif shape == "pull_request":
            findings.append(f"sub {sub!r} is a pull_request token; trust only allows {trust['sub']} (usually correct: PRs should not assume deploy roles)")
        elif shape == "ref":
            findings.append(f"sub {sub!r} is a ref token for another branch or tag than the trust allows {trust['sub']}")
        else:
            findings.append(f"sub {sub!r} matches none of {trust['sub']}")
    return findings
