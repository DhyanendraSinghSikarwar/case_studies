import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
docs=["the bank approved the loan","the river bank was flooded","loan approved by the bank manager"]
v=TfidfVectorizer()  # smooth idf, l2 norm
X=v.fit_transform(docs)
print(dict(zip(v.get_feature_names_out(),np.round(v.idf_,2))))
print(np.round(cosine_similarity(X),2))
# by hand for one term
N=3; df_bank=3; df_loan=2
print("idf(bank)",np.log((1+N)/(1+df_bank))+1,"idf(loan)",np.log((1+N)/(1+df_loan))+1)
# synonym failure
d2=["cheap flights to goa","inexpensive airfare to goa"]
print(round(cosine_similarity(TfidfVectorizer().fit_transform(d2))[0,1],2))
