import pathlib, re
ROOT = pathlib.Path(__file__).parent / "code"
CMT = {"python": "#", "shell": "#", "toml": "#", "yaml": "#", "ini": "#"}
FENCE = {"python": "python", "shell": "sh", "toml": "toml", "yaml": "yaml", "ini": "ini", "text": ""}

def code(lang, files):
    parts = []
    for f in files:
        txt = (ROOT / f).read_text().rstrip("\n")
        parts.append(f"{CMT[lang]} ===== {f.split('/',1)[1]} =====\n{txt}" if len(files) > 1 else f"{CMT[lang]} {f.split('/',1)[1]}\n{txt}")
    return f"```{FENCE[lang]}\n" + "\n\n".join(parts) + "\n```"

def out(f, header=None):
    txt = (ROOT / f).read_text().rstrip("\n")
    return "```text\n" + (header + "\n" if header else "") + txt + "\n```"
