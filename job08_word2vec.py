
#모델 학습 저장


import pandas as pd
from gensim.models import word2vec, Word2Vec

df_reviews = pd.read_csv('./Cleaned_Reviews/cleaned_reviews.csv')
df_reviews.info()


reviews = list(df_reviews.reviews)
print(reviews[0])
tokens =[]
for sentence in reviews:
    token = sentence.split()
    tokens.append(token)
print(tokens[0])

#의미 학습을 시킨다

#vector_size: 데이터 소실성 때문에 차원 축소
#window: 4개씩 짤라서 학습
#workers: 학습시킬 코어갯수(내가 가진 코어 갯수만큼 넣주면 됨)
#min_count: 전체 데이터에 20번 이상 나온 데이터만 학습해라
embedding_model = Word2Vec(tokens, vector_size= 100 , window=4,
                           min_count=20, workers=4, epochs=100 , sg=1)
embedding_model.save('./models/word2vec_movie_review.model')

print(list(embedding_model.wv.index_to_key))
print(len(embedding_model.wv.index_to_key))



