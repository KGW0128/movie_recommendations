# 영화 리뷰 기반 추천 시스템

## 1. 프로젝트 개요
이 프로젝트는 영화 리뷰 데이터를 기반으로 추천 시스템을 구축하는 프로젝트입니다. 사용자에게 영화 제목이나 키워드를 입력받아 해당 영화와 유사한 영화를 추천하는 시스템을 개발하였습니다. TF-IDF와 Word2Vec 모델을 사용하여 텍스트 데이터를 분석하고, PyQt5를 활용해 GUI를 구현하였습니다.

## 2. 데이터 준비

### 2.1. 리뷰 데이터
영화 리뷰 데이터셋을 CSV 파일 형식으로 취합하였고, 불용어 처리 및 형태소 분석을 통해 데이터 전처리를 진행하였습니다.

### 2.2. 불용어 처리
`konlpy`의 Okt 형태소 분석기를 사용하여 명사, 동사, 형용사를 추출하고, 불용어 리스트에 포함된 단어들을 제거하여 텍스트를 정제하였습니다.

### 2.3. 데이터 전처리
`pandas`를 사용하여 리뷰 데이터를 처리하고, 불용어를 제거한 후 텍스트 데이터를 정리하여 `cleaned_reviews.csv`로 저장하였습니다.

## 3. TF-IDF 벡터화

### 3.1. TF-IDF 모델 구축
`TfidfVectorizer`를 사용하여 영화 리뷰 데이터를 TF-IDF 방식으로 벡터화하였습니다. 이 벡터화된 데이터를 `.mtx` 형식으로 저장하고, 모델은 `pickle`을 통해 직렬화하여 저장하였습니다.

### 3.2. 유사도 계산
각 영화 리뷰 간의 유사도를 계산하기 위해 `linear_kernel`을 사용하여 코사인 유사도를 구하고, 이를 바탕으로 추천 시스템을 구축하였습니다.

## 4. Word2Vec 모델 학습

### 4.1. Word2Vec 모델 구축
Word2Vec 모델을 사용하여 영화 리뷰 데이터를 기반으로 단어의 의미를 벡터 공간에 학습시켰습니다. 이 모델은 영화 리뷰에서 유사한 단어들 간의 관계를 학습하여 의미적 유사도를 파악할 수 있게 해줍니다.

### 4.2. 모델 저장
학습된 Word2Vec 모델은 `word2vec_movie_review.model` 파일로 저장하였으며, 이를 통해 특정 키워드와 유사한 단어들을 찾아내고, 이를 바탕으로 추천 영화 리스트를 생성할 수 있습니다.

## 5. 영화 추천 시스템

### 5.1. 영화 제목 기반 추천
사용자가 선택한 영화 제목을 기반으로 유사한 영화들을 추천하기 위해, TF-IDF 행렬을 사용하여 코사인 유사도를 계산하고, 유사한 영화들을 추천 리스트로 반환합니다.

### 5.2. 키워드 기반 추천
사용자가 입력한 키워드가 Word2Vec 모델에 학습된 단어 중 하나일 경우, 해당 키워드와 유사한 단어들을 찾아내고 이를 바탕으로 영화 추천을 생성합니다. 키워드에 대한 유사 단어 리스트를 생성하고, 이를 바탕으로 추천 영화를 제공합니다.

## 6. UI 구현 (PyQt5)

### 6.1. UI 개발
PyQt5를 사용하여 간단한 영화 추천 시스템의 GUI를 구현하였습니다. 사용자에게 영화 제목을 선택할 수 있는 콤보박스와 키워드를 입력받을 수 있는 텍스트 필드를 제공하고, 추천 결과를 출력하는 라벨을 설정했습니다.

### 6.2. 자동완성 기능
영화 제목 입력 시 자동완성 기능을 구현하여, 사용자가 영화 제목을 빠르게 선택할 수 있도록 했습니다.

### 6.3. 추천 결과 표시
사용자 입력에 따라 추천 결과를 실시간으로 표시하며, 버튼 클릭 시 키워드 기반 추천을 실행할 수 있도록 했습니다.

## 7. 차원 축소 및 시각화

### 7.1. Word2Vec 벡터 시각화
`TSNE` 알고리즘을 사용하여 학습된 Word2Vec 단어 벡터를 2차원으로 차원 축소한 후, 시각화를 진행하였습니다. 특정 키워드와 유사한 단어들이 2D 공간에서 어떻게 군집을 이루는지 시각적으로 확인할 수 있었습니다.

### 7.2. 결과 분석
t-SNE를 통해 고차원 벡터들을 2D 평면으로 변환하여, 유사한 단어들이 서로 가까운 위치에 배치됨을 확인했습니다.

## 8. 결론
이 프로젝트를 통해 영화 리뷰 데이터를 기반으로 영화 추천 시스템을 구축하고, 다양한 방법으로 추천 결과를 제공할 수 있음을 보여주었습니다. TF-IDF와 Word2Vec를 이용한 추천 시스템은 영화와 관련된 텍스트 데이터에서 의미적 유사도를 계산하여 유용한 추천 결과를 도출할 수 있는 강력한 도구입니다. 또한, PyQt5를 사용하여 직관적인 GUI를 구현함으로써 사용자가 손쉽게 추천 시스템을 사용할 수 있도록 했습니다.

## 9. 프로젝트 구조
---
## 9. 프로젝트 구조

root/  
├── .idea/                           # 프로젝트 설정 관련 폴더 (IDE 설정 파일)  
├── models/                          # 학습된 모델 파일들이 저장되는 폴더  
├── review/                          # 영화 리뷰 데이터 파일  
├── crawling_data/                   # 크롤링 관련 코드 폴더  
│   ├── job01_crawling.py            # 영화 데이터를 크롤링하는 스크립트  
│   ├── job02_comcat.py              # 크롤링한 데이터를 병합하는 스크립트  
│   ├── job03_preprocessing.py       # 데이터 전처리 스크립트  
│   ├── job04_word_cloud.py          # 워드 클라우드를 생성하는 스크립트  
│   ├── job05_TFIDF.py               # TF-IDF 벡터화 및 모델 학습 스크립트  
│   ├── job06_recommendation.py      # 추천 시스템 구축 스크립트  
│   ├── job07_movie_recommendation_app.py # 영화 추천 시스템 앱 실행 스크립트  
│   ├── job08_word2vec.py            # Word2Vec 모델 학습 스크립트  
│   └── job09_word2vec_visualization.py # Word2Vec 시각화 스크립트  
├── Cleaned_Reviews/                 # 전처리된 리뷰 데이터가 저장되는 폴더  
├── Merged_Reviews/                  # 병합된 리뷰 데이터가 저장되는 폴더  
├── StopWord/                        # 불용어 파일 저장 폴더  
├── __pycache__/                     # 파이썬 바이트 코드 캐시 폴더  
├── malgun.ttf                       # 사용된 폰트 파일 (Malgun 폰트)  
├── requirements.txt                 # 프로젝트에 필요한 라이브러리 목록  
├── ui/                              # UI 파일 폴더  
│   └── ui.ui                        # PyQt5 UI 파일  
└── README.md                        # 프로젝트 설명 파일
---


## 10. 환경 설정

### 10.1. Python 버전
- Python 3.10

### 10.2. 폰트
- 폰트: Malgun
