import yaml
head = open("vertex_demo.yaml").read().splitlines()[:1]
doc = next(yaml.safe_load_all(open("vertex_demo.yaml")))
print("first line:", head[0])
print("top-level keys:", sorted(doc))
print("schemaVersion:", doc["schemaVersion"], "| sdkVersion:", doc["sdkVersion"])
print("pipelineInfo:", doc["pipelineInfo"], "| default pipeline_root:", doc["defaultPipelineRoot"])
