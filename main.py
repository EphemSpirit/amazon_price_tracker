from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import smtplib
from email.message import EmailMessage
import os

load_dotenv()

AMAZON_URL = "https://appbrewery.github.io/instant_pot/"

res = requests.get(AMAZON_URL)
res.raise_for_status()

soup = BeautifulSoup(res.text, "html.parser")
product_title = soup.find(name="span", id="productTitle").getText()
price = soup.find(name="span", class_="aok-offscreen").getText()
price = float(price.split("$")[-1])
print(product_title)

def send_email(title: str, product_price: float) -> None:
    body = f"{title} is now ${product_price}"
    msg = EmailMessage()
    msg["Subject"] = "Amazon Price Alert!"
    msg["From"] = os.getenv("GMAIL_ADDRESS")
    msg["To"] = os.getenv("GMAIL_ADDRESS")

    msg.set_content(body)

    with smtplib.SMTP(os.getenv("SMTP_HOST"), port=587) as connection:
        connection.starttls()
        connection.login(
            user=os.getenv("GMAIL_ADDRESS"),
            password=os.getenv("GMAIL_APP_PASSWORD")
        )
        connection.send_message(msg)

if price < 100.00:
    send_email(product_title, price)
