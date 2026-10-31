# q33_adapter.py - one tiny interface (put/list/get), two adapters. Run by the driver with the right venv.
# usage: q33_adapter.py azure|gcs PORT put|roundtrip KEY FILE
import sys, os, hashlib, json
class ArtifactStore:                      # the interface the training code sees
    def put(self, key, data): raise NotImplementedError
    def get(self, key): raise NotImplementedError
    def list(self): raise NotImplementedError
class AzureBlobStore(ArtifactStore):      # emulator: Azurite with its documented public dev account
    def __init__(self, port):
        from azure.storage.blob import BlobServiceClient
        key = "Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw=="
        cs = f"DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey={key};BlobEndpoint=http://127.0.0.1:{port}/devstoreaccount1;"
        self.c = BlobServiceClient.from_connection_string(cs).get_container_client("mlartifacts")
        try: self.c.create_container()
        except Exception: pass
    def put(self, key, data): self.c.upload_blob(key, data, overwrite=True)
    def get(self, key): return self.c.get_blob_client(key).download_blob().readall()
    def list(self): return sorted(b.name for b in self.c.list_blobs())
class GcsStore(ArtifactStore):            # emulator: gcp-storage-emulator, anonymous credentials
    def __init__(self, port):
        os.environ["STORAGE_EMULATOR_HOST"] = f"http://127.0.0.1:{port}"
        from google.cloud import storage
        from google.auth.credentials import AnonymousCredentials
        self.b = storage.Client(project="demo", credentials=AnonymousCredentials()).bucket("mlartifacts")
    def put(self, key, data): self.b.blob(key).upload_from_string(data)
    def get(self, key): return self.b.blob(key).download_as_bytes()
    def list(self): return sorted(x.name for x in self.b.client.list_blobs("mlartifacts"))
kind, port, key, path = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
store = {"azure": AzureBlobStore, "gcs": GcsStore}[kind](port)
data = open(path, "rb").read()
store.put(key, data)
back = store.get(key)
print(json.dumps({"adapter": type(store).__name__, "listed": store.list(), "sha256_in": hashlib.sha256(data).hexdigest()[:16],
                  "sha256_back": hashlib.sha256(back).hexdigest()[:16], "same": back == data}))
