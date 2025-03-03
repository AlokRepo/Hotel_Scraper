from flask import Flask, request, render_template, send_file
from booking_scraper import web_scrapper_booking
from expedia_scraper import web_scrapper_expedia
from hotels_scraper import web_scrapper_hotels
from trivago_scraper import web_scrapper_trivago
from agoda_scraper import web_scrapper_agoda
from airbnb_scraper import web_scrapper_airbnb
from makemytrip_scraper import web_scrapper_makemytrip


import os

def ensure_static_folder():
    if not os.path.exists("static"):
        os.makedirs("static")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form['url']
    filename = "hotels_data"
    
    if "booking.com" in url:
        file_path = web_scrapper_booking(url, filename)
    elif "expedia" in url:
        file_path = web_scrapper_expedia(url, filename)
    elif "hotels" in url:
        file_path = web_scrapper_hotels(url, filename)
    elif "trivago" in url:
        file_path = web_scrapper_trivago(url, filename)
    elif "agoda" in url:
        file_path = web_scrapper_agoda(url, filename)
    elif "airbnb" in url:
        file_path = web_scrapper_airbnb(url, filename)
    elif "makemytrip" in url:
        file_path = web_scrapper_makemytrip(url, filename)
    else:
        return "❌ Unsupported website. Please provide a Booking.com or Expedia URL."

    if file_path:
        return send_file(file_path, as_attachment=True)
    else:
        return "❌ Failed to scrape data. The website structure may have changed."

if __name__ == '__main__':
    app.run(debug=True)
