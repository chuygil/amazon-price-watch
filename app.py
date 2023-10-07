import time
import schedule
import requests
from bs4 import BeautifulSoup

def get_price(url, headers):
    session = requests.Session()
    response = session.get(url, headers=headers)

    soup = BeautifulSoup(response.content, "html5lib")
    price_element_whole = soup.find("span", class_="a-price-whole")
    price_element_fraction = soup.find("span", class_="a-price-fraction")

    if price_element_whole and price_element_fraction:
        price_whole = price_element_whole.get_text(strip=True)
        price_fraction = price_element_fraction.get_text(strip=True)
        price = price_whole + price_fraction
        print(price)
    else:
        print("Price Not Found")

if __name__ == "__main__":
    URL = "https://www.amazon.com/dp/B001HBIPE4/"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT": "1",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1",
    }

    schedule.every(3).minutes.do(get_price, url=URL, headers=HEADERS)
    while True:
        schedule.run_pending()
        time.sleep(1)
