from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time
import random
import os

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
]

def ensure_static_folder():
    if not os.path.exists("static"):
        os.makedirs("static")

def web_scrapper_expedia(web_url, f_name):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(web_url)
    time.sleep(5)

    hotels = driver.find_elements(By.CLASS_NAME, "uitk-card")

    if not hotels:
        driver.quit()
        return None

    file_path = f'static/{f_name}.csv'
    with open(file_path, 'w', encoding='utf-8', newline='') as file_csv:
        writer = csv.writer(file_csv)
        writer.writerow(['Hotel Name', 'Location', 'Price', 'Rating', 'Link'])

        for hotel in hotels:
            try:
                hotel_name = hotel.find_element(By.CLASS_NAME, "uitk-heading-5").text
            except:
                hotel_name = "NA"

            try:
                location = hotel.find_element(By.CLASS_NAME, "uitk-text-default-theme").text
            except:
                location = "NA"

            try:
                price = hotel.find_element(By.CLASS_NAME, "uitk-text-emphasis-theme").text.replace('₹\xa0', '')
            except:
                price = "NA"

            try:
                rating = hotel.find_element(By.CLASS_NAME, "uitk-badge").text
            except:
                rating = "NA"

            try:
                link = hotel.find_element(By.TAG_NAME, "a").get_attribute("href")
            except:
                link = "NA"

            writer.writerow([hotel_name, location, price, rating, link])
    
    driver.quit()
    return file_path
