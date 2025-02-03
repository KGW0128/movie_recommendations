#
# //*[@id="contents"]/div/div/div[3]/div[2]/div[2]/a/div/div[1]/div[1]/img

# //*[@id="contents"]/div/div/div[3]/div[2]/div[5]/a/div/div[1]/div[1]/img

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from setuptools.package_index import user_agent
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd
import re
import time
import datetime
from selenium.webdriver.common.keys import Keys


# 크롬에서 연다
# 열어볼 주소
options = ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'

# 한글만 긁어옴
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('user_agent=' + user_agent)
options.add_argument('lang=ko_KR')

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# 별점 카테고리 리스트 정의
category = ['name', 'review']

#전체 횟수
for all_i in range(5):

    # 데이터 프레임 초기화
    df_titles = pd.DataFrame()

    url = ('https://m.kinolights.com/discover/explore')

    driver.get(url)  # 브라우저 띄우기
    time.sleep(3)  # 버튼 생성이 될때까지 기다리는 딜레이

    #스크롤 할 횟수
    #for scroll_i in range(3):
    #    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #    time.sleep(3)  # 페이지 로딩 대기


    reviews = []

    #영화 선택
    for movie_i in range(1,9):


        # 영화 이름 가져오기
        element = driver.find_element('xpath','// *[ @ id = "contents"] / div / div / div[3] / div[2] / div[{}] / div / div[1]'.format(movie_i))
        movie_name_text = element.text
        print('영화이름: ', movie_name_text)

        #영화 선택
        movie_button_xpath = '//*[@id="contents"]/div/div/div[3]/div[2]/div[{}]'.format(movie_i)
        time.sleep(3)
        driver.find_element(By.XPATH, movie_button_xpath).click()

        #리뷰 버튼 누르기
        review_button_xpath = '//*[@id="review"]'
        time.sleep(3)
        driver.find_element(By.XPATH, review_button_xpath).click()


        for review_i in range(1,101):


            if (review_i % 8) == 1:
                body_xpath = '//*[@id="content__body"]/div'
                time.sleep(3)
                driver.find_element(By.XPATH, body_xpath).click()


                driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
                time.sleep(1)


            try:
                review_xpath = '//*[@id="contents"]/div[5]/section[2]/div/article[{}]/div[3]/a/h5'.format(review_i)

                # 뷰 크롤링 및 한글 외 문자 제거
                review = driver.find_element(By.XPATH, review_xpath).text
                review = re.compile('[^가-힣 ]').sub(' ', review)  # 한글과 공백만 남김
                review = re.sub(' +', ' ', review).strip()  # 여러 공백을 하나로 줄이고 양 끝 공백 제거

                # title이 비어있지 않을 때만 추가
                if review:
                    print('text저장:', reviews)
                else:
                    print('reiew_nall: ', review_i)

            except:  # 예외 처리 (존재하지 않는 항목 무시)
                print('pass: ', review_i)

            if (review_i % 8) == 0:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)  # 페이지 로딩 대기


        # 크롤링된 제목을 데이터프레임에 저장
        df_section_titles = pd.DataFrame(reviews, columns=['review'])
        df_section_titles['name'] = movie_name_text
        df_titles = pd.concat([df_titles, df_section_titles], axis='rows', ignore_index=True)
        reviews.clear()



        # 카테고리별 데이터프레임 정보 출력
        print(df_titles.head())
        df_titles.info()
        print(df_titles['name'].value_counts())

        # 제목 리스트 초기화
        reviews.clear()

        # 카테고리별 데이터를 CSV 파일로 저장
        df_titles.to_csv('C:/workspace/movie_recommendations/review/{}_reviews.csv'.format(movie_name_text), index=False)

        #뒤로가기
        back_xpath = '//*[@id="header"]/div/button[1]/div/svg'
        time.sleep(3)
        driver.find_element(By.XPATH, back_xpath).click()
        

