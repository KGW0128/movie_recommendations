# ui로 출력해보기

import sys
from PyQt5.QtWidgets import *  # PyQt5 UI 관련 모듈
from PyQt5 import uic  # UI 파일 로드
import pandas as pd  # 데이터 처리
from sklearn.metrics.pairwise import linear_kernel  # 코사인 유사도 계산
from gensim.models import Word2Vec  # Word2Vec 모델 불러오기
from scipy.io import mmread  # 희소 행렬 로드
import pickle  # 객체 직렬화
from PyQt5.QtCore import QStringListModel  # 자동완성 기능을 위한 문자열 리스트 모델

from job06_recommendation import recommendation

# UI 파일 로드
from_window = uic.loadUiType('./ui.ui')[0]

# Exam 클래스 정의
class Exam(QWidget, from_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # TF-IDF 행렬 로드 (희소 행렬 형태)
        self.Tfidf_matrix = mmread('./models/Tfidf_movie_review.mtx').tocsr()

        # TF-IDF 모델 로드
        with open('./models/tfidf.pickle', 'rb') as f:
            self.Tfidf = pickle.load(f)

        # Word2Vec 모델 로드
        self.embedding_model = Word2Vec.load('./models/word2vec_movie_review.model')

        # 영화 리뷰 데이터 로드
        self.df_reviews = pd.read_csv('./Cleaned_Reviews/cleaned_reviews.csv')

        # 영화 제목 리스트 생성 및 정렬
        self.titles = list(self.df_reviews.titles)
        self.titles.sort()

        # 콤보박스에 영화 제목 추가

        # self.cb_title.addItem('test')
        for title_i in self.titles:
            self.cb_title.addItem(title_i)

        # ✅ 자동완성 기능 추가
        model = QStringListModel()  # 문자열 리스트 모델 생성
        model.setStringList(self.titles)  # 영화 제목 리스트를 자동완성 데이터로 설정
        completor = QCompleter()  # 자동완성 객체 생성
        completor.setModel(model)  # 자동완성 모델 설정
        self.le_keyword.setCompleter(completor)  # 입력창에 자동완성 기능 적용

        # 콤보박스 값 변경 시 추천 실행
        self.cb_title.currentIndexChanged.connect(self.combobox_slot)

        # 버튼 클릭 시 키워드 기반 추천 실행
        self.btn_recommend.clicked.connect(self.bth_slot)

    # 키워드 입력 후 버튼 클릭 시 실행되는 함수
    def bth_slot(self):
        keyword = self.le_keyword.text()  # 키워드 입력값 가져오기

        #키워드가 영화제목인지 아닌지
        if keyword in self.titles:
            recommendation = self.recommendation_by_title(keyword)
        else:
            recommendation = self.recommendation_by_keyword(keyword)  # 키워드 기반 추천 실행

        # 추천 결과가 있으면 라벨에 표시
        if recommendation:
            self.lbl_recommadation.setText(recommendation)

    # 콤보박스에서 영화 선택 시 실행되는 함수
    def combobox_slot(self):
        title = self.cb_title.currentText()  # 현재 선택된 영화 제목 가져오기
        print(title)  # 선택된 영화 제목 출력
        recommendation = self.recommendation_by_title(title)  # 선택된 영화 기반 추천 실행
        self.lbl_recommadation.setText(recommendation)  # 추천 결과 출력

    # 영화 제목을 기반으로 추천 영화 찾기
    def recommendation_by_title(self, title):
        movie_idx = self.df_reviews[self.df_reviews.titles == title].index[0]  # 영화 인덱스 찾기
        cosine_sim = linear_kernel(self.Tfidf_matrix[movie_idx], self.Tfidf_matrix)  # 코사인 유사도 계산
        recommendation = self.getRecommendation(cosine_sim)  # 추천 영화 가져오기
        recommendation = '\n'.join(list(recommendation))  # 리스트를 문자열로 변환
        return recommendation  # 추천 결과 반환

    # 키워드를 기반으로 추천 영화 찾기
    def recommendation_by_keyword(self, keyword):
        try:
            sim_word = self.embedding_model.wv.most_similar(keyword, topn=10)  # 키워드와 유사한 단어 찾기
        except:
            self.lbl_recommadation.setText('검색 결과 없음.....')  # 사전에 없는 단어일 경우 메시지 출력
            return 0  # 실행 중단

        words = [keyword]  # 입력 키워드 포함
        for word, _ in sim_word:
            words.append(word)  # 유사한 단어 추가

        print(words)  # 유사 단어 리스트 출력

        # 가중치를 적용한 문장 생성
        sentence = []
        count = 10
        for word in words:
            sentence = sentence + [word] * count  # 가중치 적용 (앞쪽 단어일수록 많이 반복)
            count -= 1
        sentence = ' '.join(sentence)  # 공백으로 연결하여 하나의 문장으로 변환
        print(sentence)  # 생성된 문장 출력

        # 문장을 TF-IDF 변환
        sentence_vec = self.Tfidf.transform([sentence])

        # 코사인 유사도 계산
        cosine_sim = linear_kernel(sentence_vec, self.Tfidf_matrix)

        # 추천 영화 가져오기
        recommendation = self.getRecommendation(cosine_sim)

        # 리스트를 문자열로 변환하여 반환
        recommendation = '\n'.join(recommendation)

        return recommendation

    # 코사인 유사도를 기반으로 추천 영화 가져오기
    def getRecommendation(self, cosine_sim):
        simScore = list(enumerate(cosine_sim[-1]))  # 유사도 점수 리스트 생성
        simScore = sorted(simScore, key=lambda x: x[1], reverse=True)  # 유사도 기준 정렬
        simScore = simScore[1:11]  # 자기 자신(1.0) 제외 후 상위 10개 선택
        movieIdx = [i[0] for i in simScore]  # 추천 영화 인덱스 가져오기

        return self.df_reviews.iloc[movieIdx]['titles']  # 추천 영화 리스트 반환

# 프로그램 실행
if __name__ == '__main__':
    app = QApplication(sys.argv)  # PyQt 애플리케이션 실행
    mainWindow = Exam()  # Exam 클래스 객체 생성
    mainWindow.show()  # UI 창 띄우기
    sys.exit(app.exec_())  # 이벤트 루프 실행
