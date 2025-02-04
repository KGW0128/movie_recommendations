from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
import pandas as pd
import re
import time
import os




# ===============================
# 🔹 1. 크롬 드라이버 설정
# ===============================


# 크롬 옵션 설정
options = ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'

options.add_argument('--disable-blink-features=AutomationControlled')  # 자동화 탐지 방지
options.add_argument(f'user-agent={user_agent}')  # User-Agent 설정
options.add_argument('lang=ko_KR')  # 기본 언어 설정

# 크롬 드라이버 실행
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)





# ===============================
# 🔹 2. 웹페이지 열기
# ===============================


url = 'https://m.kinolights.com/discover/explore'
driver.get(url)
time.sleep(3)  # 페이지 로딩 대기





# ===============================
# 🔹 3. 데이터프레임 초기화 및 저장 디렉토리 설정
# ===============================


#데이터프레임 초기화
df_titles = pd.DataFrame()

# 저장할 디렉토리 설정
#저장위치 잘 확인하기
save_path = "C:/workspace/movie_recommendations/review"
os.makedirs(save_path, exist_ok=True)  # 폴더 없으면 자동 생성





# ===============================
# 🔹 4. 영화 리뷰 크롤링
# ===============================


for movie_i in range(50, 1001):  # 최대 15개 영화 크롤링

    time.sleep(0.5)  # 페이지 안정화 대기
    reviews = []  # 리뷰 리스트 초기화

    # 8개 단위로 스크롤 (한 페이지에 8개씩 표시됨)
    if movie_i % 8 == 0:
        for _ in range(int(movie_i/8)*2): # 만약 중간부터 다시 크롤링 할 것을 대비한 반복문
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # 페이지 로딩 대기


    # 영화 제목 가져오기
    try:
        element = driver.find_element(By.XPATH, f'//*[@id="contents"]/div/div/div[3]/div[2]/div[{movie_i}]/div/div[1]')
        movie_name_text = element.text.strip()
        print(f"🎬 영화 이름: {movie_name_text}")

        # 특수 문자 제거 (파일명에 사용 불가한 문자 제거)
        safe_movie_name = re.sub(r'[\\/*?:"<>|]', '', movie_name_text)[:100] or "unknown_movie"

    except NoSuchElementException:
        # 영화 제목을 찾지 못했을 때
        print(f"❌ 영화 {movie_i} 정보를 찾을 수 없습니다.")
        continue  # 다음 영화로 넘어가기

    # 영화 선택
    movie_button_xpath = f'//*[@id="contents"]/div/div/div[3]/div[2]/div[{movie_i}]'
    driver.find_element(By.XPATH, movie_button_xpath).click()
    time.sleep(3)

    # 리뷰 페이지 이동
    review_button_xpath = '//*[@id="review"]'
    driver.find_element(By.XPATH, review_button_xpath).click()
    time.sleep(3)






# ===============================
# 🔹 5. 영화 리뷰 크롤링 (최대 110개)
# ===============================


    for review_i in range(1, 51):  # 여유롭게 110개까지 크롤링

        # 8개마다 스크롤 (한 페이지당 8개)
        if review_i % 8 == 1:
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(1)

        # 리뷰 XPATH 지정
        review_xpath = f'//*[@id="contents"]/div[5]/section[2]/div/article[{review_i}]/div[3]/a/h5'

        try:
            # 최대 10초 동안 리뷰 요소가 나타날 때까지 대기
            review_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, review_xpath)))

            #스크롤
            driver.execute_script("arguments[0].scrollIntoView(true);", review_element)
            time.sleep(1)

            # 리뷰 텍스트 가져오기 및 정제
            review = review_element.text
            review = re.compile('[^가-힣 ]').sub(' ', review)  # 한글과 공백만 남김
            review = re.sub(' +', ' ', review).strip()  # 여러 공백을 하나로 줄이고 양 끝 공백 제거

            if review:
                reviews.append(review) # 데이터 저장
                print(f"✅ [{review_i}]저장된 리뷰: {review}")
            else:
                print(f"⚠️ 리뷰 없음: {review_i}번")

        except TimeoutException: # 10초 이상 대기 했지만 데이터가 없을 때(리뷰 최대가 for문 보다 작을 때)
            print(f"\n🚨 다음 리뷰 요소가 존재하지 않아 크롤링 중단\n")
            break  # 리뷰가 없으면 반복문 종료 후 있는거 까지만 저장

        except (NoSuchElementException, StaleElementReferenceException):
            print(f"\n❌ 리뷰 {review_i} 크롤링 실패\n")
            continue  # 다음 리뷰로 넘어감





# ===============================
# 🔹 6. 크롤링한 데이터 저장
# ===============================


    # 리뷰 데이터를 데이터프레임으로 변환 (리뷰, 영화 제목)
    df_section_titles = pd.DataFrame({'review': reviews, 'name': movie_name_text})
    df_titles = pd.concat([df_titles, df_section_titles], axis=0, ignore_index=True)

    # 데이터프레임 정보 출력
    print(df_titles.head())
    df_titles.info()
    print(df_titles['name'].value_counts())

    # CSV 파일 저장
    df_titles.to_csv(os.path.join(save_path, f"{safe_movie_name}_reviews.csv"), index=False)

    # 데이터프레임 초기화
    df_titles = pd.DataFrame()


# ===============================
# 🔹 7. 다음 영화로 이동 (뒤로 가기)
# ===============================
    

    back_xpath = '//*[@id="header"]/div/button[1]'
    driver.find_element(By.XPATH, back_xpath).click()
    time.sleep(3)




# ===============================
# 🔹 8. 브라우저 종료
# ===============================

# 크롤링 완료 후 브라우저 종료
driver.quit()
