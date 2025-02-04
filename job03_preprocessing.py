# 형태소 분리 및 불용어 처리

import pandas as pd
from konlpy.tag import Okt
import re

# 취합한 리뷰 데이터 가져오기
df = pd.read_csv('./Merged_Reviews/reciews_kinolights.csv')
df.info()

# 불용어 처리 데이터 가져오기
df_stopwords = pd.read_csv('./StopWord/stopwords.csv')
stopwords = list(df_stopwords['stopword'])  # 리스트화

# 가져온 데이터 0번 출력 해보기
# print(df.titles[0])
# print(df.reviews[0])

cleaned_sentences = []

for review in df.reviews:

    # 형태소 분리
    okt = Okt()

    tokened_review = okt.pos(review, stem=True)
    # print(tokened_review)

    df_token = pd.DataFrame(tokened_review, columns=['word', 'class'])
    df_token = df_token[(df_token['class'] == 'Noun') |
                        (df_token['class'] == 'Verb') |
                        (df_token['class'] == 'Adjective')]
    # print(df_token)


    # 불용어 처리
    words = []
    for word in df_token.word:
        if 1 < len(word):
            if word not in stopwords:
                words.append(word)

    cleaned_sentence = ' '.join(words)
    cleaned_sentences.append(cleaned_sentence)


df.reviews  = cleaned_sentences
df.dropna(inplace=True)
df.info()

df.to_csv('./Cleaned_Reviews/cleaned_reviews.csv',index=False)