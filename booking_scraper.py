import requests
from bs4 import BeautifulSoup
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

def web_scrapper_booking(web_url, f_name):
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    ensure_static_folder()

    try:
        response = requests.get(web_url, headers=headers, timeout=10)
        response.raise_for_status()
        time.sleep(random.uniform(1, 3))

        soup = BeautifulSoup(response.text, 'html.parser')
        hotel_divs = soup.find_all('div', role="listitem")

        if not hotel_divs:
            return None

        file_path = f'static/{f_name}.csv'
        with open(file_path, 'w', encoding='utf-8', newline='') as file_csv:
            writer = csv.writer(file_csv)
            writer.writerow(['Hotel Name', 'Location', 'Price', 'Rating', 'Score', 'Reviews', 'Link'])

            for hotel in hotel_divs:
                hotel_name = hotel.find('div', class_="f6431b446c a15b38c233")
                hotel_name = hotel_name.get_text(strip=True) if hotel_name else "NA"

                location = hotel.find('span', class_="aee5343fdb def9bc142a")
                location = location.get_text(strip=True) if location else "NA"

                price = hotel.find('span', class_="f6431b446c fbfd7c1165 e84eb96b1f")
                price = price.get_text(strip=True).replace('₹\xa0', '') if price else "NA"

                rating = hotel.find('div', class_="a3b8729ab1 e6208ee469 cb2cbb3ccb")
                rating = rating.get_text(strip=True) if rating else "NA"

                score = hotel.find('div', class_="a3b8729ab1 d86cee9b25")
                score = score.get_text(strip=True).split(' ')[-1] if score else "NA"

                review = hotel.find('div', class_="abf093bdfe f45d8e4c32 d935416c47")
                review = review.get_text(strip=True) if review else "NA"

                link_tag = hotel.find('a', href=True)
                link = f"{link_tag['href']}" if link_tag else "NA"

                writer.writerow([hotel_name, location, price, rating, score, review, link])

        return file_path
    except requests.RequestException:
        return None
