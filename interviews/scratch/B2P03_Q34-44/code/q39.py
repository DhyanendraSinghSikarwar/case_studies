# Two fallbacks to a rigid schema, with MOCK model outputs (no real model).
import json, re
from typing import Literal, Optional
from pydantic import BaseModel, ValidationError

# (a) Schema with an escape hatch: closed enum + 'other' + free-text field
class Ticket(BaseModel):
    category: Literal["billing", "bug", "feature", "other"]
    category_other: Optional[str] = None     # filled only when category == "other"
    summary: str

# (b) Lenient parse of free text: pull the first {...} block, then validate
def lenient_parse(text):
    m = re.search(r"\{.*\}", text, re.S)
    if not m: return None, "no JSON found"
    try: return Ticket.model_validate(json.loads(m.group(0))), None
    except (json.JSONDecodeError, ValidationError) as e: return None, type(e).__name__

mock_outputs = [
    'Sure! Here you go:\n{"category": "bug", "summary": "App crashes on login"}\nHope that helps.',
    '{"category": "other", "category_other": "legal threat", "summary": "Customer mentions a lawyer"}',
    '{"category": "complaint", "summary": "Rude agent"}',      # outside the enum
    'I think this is mostly billing but also a bug.',            # no JSON
]
for t in mock_outputs:
    obj, err = lenient_parse(t)
    print("OK  " + obj.model_dump_json() if obj else f"FAIL {err}  -> route to retry / second extraction pass / human")
