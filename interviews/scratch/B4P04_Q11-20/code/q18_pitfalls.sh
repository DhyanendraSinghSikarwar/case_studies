git init -q . && dvc init -q
printf '{"scale": 2}\n' > config.json
printf '1\n2\n3\n' > data.txt
cat > make.py <<'P'
import json
cfg = json.load(open("config.json"))          # <- reads a file the stage did not declare
vals = [int(v) * cfg["scale"] for v in open("data.txt")]
open("out.txt", "w").write(f"sum={sum(vals)}\n")
P
cat > dvc.yaml <<'Y'
stages:
  make:
    cmd: python make.py
    deps:
      - make.py
      - data.txt          # config.json is MISSING here
    outs:
      - out.txt
Y
echo "=== 1. broken pipeline"; dvc repro 2>&1 | grep -v -e '^$' -e autostage -e 'git add' -e 'To track' -e 'To enable'; cat out.txt
echo '{"scale": 10}' > config.json
echo "--- changed config.json to scale=10, ran dvc repro:"; dvc repro 2>&1 | grep -v '^$'; cat out.txt
echo "--- truth (run by hand):"; python make.py; cat out.txt
echo "=== 2. fix: declare config.json"
sed -i 's/      - data.txt          # config.json is MISSING here/      - data.txt\n      - config.json/' dvc.yaml
dvc repro 2>&1 | grep -e Running -e Updating; cat out.txt
echo '{"scale": 3}' > config.json; dvc repro 2>&1 | grep -e Running; cat out.txt
echo "=== 3. always_changed, frozen, cache:false metrics"
cat > dvc.yaml <<'Y'
stages:
  make:
    cmd: python make.py
    deps: [make.py, data.txt, config.json]
    outs: [out.txt]
  stamp:
    cmd: date +%s%N > stamp.txt
    always_changed: true
    outs:
      - stamp.txt:
          cache: false
Y
dvc repro 2>&1 | grep -e Running -e "didn't change"
dvc repro 2>&1 | grep -e Running -e "didn't change"
echo "--- freeze make, change data, repro"; dvc freeze make >/dev/null; echo 4 >> data.txt; dvc repro 2>&1 | grep -e Running -e "didn't change" -e frozen; cat out.txt
dvc unfreeze make > /dev/null; dvc repro make 2>&1 | grep -e Running; cat out.txt
echo "=== 4. foreach and matrix"
cat > dvc.yaml <<'Y'
stages:
  make:
    cmd: python make.py
    deps: [make.py, data.txt, config.json]
    outs: [out.txt]
  fold:
    foreach: [0, 1, 2]
    do:
      cmd: echo fold ${item} > fold_${item}.txt
      outs:
        - fold_${item}.txt
  grid:
    matrix:
      model: [svm, rf]
      seed: [1, 2]
    cmd: echo ${item.model} ${item.seed} > g_${item.model}_${item.seed}.txt
    outs:
      - g_${item.model}_${item.seed}.txt
Y
dvc stage list 2>&1 | grep -v '^$'
echo "=== 5. non-deterministic stage"
cat > dvc.yaml <<'Y'
stages:
  noisy:
    cmd: python -c "import random; print(random.random())" > noisy.txt
    outs:
      - noisy.txt
Y
dvc repro 2>&1 | grep Running; python -I -c "import yaml;print('noisy.txt md5 in dvc.lock:', yaml.safe_load(open('dvc.lock'))['stages']['noisy']['outs'][0]['md5'])"
dvc repro -f 2>&1 | grep Running; python -I -c "import yaml;print('noisy.txt md5 in dvc.lock:', yaml.safe_load(open('dvc.lock'))['stages']['noisy']['outs'][0]['md5'])"
