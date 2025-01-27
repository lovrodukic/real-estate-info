import os
import json
import requests
from flask import request, jsonify
from openai import OpenAI
from app.config import Config


def _fetch_property_details(address, use_dummy=False):
    """Fetch property details using the property API or dummy data"""
    if use_dummy:
        dummy_path = os.path.join(
            os.path.dirname(__file__), "..", "tests", "dummy_data.json"
        )
        with open(dummy_path, "r") as dummy_data:
            content = dummy_data.read().strip()
            return json.loads(content)

    url = f"https://{Config.PROPERTY_HOST}/property"
    headers = {
        "X-RapidAPI-Key": Config.PROPERTY_KEY,
        "X-RapidAPI-Host": Config.PROPERTY_HOST
    }
    params = {"address": address}

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200 and response.text != '{}':
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Error fetching property details: {e}")
        return None


def _call_llm(prompt):
    """Make a request to OpenAI API given a prompt"""
    if not Config.OPENAI_API_KEY:
        print("ERROR: Missing OpenAI API Key!")
        return "Error: OpenAI API key is missing."
    
    client = OpenAI(api_key=Config.OPENAI_API_KEY)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": prompt}]
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating property summary: {e}")
        return "Error generating property summary."


###########################  Public APIs  ###########################

def fetch_property():
    """API for extracting relevant property details for a given address"""
    address = request.get_json().get("address")

    if not address:
        return jsonify({"error": "Address is required"}), 400

    data = _fetch_property_details(address)

    if not data:
        return jsonify({
            "error": "Could not fetch property details. Try another address."
        }), 404
    
    # Extract relevant fields from API response
    property_info = {
        "address": (
            f"{data.get('streetAddress', 'N/A')}, "
            f"{data.get('city', 'N/A')}, "
            f"{data.get('state', 'N/A')} {data.get('zipcode', 'N/A')}"
        ),
        "city": data.get("city", "N/A"),
        "state": data.get("state", "N/A"),
        "zipcode": data.get("zipcode", "N/A"),
        "country": data.get("country", "USA"),
        "size": f"{data.get('livingArea', 'N/A')} sqft",
        "bedrooms": data.get("bedrooms", "N/A"),
        "bathrooms": data.get("bathrooms", "N/A"),
        "year_built": data.get("yearBuilt", "N/A"),
        "home_type": data.get("homeType", "N/A"),
        "price": f"${data.get('price', 'N/A')}",
        "price_per_sqft": f"${data.get('pricePerSquareFoot', 'N/A')}",
        "lot_size": data.get("lotSize", "N/A"),
        "description": data.get("description", "No description found."),
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

    return jsonify({
        "address": address,
        "details": property_info
    })


def generate_summary():
    """API for generating property overview given property information"""
    data = request.get_json()
    property_info = data.get("property_info")

    if not property_info:
        return jsonify({"error": "Property information is required"}), 400
    
    prompt = f"""
    Generate a detailed, engaging real estate property overview based on
    the following details:

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
    {', '.join(
        [
            f"{school['name']} ({school['rating']}/10) - {school['distance']}"
            for school in property_info.get("schools", [])
        ]
    )}

    Return the response **only as valid HTML**, without Markdown or code blocks.
    - Include a short introductory `<p>` paragraph summarizing the property.
    - Follow the introduction with a `<ul>` list of key features using `<li>` tags.
    - **Do not wrap the output in triple backticks (` ``` `).**
    - The response should be directly insertable into an HTML page without modification.
    """

    summary = _call_llm(prompt)

    return jsonify({
        "summary": summary
    })
