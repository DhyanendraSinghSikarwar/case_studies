from packaging.specifiers import SpecifierSet
from packaging.version import Version
repos = {"churn": ">=1.4,<2", "fraud": ">=1.4,<2", "ltv": ">=1.2,<2", "ranker": ">=1.4,<3",
         "forecast": "==1.4.*", "nlp": ">=1.0", "pricing": ">=1.4,<2", "risk": ">=1.3,<2"}
for new in ["1.5.0", "2.0.0"]:
    ok = [r for r, s in repos.items() if Version(new) in SpecifierSet(s)]
    blocked = [r for r in repos if r not in ok]
    print(f"featlib {new}: accepted by {len(ok)} repos {ok}")
    print(f"             blocked in {len(blocked)} repos {blocked}")
