from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
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

def web_scrapper_airbnb(web_url, f_name):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(web_url)
    time.sleep(5)

    action = ActionChains(driver)
    for _ in range(5):  # Scroll multiple times to load more listings
        action.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(2)

    listings = driver.find_elements(By.CLASS_NAME, "_8ssblpx")

    if not listings:
        driver.quit()
        return None

    file_path = f'static/{f_name}.csv'
    with open(file_path, 'w', encoding='utf-8', newline='') as file_csv:
        writer = csv.writer(file_csv)
        writer.writerow(['Listing Name', 'Location', 'Price', 'Rating', 'Link'])

        for listing in listings:
            try:
                name = listing.find_element(By.CLASS_NAME, "t1jojoys").text
            except:
                name = "NA"

            try:
                location = listing.find_element(By.CLASS_NAME, "_167qordg").text
            except:
                location = "NA"

            try:
                price = listing.find_element(By.CLASS_NAME, "_tyxjp1").text.replace('₹\xa0', '')
            except:
                price = "NA"

            try:
                rating = listing.find_element(By.CLASS_NAME, "r1dxllyb").text
            except:
                rating = "NA"

            try:
                link = listing.find_element(By.TAG_NAME, "a").get_attribute("href")
            except:
                link = "NA"

            writer.writerow([name, location, price, rating, link])
    
    driver.quit()
    return file_path
