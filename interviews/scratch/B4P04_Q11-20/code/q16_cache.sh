R=$(mktemp -d /tmp/q16remote.XXXX)
mkdir part1 && cd part1 && git init -q . && dvc init -q && dvc remote add -d loc $R -q
printf 'hello\n' > a.txt; cp a.txt b.txt; printf 'other\n' > c.txt
dvc add a.txt b.txt c.txt >/dev/null 2>&1
echo "--- cache after dvc add (a.txt and b.txt are identical): 2 objects for 3 files"; find .dvc/cache -type f | sort
echo "--- a.txt.dvc"; cat a.txt.dvc
git add -A >/dev/null; git commit -qm v1
echo "--- dvc status -c BEFORE push (cache vs remote)"; dvc status -c 2>&1 | grep -v '^$'
dvc push 2>&1 | tail -1
echo "--- dvc status -c AFTER push"; dvc status -c 2>&1
echo "--- delete a.txt from workspace; dvc status; dvc checkout"
rm a.txt; dvc status 2>&1 | grep -v '^$'; dvc checkout 2>&1 | grep -v '^$'; cat a.txt
echo "--- change c.txt, add, commit: old c.txt object is now unreferenced"
printf 'other v2\n' > c.txt; dvc add c.txt >/dev/null 2>&1; git add -A >/dev/null; git commit -qm v2
echo "cache objects: $(find .dvc/cache -type f | wc -l)"
echo "--- dvc gc -w --dry (dry run)"; dvc gc -w --dry 2>&1 | grep -v '^$'
echo "cache objects after dry run: $(find .dvc/cache -type f | wc -l)"
echo "--- dvc gc -w -f (workspace only: keeps only what the current workspace uses)"; dvc gc -w -f 2>&1 | grep -v '^$'
echo "cache objects after gc: $(find .dvc/cache -type f | wc -l)"
echo "--- but the old c.txt is still in the remote, so it can come back"
git checkout -q HEAD~1 -- c.txt.dvc; dvc pull 2>&1 | grep -v '^$' | tail -2; cat c.txt
cd ..
echo "=== part 2: symlink cache type, edit through the link"
mkdir part2 && cd part2 && git init -q . && dvc init -q && dvc config cache.type symlink
printf 'hello\n' > a.txt; cp a.txt b.txt; dvc add a.txt b.txt >/dev/null 2>&1
ls -l a.txt | awk '{print $1, $9, $10, $11}' | sed "s#$PWD/##"
echo "oops" >> a.txt        # as root the read-only bit does not stop this; as a normal user it usually does
echo "--- dvc status after the edit:"; dvc status 2>&1 | grep -v '^$'
