import os
# import time
# import schedule
import requests
from bs4 import BeautifulSoup
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

ASINS = ["B001HBIPE4", "B0C9R5SJSF", "B0C9R5NNRB", "B0C9R5VGY7"]
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1",
}

def job():
    for asin in ASINS:
        url = f"https://www.amazon.com/dp/{asin}/"
        session = requests.Session()
        r = session.get(url, headers=HEADERS)

        soup = BeautifulSoup(r.content, "html5lib")
        price_element_whole = soup.find("span", class_="a-price-whole")
        price_element_fraction = soup.find("span", class_="a-price-fraction")

        if price_element_whole and price_element_fraction:
            price_whole = price_element_whole.get_text(strip=True)
            price_fraction = price_element_fraction.get_text(strip=True)
            price = price_whole + price_fraction
            price_float = float(price)

            match asin:
                case "B001HBIPE4":
                    if price_float > 29.99:
                        send_email(asin, price_float)
                    else:
                        print(f"{asin},${price_float}")
                case "B0C9R5SJSF":
                    if price_float > 1.49:
                        send_email(asin, price_float)
                    else:
                        print(f"{asin},${price_float}")
                case "B0C9R5NNRB":
                    if price_float > 1.99:
                        send_email(asin, price_float)
                    else:
                        print(f"{asin},${price_float}")
                case "B0C9R5VGY7":
                    if price_float > 4.99:
                        send_email(asin, price_float)
                    else:
                        print(f"{asin},${price_float}")
                case _:
                    print("Something went wrong.")
        else:
            print(f"{asin},Price Not Found")
    

def send_email(asin, price):
    to_emails = [
        # (os.environ.get('TO_EMAIL_ONE'), os.environ.get('EMAIL_ONE_NAME')),
        # (os.environ.get('TO_EMAIL_TWO'), os.environ.get('EMAIL_TWO_NAME')),
        (os.environ.get('ADMIN_EMAIL'), os.environ.get('ADMIN_NAME'))
    ]

    message = Mail(
        from_email = os.environ.get('ADMIN_EMAIL'),
        to_emails = to_emails,
        subject=f'Amazon Price Alert - ASIN: {asin} - Price: ${price}',
        html_content=f'<p>See subject line.</p>')

    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(f">>> Email sent: {asin}/${price} - Status Code: {response.status_code}")
    except Exception as e:
        print(e.message)
    

if __name__ == "__main__":
    job()

# schedule.every(1).minutes.do(job)
# while True:
#     schedule.run_pending()
#     time.sleep(1)
