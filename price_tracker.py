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


def price_tracker(URL, headers, threshold, tar_currency, email_ad=None, pw=None, to_ad=None):
    """

    :param URL: type str
        URL of target website
    :param headers: type str
        User-agent information (can be found by searching for "User-Agent" in Google
    :param threshold: type float or int
        The maximum value you would like to pay for the selected item
    :param tar_currency: type str
        The currency in which you would like to pay for the product
    :param email_ad: type str
        The user's email address
    :param pw: type str
        The user's email password or key
    :param to_ad: type str
        The "to" email address: can be same as email_ad
    :return: type str
        Whether or not the product is available at or below the threshold value
        If selected, an email be be sent to to_ad
    """
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    currency = 0

    title = soup.find("div", {"class": "title"})
    price = soup.find("div", {"class": "price"})
    if title and price:
        title = title.get_text()
        price = price.get_text()
    else:
        print("Currently for use on Dick's Sporting Goods only.")
        return

    if price[0] == "$":
        currency = "USD"

    if float(price[1:]) <= float(threshold) and currency == tar_currency:
        print("Deal time!")
        if email_ad and pw and to_ad:
            send_mail(email_ad, pw, to_ad)

    else:
        print("Not today, bruh...")

    print(title)
    print(price)
    print(currency)

URL = "https://www.dickssportinggoods.com/p/strikeforce-linds-heritage-mens-performance-bowling-shoes-20sfcmlndshrt" \
      "grhbstg/20sfcmlndshrtgrhbstg"

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                         "Version/14.0.1 Safari/605.1.15"}

threshold = 160.0