import yaml
cfg = yaml.safe_load(open("prefect.yaml"))
dep = cfg["deployments"][0]
print("deployment:", dep["name"], "| entrypoint:", dep["entrypoint"], "| pool:", dep["work_pool"]["name"])
print("schedule:", dep["schedules"][0], "| parameters:", dep["parameters"])
file, func = dep["entrypoint"].split(":")
import ast
tree = ast.parse(open(file).read())
print("entrypoint function found in", file, ":", any(isinstance(n, ast.FunctionDef) and n.name == func for n in ast.walk(tree)))
