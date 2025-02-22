import os
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

# Product URL
URL = "https://store.fcbarcelona.com/en-us/products/fc-barcelona-awayws-shirt-24-25"

# Headers to mimic a real browser visit
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Email configuration
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

def send_email():
    """Send an email alert when the product is in stock."""
    msg = MIMEText(f"The product is back in stock! Check it here: {URL}")
    msg["Subject"] = "Inventory Alert - FC Barcelona Away Jersey"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print("📧 Email sent!")
    except Exception as e:
        print(f"❌ Email failed: {e}")

def check_stock():
    """Check if the product is available."""
    try:
        # Fetch the webpage
        response = requests.get(URL, headers=HEADERS, timeout=10)

        # Check if request was successful
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            return
    
        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Convert page text to lowercase for case-insensitive search 
        page_text = soup.text.lower()

        # Check if "sold out" appears in any form
        if "sold out" in page_text:
            print("❌ Still out of stock.")
        else:
            print("🚨 Product is available! 🚨")
            send_email()
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")

# Run the function once to test
check_stock()