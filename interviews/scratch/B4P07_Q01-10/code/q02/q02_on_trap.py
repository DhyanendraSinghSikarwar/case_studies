import yaml
print(yaml.safe_load("on: push"))
wf = yaml.safe_load(open("q02_good.yml"))
print("keys:", list(wf))
print("wf.get('on'):", wf.get("on"))
print("wf.get(True):", wf.get(True))
def trigger(wf):                      # safe reader: accept both spellings
    return wf.get("on", wf.get(True))
print("safe reader:", trigger(wf))
print("quoted key:", list(yaml.safe_load('"on": push')))
