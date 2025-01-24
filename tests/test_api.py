import os
import requests
from dotenv import load_dotenv

load_dotenv()
PROPERTY_KEY = os.getenv("PROPERTY_KEY")
PROPERTY_HOST = os.getenv("PROPERTY_HOST")

def test_real_estate_api():
    """Test if the API returns property details using an address."""
    
    url = f"https://{PROPERTY_HOST}/property"
    headers = {
        "x-rapidapi-key": PROPERTY_KEY,
        "x-rapidapi-host": PROPERTY_HOST
    }
    params = {
        "address": "1600 Amphitheatre Pkwy, Mountain View, CA"
    }

    print(PROPERTY_HOST)
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        print("✅ API Test Passed: ", response.json())
    else:
        print("❌ API Test Failed: ", response.status_code, response.text)

if __name__ == "__main__":
    test_real_estate_api()
