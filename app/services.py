import os
import json
import requests
from openai import OpenAI

PROPERTY_KEY = os.getenv("PROPERTY_KEY")
PROPERTY_HOST = os.getenv("PROPERTY_HOST")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def fetch_property_details(address, use_dummy=False):
    """Fetch property details using the real API, or return dummy data if needed."""
    
    if use_dummy:
        dummy_path = os.path.join(os.path.dirname(__file__), "..", "tests", "dummy_data.json")
        with open(dummy_path, "r") as dummy_data:
            content = dummy_data.read().strip()
            return json.loads(content)

    url = f"https://{PROPERTY_HOST}/property"
    headers = {
        "X-RapidAPI-Key": PROPERTY_KEY,
        "X-RapidAPI-Host": PROPERTY_HOST
    }
    params = {"address": address}

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()

            # Extract only relevant fields
            return {
                "address": f"{data.get('streetAddress', 'N/A')}, {data.get('city', 'N/A')}, {data.get('state', 'N/A')} {data.get('zipcode', 'N/A')}",
                "city": data.get("city", "N/A"),
                "state": data.get("state", "N/A"),
                "zipcode": data.get("zipcode", "N/A"),
                "country": data.get("country", "USA"),
                "latitude": data.get("latitude", "N/A"),
                "longitude": data.get("longitude", "N/A"),
                "size": f"{data.get('livingArea', 'N/A')} sqft",
                "bedrooms": data.get("bedrooms", "N/A"),
                "bathrooms": data.get("bathrooms", "N/A"),
                "year_built": data.get("yearBuilt", "N/A"),
                "home_type": data.get("homeType", "N/A"),
                "price": f"${data.get('price', 'N/A')}",
                "tax_paid": f"${data.get('taxAnnualAmount', 'N/A')} (Last Year)",
                "property_tax_rate": f"{data.get('propertyTaxRate', 'N/A')}%",
                "monthly_hoa_fee": f"${data.get('monthlyHoaFee', 'N/A')}" if data.get("monthlyHoaFee") else "None",
                "zestimate": f"${data.get('zestimate', 'N/A')}",
                "price_per_sqft": f"${data.get('pricePerSquareFoot', 'N/A')}",
                "lot_size": data.get("lotSize", "N/A"),
                "description": data.get("description", "No description available."),
                "schools": [
                    {
                        "name": school.get("name", "N/A"),
                        "distance": f"{school.get('distance', 'N/A')} miles",
                        "rating": school.get("rating", "N/A"),
                        "grades": school.get("grades", "N/A"),
                    }
                    for school in data.get("schools", [])
                ],
                "image_url": data.get("imgSrc", ""),
                "zillow_url": f"https://www.zillow.com{data.get('url', '')}"
            }
        else:
            return None
    except Exception as e:
        print(f"Error fetching property details: {e}")
        return None

def generate_property_summary(property_info):
    """Use OpenAI API to generate a summary of the property details."""
    if not OPENAI_API_KEY:
        print("ERROR: Missing OpenAI API Key!")
        return "Error: OpenAI API key is missing."
    
    client = OpenAI(api_key=OPENAI_API_KEY)

    prompt = f"""
    Generate a detailed, engaging real estate property overview based on the following details:

    Address: {property_info.get("address", "N/A")}
    City: {property_info.get("city", "N/A")}, {property_info.get("state", "N/A")}
    Size: {property_info.get("size", "N/A")}
    Bedrooms: {property_info.get("bedrooms", "N/A")}
    Bathrooms: {property_info.get("bathrooms", "N/A")}
    Year Built: {property_info.get("year_built", "N/A")}
    Price: {property_info.get("price", "N/A")}
    Lot Size: {property_info.get("lot_size", "N/A")}
    Description: {property_info.get("description", "N/A")}

    Nearby Schools:
    {', '.join([f"{school['name']} ({school['rating']}/10) - {school['distance']}" for school in property_info.get("schools", [])])}

    Provide a compelling summary of the home, its features, and why it would be a great place to live.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": prompt}]
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating property summary: {e}")
        return "Error generating property summary."
