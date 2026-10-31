set -e
head -c 2000000 /dev/zero | tr '\0' 'a' > /tmp/big.bin      # stand-in for a big file
echo "=== Git LFS (local only, no host, no push)"
mkdir lfs && cd lfs && git init -q . && git lfs install --local >/dev/null
git lfs track "*.bin"
cp /tmp/big.bin . && git add .gitattributes big.bin && git commit -qm lfs
echo "--- .gitattributes"; cat .gitattributes
echo "--- what Git stores (the pointer)"; git cat-file -p HEAD:big.bin
git lfs ls-files
cd ..
echo "=== DVC"
mkdir dvc && cd dvc && git init -q . && dvc init -q
cp /tmp/big.bin . && dvc add big.bin 2>&1 | grep -v -e '^$' -e 'track' -e 'git add' -e autostage
echo "--- big.bin.dvc"; cat big.bin.dvc
echo "--- cache"; find .dvc/cache -type f
