from oidc_diag import diagnose

ISS = "https://token.actions.githubusercontent.com"
TRUST = {"sub": ["repo:acme/churn:environment:production"], "aud": "sts.amazonaws.com", "iss": ISS}

def claims(sub, aud="sts.amazonaws.com", iss=ISS):
    return {"sub": sub, "aud": aud, "iss": iss}

def test_match_gives_no_findings():
    assert diagnose(claims("repo:acme/churn:environment:production"), TRUST) == []

def test_branch_job_without_environment():
    f = diagnose(claims("repo:acme/churn:ref:refs/heads/main"), TRUST)
    assert len(f) == 1 and "ref token" in f[0]

def test_environment_mismatch_when_trust_pins_branch():
    trust = {**TRUST, "sub": ["repo:acme/churn:ref:refs/heads/main"]}
    f = diagnose(claims("repo:acme/churn:environment:production"), trust)
    assert "environment form" in f[0]

def test_pull_request_token():
    f = diagnose(claims("repo:acme/churn:pull_request"), TRUST)
    assert "pull_request token" in f[0]

def test_other_repo_and_wrong_audience():
    f = diagnose(claims("repo:acme/other:environment:production", aud="sts.example.com"), TRUST)
    assert any("aud mismatch" in x for x in f) and any("sub repo" in x for x in f)
