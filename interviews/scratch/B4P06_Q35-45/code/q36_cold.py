import sys,time,tempfile,pathlib; sys.path.insert(0,"/home/user/case_studies/interviews/scratch/B4P06_Q35-45/code")
import numpy as np
from sklearn.linear_model import LogisticRegression
from skl2onnx import to_onnx
from q36_manager import ModelManager
X=np.random.default_rng(0).normal(size=(50,4)).astype(np.float32); m=LogisticRegression().fit(X,(X[:,0]>0).astype(int))
d=pathlib.Path(tempfile.mkdtemp()); p=d/"m.onnx"; p.write_bytes(to_onnx(m,X[:1],target_opset=17,options={id(m):{"zipmap":False}}).SerializeToString())
mm=ModelManager(lambda t:str(p),2)
t=time.perf_counter(); s=mm.get("a"); cold=time.perf_counter()-t
t=time.perf_counter(); mm.get("a"); warm=time.perf_counter()-t
t=time.perf_counter(); s.run(None,{"X":X[:1]}); inf=time.perf_counter()-t
print(f"cold get {cold*1000:.2f} ms, cached get {warm*1000:.4f} ms, one inference {inf*1000:.3f} ms (this sandbox only)")
