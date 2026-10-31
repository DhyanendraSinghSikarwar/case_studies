actionlint unsafe.yml; echo "unsafe exit=$?"
actionlint safe.yml; echo "safe exit=$?"
bash inject_demo.sh
python -I mask_demo.py
