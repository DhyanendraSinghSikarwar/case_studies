import tritonclient.http as h
try: h.InferenceServerClient(url="localhost:8999").is_server_live()
except Exception as e: print("no server running ->", type(e).__name__)
