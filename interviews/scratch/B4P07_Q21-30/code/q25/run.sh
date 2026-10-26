V=/tmp/claude-0/b7p07/v/bin
D=$(dirname "$(readlink -f "$0")")
W=/tmp/claude-0/b7_q21_30/q25; rm -rf $W; mkdir -p $W; cd $W
git init -q . && git config user.email t@example.com && git config user.name t
echo a > f; git add f; git commit -qm "Initial training pipeline"; git tag -a model-v3.0.0 -m v3
echo b > f; git commit -qam "Add tenure feature"; echo c > f; git commit -qam "Retrain on October data"; git tag -a model-v4.0.0 -m v4
echo '$ git log --pretty=format:%s model-v3.0.0..model-v4.0.0 > commits.txt'
git log --pretty=format:%s model-v3.0.0..model-v4.0.0 > commits.txt; cat commits.txt; echo
echo '$ python3 -I release_notes.py old_metrics.json new_metrics.json model-v3.0.0 model-v4.0.0 --commits commits.txt'
$V/python -I $D/release_notes.py $D/old_metrics.json $D/new_metrics.json model-v3.0.0 model-v4.0.0 --commits commits.txt
