import yaml
wf = yaml.safe_load(open("release.yml"))
for name, job in wf["jobs"].items():
    env = job.get("environment")
    print(f"{name:18} needs={job.get('needs', '-')!s:16} environment={env['name'] if isinstance(env, dict) else env}")
