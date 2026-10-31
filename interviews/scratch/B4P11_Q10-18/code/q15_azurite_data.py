"""Azurite blob emulator + offline Azure ML Datastore/Data entities. Storage API shape only: no Entra, no Azure ML."""
import sys, warnings; warnings.filterwarnings("ignore")
from azure.storage.blob import BlobServiceClient
from azure.ai.ml import Input
from azure.ai.ml.entities import Data, AzureBlobDatastore
import azure.ai.ml as m

PORT = sys.argv[1]
# Documented PUBLIC Azurite dev account; not a secret.
KEY = "Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw=="
cs = (f"DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey={KEY};"
      f"BlobEndpoint=http://127.0.0.1:{PORT}/devstoreaccount1;")
bsc = BlobServiceClient.from_connection_string(cs)
c = bsc.create_container("train-data")
c.upload_blob("churn/2026-10/part-0.csv", b"id,y\n1,0\n2,1\n", overwrite=True)
print("azure-ai-ml", m.__version__, "| blobs:", [b.name for b in c.list_blobs()])
print("round trip:", c.get_blob_client("churn/2026-10/part-0.csv").download_blob().readall())

# Offline entities: nothing is registered anywhere.
ds = AzureBlobDatastore(name="churn_blob", account_name="devstoreaccount1", container_name="train-data")
print("datastore:", ds.name, ds.type, ds.account_name, ds.container_name, "| credentials:", type(ds.credentials).__name__)
folder = "azureml://datastores/churn_blob/paths/churn/2026-10/"
d1 = Data(name="churn-raw", version="1", type="uri_folder", path=folder)
d2 = Data(name="churn-raw", version="2", type="uri_file", path=folder + "part-0.csv")
for d in (d1, d2):
    print("Data", d.name, "v" + d.version, d.type, d.path)
for mode in ("ro_mount", "download"):
    i = Input(type="uri_folder", path="azureml:churn-raw:1", mode=mode)
    print("Input mode:", i.mode, "->", i.path)
