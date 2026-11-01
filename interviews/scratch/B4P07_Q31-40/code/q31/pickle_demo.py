"""Harmless demo: unpickling runs code. Never pickle.load a model you did not produce."""
import pickle

class Evil:
    def __reduce__(self):                 # a real attacker would return (os.system, ("...",))
        return (print, ("code ran during pickle.loads",))

blob = pickle.dumps(Evil())
pickle.loads(blob)
