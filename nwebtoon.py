from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# 브라우저 옵션 설정
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # 필요한 경우 주석 해제
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# 드라이버 실행
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 네이버 웹툰 요일별 페이지 접속
url = "https://comic.naver.com/webtoon/weekday"
driver.get(url)
time.sleep(2)

# 월요일 웹툰 리스트 가져오기
try:
    webtoon = driver.find_element(By.CSS_SELECTOR, 'ul.PosterList__list--ZyGDL li')  # 첫 번째 웹툰만 선택

    title = webtoon.find_element(By.CLASS_NAME, 'Poster__title--dX3MH').text
    img = webtoon.find_element(By.TAG_NAME, 'img').get_attribute('src')
    author = webtoon.find_element(By.CLASS_NAME, 'Poster__author--tFAl_').text
    rating = webtoon.find_element(By.CLASS_NAME, 'Poster__star--WjPbT').text

    result = {
        'title': title,
        'thumbnail': img,
        'author': author,
        'rating': rating
    }

    print("\n✅ 웹툰 1개 정보:")
    print(result)

except Exception as e:
    print("❌ 오류 발생:", e)

finally:
    driver.quit()

