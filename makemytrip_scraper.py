from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

def web_scrapper_makemytrip(web_url, f_name):
    options = Options()
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

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "listingRowOuter"))
        )
    except:
        print("❌ No listings found or page structure has changed.")
        driver.quit()
        return None

    listings = driver.find_elements(By.CLASS_NAME, "listingRowOuter")

    file_path = f'static/{f_name}.csv'
    with open(file_path, 'w', encoding='utf-8', newline='') as file_csv:
        writer = csv.writer(file_csv)
        writer.writerow(['Hotel Name', 'Location', 'Price', 'Rating', 'Reviews', 'Link'])

        for listing in listings:
            try:
                name = listing.find_element(By.CLASS_NAME, "makeFlex.flexOne.appendLeft20").text.strip()
            except:
                name = "NA"

            try:
                location = listing.find_element(By.CLASS_NAME, "font12.greyText").text.strip()
            except:
                location = "NA"

            try:
                price = listing.find_element(By.CLASS_NAME, "latoBlack.font26.blackText.appendBottom5").text.replace('₹', '').strip()
            except:
                price = "NA"

            try:
                rating = listing.find_element(By.CLASS_NAME, "greenText").text.strip()
            except:
                rating = "NA"
            
            try:
                reviews = listing.find_element(By.CLASS_NAME, "reviewCount").text.strip()
            except:
                reviews = "NA"

            try:
                link = listing.find_element(By.TAG_NAME, "a").get_attribute("href")
            except:
                link = "NA"

            writer.writerow([name, location, price, rating, reviews, link])
    
    driver.quit()
    return file_path
