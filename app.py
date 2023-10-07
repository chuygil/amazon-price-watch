import os
import time
import schedule
import requests
from bs4 import BeautifulSoup
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

ASIN = "B001HBIPE4"
URL = f"https://www.amazon.com/dp/{ASIN}/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1",
}

def job():
    session = requests.Session()
    r = session.get(URL, headers=HEADERS)

    soup = BeautifulSoup(r.content, "html5lib")
    price_element_whole = soup.find("span", class_="a-price-whole")
    price_element_fraction = soup.find("span", class_="a-price-fraction")

    if price_element_whole and price_element_fraction:
        price_whole = price_element_whole.get_text(strip=True)
        price_fraction = price_element_fraction.get_text(strip=True)
        price = price_whole + price_fraction
        price_float = float(price)
        target_price = 29.99
        if price_float > target_price:
            print(price_float)
            send_email(price_float)
        else:
            print(price_float)
    else:
        print("Price Not Found")
    

def send_email(price):
    to_emails = [
        (os.environ.get('TO_EMAIL_ONE'), 'JG 1'),
        (os.environ.get('TO_EMAIL_TWO'), 'JG 2')
    ]

    message = Mail(
        from_email = os.environ.get('FROM_EMAIL'),
        to_emails = to_emails,
        subject=f'Amazon Price Alert - ASIN: {ASIN}',
        html_content=f'<p>ASIN: {ASIN}</p><p>Price: ${price}</p>')

    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        # print(response.body)
        # print(response.headers)
    except Exception as e:
        print(e.message)
    

if __name__ == "__main__":
    schedule.every(1).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
