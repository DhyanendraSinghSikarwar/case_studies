import warnings; warnings.filterwarnings("ignore")
import azure.ai.ml as m
from azure.ai.ml import MLClient
from azure.ai.ml.entities import Workspace
from azure.identity import DefaultAzureCredential
print("azure-ai-ml", m.__version__)

SUB = "00000000-0000-0000-0000-000000000000"   # fake subscription id
RG = "rg-ml-dev"
ws = Workspace(
    name="mlw-dev-cin",
    location="centralindia",
    display_name="ML dev workspace",
    description="offline entity only; nothing created",
    public_network_access="Disabled",
    tags={"owner": "ml-platform", "env": "dev"},
)
print("entity:", ws.name, ws.location, "public_network_access =", ws.public_network_access)
# Companion resources are NOT created by building the entity; they are None until you set them
for k in ("storage_account", "key_vault", "container_registry", "application_insights"):
    print(f"  {k:22} ->", getattr(ws, k))
# What the workspace asset ID of a real one looks like (built by hand, as a string)
print("ARM id shape:", f"/subscriptions/{SUB}/resourceGroups/{RG}/providers/Microsoft.MachineLearningServices/workspaces/{ws.name}")

# MLClient needs 4 things: a credential, subscription, resource group, workspace name
try:
    MLClient(credential=None, subscription_id=SUB, resource_group_name=RG, workspace_name=ws.name)
except Exception as e:
    print("MLClient(credential=None):", type(e).__name__, "-", str(e)[:110])
# DefaultAzureCredential constructs offline; asking for a token with only local sources fails clearly
cred = DefaultAzureCredential(exclude_managed_identity_credential=True)
print("credential built:", type(cred).__name__)
try:
    cred.get_token("https://management.azure.com/.default")
except Exception as e:
    print("get_token:", type(e).__name__, "-", str(e).splitlines()[0][:100])
