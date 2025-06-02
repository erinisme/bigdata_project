from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# 크롬 옵션 설정
options = Options()
options.add_argument('--window-size=1920,1080')
# options.add_argument('--headless')  # 필요 시 활성화

# 웹드라이버 실행
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 웹 페이지 접속
url = 'https://comic.naver.com/webtoon?tab=mon'
driver.get(url)
time.sleep(3)  # 페이지 로딩 대기

# 웹툰 데이터 수집
webtoon_elements = driver.find_elements(By.CSS_SELECTOR, 'ul.ContentList__content_list--eFRCN li')

webtoons = []

for element in webtoon_elements:
    try:
        title = element.find_element(By.CLASS_NAME, 'ContentTitle__title--e3qXt').text
        thumbnail = element.find_element(By.TAG_NAME, 'img').get_attribute('src')
        authors = element.find_elements(By.CLASS_NAME, 'ContentAuthor__author--CTAAP')
        author_text = ', '.join([a.text for a in authors])
        try:
            rating = element.find_element(By.CSS_SELECTOR, '.Rating__star_area--Fh_ng span').text
        except:
            rating = 'N/A'

        webtoons.append({
            '타이틀': title,
            '썸네일': thumbnail,
            '작가': author_text,
            '평점': rating
        })
    except Exception as e:
        print(f"오류 발생: {e}")

driver.quit()

# 중복 제거
unique_webtoons = {w['타이틀']: w for w in webtoons}.values()

# 출력
print(f"\n총 {len(unique_webtoons)}개의 웹툰 정보를 수집했습니다.\n")
for i, w in enumerate(unique_webtoons, 1):
    print(f"{i}. {w['타이틀']} - {w['작가']} (평점: {w['평점']})")

# CSV 저장
df = pd.DataFrame(unique_webtoons)
df.to_csv('naver_monday_webtoons.csv', index=False, encoding='utf-8-sig')
print("\nCSV 파일 저장 완료: naver_monday_webtoons.csv")
