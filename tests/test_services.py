from unittest.mock import patch


def test_fetch_property_valid(client):
    """Test fetching property with valid input"""
    mock_data = {
        "streetAddress": "123 Test Street",
        "city": "Test",
        "state": "CA",
        "zipcode": "12345",
        "country": "USA",
        "livingArea": "2000",
        "bedrooms": "2",
        "bathrooms": "2",
        "yearBuilt": "2000",
        "homeType": "Apartment",
        "price": "100000",
        "pricePerSquareFoot": "10000",
        "lotSize": "1000",
        "description": "Test description",
        "schools": [
            {
                "name": "Test School",
                "distance": "2",
                "rating": "10",
                "grades": "1-12",
            }
        ],
        "imgSrc": "www.com",
        "url": "/test"
    }

    mock_response = {
        "address": "123 Test Street, Test, CA",
        "details": {
            "address": "123 Test Street, Test, CA 12345",
            "city": "Test",
            "state": "CA",
            "zipcode": "12345",
            "country": "USA",
            "size": "2000 sqft",
            "bedrooms": "2",
            "bathrooms": "2",
            "year_built": "2000",
            "home_type": "Apartment",
            "price": "$100000",
            "price_per_sqft": "$10000",
            "lot_size": "1000",
            "description": "Test description",
            "schools": [
                {
                    "name": "Test School",
                    "distance": "2 miles",
                    "rating": "10",
                    "grades": "1-12",
                }
            ],
            "image_url": "www.com",
            "zillow_url": "https://www.zillow.com/test"
        }
    }

    with patch("app.services._fetch_property_details", return_value=mock_data):
        response = client.post(
            "/api/fetch-property",
            json={"address": "123 Test Street, Test, CA"}
        )
        assert response.status_code == 200
        assert response.get_json() == mock_response
    

def test_fetch_property_no_address(client):
    """Test fetching property details with no address"""
    mock_response = {"error": "Address is required"}

    response = client.post("/api/fetch-property", json={"address": ""})
    assert response.status_code == 400
    assert response.get_json() == mock_response


def test_fetch_property_invalid(client):
    """Test fetching property with invalid input"""
    mock_response = {
        "error": "Could not fetch property details. Try another address."
    }

    with patch("app.services._fetch_property_details", return_value=None):
        response = client.post(
            "/api/fetch-property",
            json={"address": "123 Test Street, Test, CA"}
        )
        assert response.status_code == 404
        assert response.get_json() == mock_response


def test_generate_property_summary(client):
    """Test AI-generated property summary"""
    mock_response = {
        "summary": "Beautiful house with 3 bedrooms and a large backyard."
    }
    
    with patch("app.services._call_llm", return_value=mock_response["summary"]):
        response = client.post(
            "/api/generate-summary",
            json={"property_info": {"bedrooms": "3"}}
        )
        assert response.get_json() == mock_response


def test_generate_property_summary_no_info(client):
    """Test AI-generated property summary"""
    mock_response = {"error": "Property information is required"}
    
    response = client.post(
        "/api/generate-summary",
        json={"property_info": None}
    )
    assert response.get_json() == mock_response
