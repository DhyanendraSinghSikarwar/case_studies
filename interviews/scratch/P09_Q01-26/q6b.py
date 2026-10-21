from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
pos=["great product works well","love it fast delivery","excellent quality highly recommend","very happy with purchase","amazing value works perfectly","superb build and quality","good value will buy again","fantastic support quick refund"]
neg=["terrible product broke quickly","hate it slow delivery","poor quality do not recommend","very unhappy with purchase","awful value stopped working","bad build and quality","waste of money never again","horrible support no refund"]
X=pos+neg; y=[1]*8+[0]*8
pipe=make_pipeline(TfidfVectorizer(ngram_range=(1,2),sublinear_tf=True),
                   LogisticRegression(C=1.0,max_iter=1000,class_weight="balanced"))
pipe.fit(X,y)
print(pipe.predict(["quality is awful","works great love it"]))
vec,clf=pipe.steps[0][1],pipe.steps[1][1]
import numpy as np
names=vec.get_feature_names_out(); w=clf.coef_[0]
print("top +:",list(names[np.argsort(-w)[:3]]),"top -:",list(names[np.argsort(w)[:3]]))
