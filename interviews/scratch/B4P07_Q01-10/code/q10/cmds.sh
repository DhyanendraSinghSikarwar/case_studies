pytest -q -p no:cacheprovider
python -I gate.py --candidate candidate_pass.json --champion champion.json; echo "exit=$?"
python -I gate.py --candidate candidate_regress.json --champion champion.json; echo "exit=$?"
python -I gate.py --candidate candidate_missing.json --champion champion.json; echo "exit=$?"
python -I gate.py --candidate candidate_pass.json --champion no_such_file.json; echo "exit=$?"
python -I gate.py --candidate candidate_pass.json --champion no_such_file.json --allow-no-champion; echo "exit=$?"
actionlint gate_step.yml; echo "actionlint exit=$?"
