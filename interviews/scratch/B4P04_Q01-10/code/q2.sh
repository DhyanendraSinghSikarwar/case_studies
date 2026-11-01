set -e
export PATH=/tmp/claude-0/ven/v/bin:$PATH
W=$(mktemp -d); R=$(mktemp -d); cd $W
git init -q; git config user.email a@b.c; git config user.name demo
python3 -I -c "
open('data.csv','w').write('x,y\n'+''.join(f'{i},{i%2}\n' for i in range(500)))"
dvc init -q; dvc add -q data.csv
dvc remote add -d localstore $R/store
dvc remote add -q s3demo s3://my-bucket/dvcstore
git add -A; git commit -qm init
echo "--- .dvc/config"; cat .dvc/config
echo "--- push 1"; dvc push
echo "--- push 2"; dvc push
echo "--- remote layout"; (cd $R/store; find . -type f | sort)
echo "--- add a secret-ish setting to local config"
dvc remote modify s3demo region us-east-1
dvc remote modify --local s3demo access_key_id FAKE_KEY_FOR_DEMO
echo "--- .dvc/config after region edit"; cat .dvc/config
echo "--- .dvc/config.local"; cat .dvc/config.local
echo "--- gitignore in .dvc"; cat .dvc/.gitignore
echo "--- delete workspace file and cache"
rm data.csv; rm -rf .dvc/cache
ls
echo "--- dvc status -c"; dvc status -c || true
echo "--- pull"; dvc pull
ls; wc -l data.csv
