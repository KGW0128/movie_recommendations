

#텍스트 프리퀀시(TF)를 그대로 쓰면 모든문장에 중복되는 단어를 
# 그대로 쓰면 모델 학습에 방해됨.
#그래서 역수치해서 곱해줌.(DF)
#100/100 = 1

#즉, 유사 문장 찾기

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer #통계에 관련된 패키지
from scipy.io import mmwrite, mmread # 과학 함수를 다루는 패키지
import pickle

df_reviews = pd.read_csv('./Cleaned_Reviews/cleaned_reviews.csv')
df_reviews.info()

Tfidf = TfidfVectorizer(sublinear_tf=True)
Tfidf_matrix = Tfidf.fit_transform(df_reviews.reviews)
print(Tfidf_matrix.shape)

with open('./models/tfidf.pickle','wb') as f:
    pickle.dump(Tfidf, f)

mmwrite('./models/Tfidf_movie_review.mtx', Tfidf_matrix)

