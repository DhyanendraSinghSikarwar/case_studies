import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
text="Not happy! The delivery was NOT on time, and I'm asking for a refund :( http://x.co/1"
t=text.lower()
t=re.sub(r"https?://\S+"," ",t)
tokens=re.findall(r"[a-z']+",t)
print(tokens)
print([w for w in tokens if w not in ENGLISH_STOP_WORDS])    # note: 'not' is removed!
print("not" in ENGLISH_STOP_WORDS, "no" in ENGLISH_STOP_WORDS)
