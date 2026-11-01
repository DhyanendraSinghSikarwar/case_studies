"""Q19 Azure side: managed feature store entities built offline (nothing is created)."""
import warnings; warnings.filterwarnings("ignore")
import importlib.metadata as md
from azure.ai.ml.entities import FeatureStore, FeatureStoreEntity, FeatureSet, FeatureSetSpecification, DataColumn
print("azure-ai-ml", md.version("azure-ai-ml"))
fs = FeatureStore(name="fs-demo", location="centralindia")
print(type(fs).__name__, fs.name, fs.location)
ent = FeatureStoreEntity(name="account", version="1", index_columns=[DataColumn(name="accountID", type="string")], stage="Development")
print(type(ent).__name__, ent.name, ent.version, [c.name for c in ent.index_columns])
fset = FeatureSet(name="txn_agg", version="1", entities=["azureml:account:1"],
                  specification=FeatureSetSpecification(path="./featureset_spec"), stage="Development")
print(type(fset).__name__, fset.name, fset.version, fset.entities)
