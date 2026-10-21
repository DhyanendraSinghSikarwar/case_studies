import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
docs=["win free prize now","free money win","meeting at noon","lunch meeting tomorrow","free lunch offer now","project update meeting"]
y=np.array([1,1,0,0,1,0])
cv=CountVectorizer();X=cv.fit_transform(docs)
nb=MultinomialNB(alpha=1).fit(X,y)
print(nb.predict_proba(cv.transform(["free prize meeting"])))
# manual
vocab=cv.get_feature_names_out();V=len(vocab)
def lik(c):
    cnt=X[y==c].sum(0).A1+1;return cnt/cnt.sum()
msg=cv.transform(["free prize meeting"]).toarray()[0]
ls=[np.log((y==c).mean())+msg@np.log(lik(c)) for c in (0,1)]
p=np.exp(ls);print(p/p.sum())
# Q4 code
rng=np.random.default_rng(0);N=100_000
car=rng.integers(0,3,N);pick=rng.integers(0,3,N)
print((pick==car).mean(),(pick!=car).mean())
# Q9 compact
def vn_bit(p,rng):
    while True:
        a,b=rng.random()<p,rng.random()<p
        if a!=b:return int(a)
def uniform7(p,rng):
    while True:
        v=4*vn_bit(p,rng)+2*vn_bit(p,rng)+vn_bit(p,rng)
        if v<7:return v
r=np.random.default_rng(1);print(np.bincount([uniform7(.8,r) for _ in range(14000)])/14000)
