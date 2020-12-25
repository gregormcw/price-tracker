import requests
from bs4 import BeautifulSoup
import smtplib


def send_mail(email_ad, pw, to_ad):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(email_ad, pw)
    subject = "{} is now available for {}: at or below your threshold price!".format(title, price)
    body = "Click the link to make your purchase: {}".format(URL)
    msg = f"subject: {subject}\n\n{body}"
    server.sendmail(email_ad, to_ad, msg)
    print("Email sent!")
    server.quit()


def price_tracker(URL, headers, threshold, email_ad=None, pw=None, to_ad=None):
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    title = soup.find("div", {"class": "title"}).get_text()
    price = soup.find("div", {"class": "price"}).get_text()

    if price[0] == "$":
        currency = "USD"

    if float(price[1:]) <= float(threshold):
        print("Deal time!")
        if email_ad and pw and to_ad:
            send_mail(email_ad, pw, to_ad)

    else:
        print("Not today, bruh...")

    print(title)
    print(price)
    print(currency)

URL = "https://www.dickssportinggoods.com/p/strikeforce-linds-heritage-mens-performance-bowling-shoes-20sfcmlndshrtgr" \
      "hbstg/20sfcmlndshrtgrhbstg"

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                         "Version/14.0.1 Safari/605.1.15"}