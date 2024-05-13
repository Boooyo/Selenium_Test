import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Chrome 드라이버 설정
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

# 검색어 입력
driver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&authuser=0&ogbl")
text = driver.find_element(By.NAME, "q")
search = "샌드위치"
text.send_keys(search)
text.send_keys(Keys.RETURN)

# 이미지 저장 폴더 생성
dir_path = search
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

# 검색 결과 페이지 URL
""" #페이지 끝까지 스크롤 후 이미지 가져옴
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
"""

# 이미지 다운로드
images = driver.find_elements(By.CSS_SELECTOR, ".rg_i")
for i, image in enumerate(images):
    try:
        image.click()
        time.sleep(2)
        original_image_url = None
        element = driver.find_element(By.CSS_SELECTOR, ".iPVvYb")
        if element.get_attribute("src") and element.get_attribute("src").startswith("http"):
            original_image_url = element.get_attribute("src")
        if not original_image_url:
            raise ValueError("Could not find image URL")
        filename = "{}_{}.jpg".format(search, i)
        filepath = os.path.join(dir_path, filename)
        response = requests.get(original_image_url)
        with open(filepath, "wb") as f:
            f.write(response.content)
        print("다운로드 완료:", filepath)
        #10개만 다운
        if i == 10-1:
            break
    except Exception as e:
        print("에러 발생:", e)
# Chrome 드라이버 종료
driver.quit()