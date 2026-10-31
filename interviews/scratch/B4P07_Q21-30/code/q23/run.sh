V=/tmp/claude-0/b7p07/v/bin
D=$(dirname "$(readlink -f "$0")")
cd $D && echo '$ pytest -q -p no:cacheprovider test_data_checks.py' && PYTHONDONTWRITEBYTECODE=1 $V/pytest -q -p no:cacheprovider test_data_checks.py
$V/python -I - <<'PY'
import sys; sys.path.insert(0, ".")
import pandas as pd
from data_checks import check_frame
df = pd.DataFrame({"customer_id":[1,2,2,4,5,6],"age":[25,250,33,58,29,61],"plan":["basic","gold","pro","basic","plus","pro"],
 "monthly_spend":[None,25.5,-1.0,12.0,None,55.0],"churned":[0,1,0,0,1,0]})
print("corrupted frame ->")
for m in check_frame(df): print("  FAIL", m)
PY
