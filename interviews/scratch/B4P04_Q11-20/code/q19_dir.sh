R=$(mktemp -d /tmp/q19remote.XXXX)
mkdir producer consumer
cd producer && git init -q . && dvc init -q && dvc remote add -d loc $R -q
mkdir -p images && for i in 1 2 3 4; do echo "image-$i" > images/img$i.txt; done
dvc add images >/dev/null 2>&1
echo "--- images.dvc"; cat images.dvc
echo "--- cache: one .dir manifest + one object per file"; find .dvc/cache -type f | sed 's#.dvc/cache/files/md5/##' | sort
M=$(grep md5 images.dvc | head -1 | awk '{print $3}'); echo "--- manifest content ($M)"; cat .dvc/cache/files/md5/${M:0:2}/${M:2}; echo
git add -A >/dev/null; git commit -qm v1; git tag v1; dvc push 2>&1 | tail -1
echo "=== change ONE file, add again"
echo "image-3 edited" > images/img3.txt; dvc add images >/dev/null 2>&1
echo "new dir hash:"; grep md5 images.dvc | head -1
echo "cache objects: $(find .dvc/cache -type f | wc -l)  (3 unchanged files reused, +1 file, +1 manifest)"
git add -A >/dev/null; git commit -qm v2; git tag v2; dvc push 2>&1 | tail -1
P=$PWD; cd ../consumer && git init -q . && dvc init -q
echo "=== dvc get (plain copy, no link to the source repo)"
dvc get $P images --rev v1 -o got_v1 2>&1 | tail -1; ls got_v1; cat got_v1/img3.txt
echo "=== dvc import (copy + a .dvc file that pins repo and rev)"
dvc import $P images --rev v1 -o imported 2>&1 | tail -1; cat imported.dvc
echo "=== dvc.api.open: stream one file of a pinned version, no checkout"
python -I -c "
import dvc.api
for rev in ('v1', 'v2'):
    with dvc.api.open('images/img3.txt', repo='$P', rev=rev) as f: print(rev, '->', f.read().strip())
"
echo "=== dvc update to v2"
dvc update imported.dvc --rev v2 2>&1 | tail -1; cat imported/img3.txt
