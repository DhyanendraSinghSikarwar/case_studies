import yaml, sys
m = yaml.safe_load(open(sys.argv[1]))
BROAD = {"Owner", "Contributor", "roles/owner", "roles/editor"}
need = {"job_creator", "job_runs_as", "image_pull", "output_write"}
for cloud, rows in m.items():
    assert set(rows) == need, (cloud, set(rows) ^ need)
    for k, r in rows.items():
        assert {"identity", "role", "scope"} <= set(r), (cloud, k)
        assert r["role"] not in BROAD, (cloud, k, "too broad", r["role"])
    # the identity that reads data must not be the human/CI creator
    assert rows["job_creator"]["identity"] != rows["job_runs_as"]["identity"], cloud
    print(cloud, "ok:", len(rows), "duties,",
          "creator != runtime identity:", rows["job_creator"]["identity"] != rows["job_runs_as"]["identity"])
# negative test: a lazy matrix must fail
bad = {"azure_ml": {k: {"identity": "me", "role": "Contributor", "scope": "subscription"} for k in need}}
try:
    for k, r in bad["azure_ml"].items():
        assert r["role"] not in BROAD, f"{k}: broad role {r['role']}"
    assert bad["azure_ml"]["job_creator"]["identity"] != bad["azure_ml"]["job_runs_as"]["identity"], "creator == runtime identity"
except AssertionError as e:
    print("lazy matrix rejected:", e)
