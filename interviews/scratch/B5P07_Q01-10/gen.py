# gen.py: code/qNN.py = prelude (unless body starts with '#NOPRELUDE') + parts/qNN.py
import pathlib, sys
root = pathlib.Path(__file__).resolve().parent
pre = (root / 'prelude.py').read_text()
for p in sorted((root / 'parts').glob('q*.py')):
    b = p.read_text()
    if b.startswith('#NOPRELUDE'):
        txt = b.split('\n', 1)[1]
    else:
        txt = pre + '\n' + b
    (root / 'code' / p.name).write_text(txt)
