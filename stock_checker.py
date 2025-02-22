import requests
from bs4 import BeautifulSoup

# Product URL
URL = "https://store.fcbarcelona.com/en-us/products/fc-barcelona-awayws-shirt-24-25"

# Headers to mimic a real browser visit
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

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
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")

# Run the function once to test
check_stock()