import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle
from konlpy.tag import Okt
from gensim.models import Word2Vec
from tensorflow.python.framework.test_ops import ref_in


def getRecommendation(cosine_sim, df_reviews):
    simScore = list(enumerate(cosine_sim[-1]))  # 유사도 점수 리스트 생성
    simScore = sorted(simScore, key=lambda x: x[1], reverse=True)  # 유사도 기준 정렬
    simScore = simScore[1:11]  # 자기 자신(1.0) 제외 후 상위 10개 선택
    movieIdx = [i[0] for i in simScore]  # 인덱스 가져오기

    return df_reviews.iloc[movieIdx]['titles']  # 추천 영화 리스트 반환


# CSV 파일 & TF-IDF 행렬 불러오기
df_reviews = pd.read_csv('./Cleaned_Reviews/cleaned_reviews.csv')
Tfidf_matrix = mmread('./models/Tfidf_movie_review.mtx').tocsr()

# TF-IDF 모델 불러오기
with open('./models/tfidf.pickle', 'rb') as f:
    Tfidf = pickle.load(f)

# 기준이 되는 영화 index 선택
ref_idx = 10
print("🎬 기준 영화:", df_reviews.iloc[ref_idx]['titles'])

# 코사인 유사도 계산
cosine_sim = linear_kernel(Tfidf_matrix[ref_idx], Tfidf_matrix)

# 추천 영화 리스트 출력
recommendations = getRecommendation(cosine_sim, df_reviews)
print("📌 추천 영화 목록:")
print(recommendations)