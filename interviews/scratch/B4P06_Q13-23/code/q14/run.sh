. "$(dirname "$0")/../env.sh"; D=$(dirname "$0")
R=$W/q14/model_repository
(cd $W/q14 && find model_repository | sort)
$PY -I $D/check_repo.py $R
echo "--- broken copy (config dims 5 instead of 4):"
$PY -I $D/check_repo.py $W/q14/bad | grep -E "FAIL|PROBLEMS|ALL"
