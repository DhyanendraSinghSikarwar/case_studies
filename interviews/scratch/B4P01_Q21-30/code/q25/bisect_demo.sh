set -e
D=$(mktemp -d); cd "$D"
export GIT_AUTHOR_DATE="2026-01-01T00:00:00+0000" GIT_COMMITTER_DATE="2026-01-01T00:00:00+0000"   # fixed dates: same hashes every run
git init -q -b main; git config user.email a@b.c; git config user.name demo
# the "model": threshold classifier on 200 seeded points; accuracy must stay >= 0.85
cat > train.py <<'PY'
import random, json
random.seed(0)
cfg = json.load(open("cfg.json"))
pts = [(random.random() * 0.55, 0) for _ in range(100)] + [(0.45 + random.random() * 0.55, 1) for _ in range(100)]
# class 0 lives in [0,0.55), class 1 in [0.45,1): a little overlap, so ~0.9 accuracy at threshold 0.5
hits = sum((x * cfg["scale"] >= cfg["threshold"]) == bool(y) for x, y in pts)
print(f"accuracy={hits/len(pts):.3f}")
PY
cat > check.sh <<'SH'
#!/bin/sh
# exit 0 = good, 1 = bad, 125 = cannot test this commit (skip)
python3 -I -m py_compile train.py 2>/dev/null || exit 125
acc=$(python3 -I train.py | sed 's/accuracy=//')
python3 -I -c "import sys; sys.exit(0 if float('$acc') >= 0.85 else 1)"
SH
chmod +x check.sh
echo '{"threshold": 0.5, "scale": 1.0}' > cfg.json
git add .; git commit -qm "v1.0 baseline"; git tag v1.0
echo "baseline: $(python3 -I train.py)"
for i in 1 2 3 4 5 6 7 8 9 10 11 12; do
  case $i in
    6) echo 'def broken(:' >> train.py ;;                                   # c6: does not even compile
    7) sed -i '$d' train.py ;;                                              # c7: fixes the syntax error
    9) echo '{"threshold": 0.5, "scale": 0.6}' > cfg.json ;;               # c9: the real culprit (bad scale)
    *) echo "# note $i" >> README.md ;;
  esac
  git add -A; git commit -qm "c$i"
done
echo "HEAD:     $(python3 -I train.py)"
echo; echo '$ git bisect start HEAD v1.0 && git bisect run ./check.sh'
git bisect start HEAD v1.0 >/dev/null
git bisect run ./check.sh > run.log 2>&1 || true
grep -E "^(Bisecting|running)|is the first bad commit|^    c[0-9]+$" run.log | sed -E 's#^running .*check.sh.*#running ./check.sh#; s/^[0-9a-f]{40} is/<sha> is/'
echo "commits tested by the script (one of them skipped): $(git bisect log | grep -c "^git bisect \(good\|bad\|skip\)")"
git bisect log | grep -E "^(# (good|bad|skip)|git bisect (good|bad|skip))" | sed -E 's/\[[0-9a-f]{40}\]//; s/git bisect (good|bad|skip) [0-9a-f]{40}/git bisect \1 <sha>/' | grep '^#' 
git bisect reset >/dev/null 2>&1
echo; echo '--- a flaky check blames the wrong commit (deterministic demo: it lies once, on its 3rd call) ---'
cat > flaky.sh <<'SH'
#!/bin/sh
n=$(cat /tmp/_flaky_count 2>/dev/null || echo 0); n=$((n+1)); echo $n > /tmp/_flaky_count
[ "$n" -eq 3 ] && exit 1          # lies once: reports 'bad' for a good commit
exec ./check.sh
SH
chmod +x flaky.sh; rm -f /tmp/_flaky_count
git bisect start HEAD v1.0 >/dev/null
git bisect run ./flaky.sh > flaky.log 2>&1 || true
grep -E "first bad|could be any|^[0-9a-f]{40} |^    c[0-9]+$" flaky.log | sed -E "s/^[0-9a-f]{40} /<sha> /"
git bisect reset >/dev/null 2>&1; rm -f /tmp/_flaky_count
git --version
