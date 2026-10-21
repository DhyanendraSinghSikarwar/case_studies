import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import classification_report
pos=["great product works well","love it fast delivery","excellent quality highly recommend","very happy with purchase","amazing value works perfectly","superb build and quality","good value will buy again","fantastic support quick refund"]
neg=["terrible product broke quickly","hate it slow delivery","poor quality do not recommend","very unhappy with purchase","awful value stopped working","bad build and quality","waste of money never again","horrible support no refund"]
X=pos+neg; y=[1]*8+[0]*8
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=0.3,stratify=y,random_state=0)
pipe=make_pipeline(TfidfVectorizer(ngram_range=(1,2),sublinear_tf=True,min_df=1),LogisticRegression(C=1.0,max_iter=1000,class_weight="balanced"))
pipe.fit(Xtr,ytr)
print(classification_report(yte,pipe.predict(Xte),digits=2))
print(pipe.predict(["quality is awful","works great love it"]))
