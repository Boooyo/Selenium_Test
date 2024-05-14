import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def configure_driver():
    # Chrome 드라이버 설정
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(ChromeDriverManager().install(), options=options)

def search_and_download_images(search_query, max_images=10):
    # WebDriver 설정
    driver = configure_driver()

    try:
        # Google 이미지 검색 페이지 열기
        driver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&authuser=0&ogbl")
        
        # 검색어 입력
        search_input = driver.find_element(By.NAME, "q")
        search_input.send_keys(search_query)
        search_input.send_keys(Keys.RETURN)

        # 이미지 저장 폴더 생성
        dir_path = search_query
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # 이미지 다운로드
        images = driver.find_elements(By.CSS_SELECTOR, ".rg_i")
        for i, image in enumerate(images):
            try:
                image.click()
                time.sleep(2)
                
                # 원본 이미지 URL 가져오기
                original_image_url = driver.find_element(By.CSS_SELECTOR, ".iPVvYb").get_attribute("src")
                if not original_image_url.startswith("http"):
                    raise ValueError("Could not find image URL")

                # 이미지 저장
                filename = f"{search_query}_{i}.jpg"
                filepath = os.path.join(dir_path, filename)
                with open(filepath, "wb") as f:
                    response = requests.get(original_image_url)
                    f.write(response.content)
                
                print("다운로드 완료:", filepath)
                
                # 지정된 최대 이미지 개수만큼 다운로드
                if i == max_images - 1:
                    break
            except Exception as e:
                print("에러 발생:", e)
    finally:
        # WebDriver 종료
        driver.quit()

if __name__ == "__main__":
    search_query = "샌드위치"
    search_and_download_images(search_query)
