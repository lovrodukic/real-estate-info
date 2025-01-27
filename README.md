# Real Estate Information Retrieval System

## Overview
This project is a Flask-based web application that retrieves and summarizes real
estate property information using an external API and AI text generation. Users
can input an address, and the system fetches property details, generates a
summary using OpenAI's API, and displays property information. The Web UI is
mainly used for testing API and functionality.

## Features
- **Retrieve Property Information:** Fetches details such as size, number of
  rooms, estimated value, etc.
- **Generate AI-Powered Summary:** Uses OpenAI's API to summarize property
  details
- **Fetch Nearby Schools:** Provides a list of schools near the address with
  details like name, distance, and ratings.
- **User-Friendly Interface:** Web-based form for address input and displaying
  results.
- **Error Handling & Validation:** Validates inputs and handles API errors
  gracefully.
- **API Testing:** Page for testing and visualizing RapidAPI JSON response
  without AI summary.

## Tech Stack
- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, JavaScript
- **External APIs:**
  - [Zillow Property Data API](https://rapidapi.com/apimaker/api/zillow-com1/)
  - [OpenAI API](https://platform.openai.com/docs/api-reference/chat)
- **Testing:** pytest

## API Endpoints
### `POST /api/fetch-property`
Retrieves property details for a given address.
- **Input:** `{ "address": "1600 Amphitheatre Pkwy, Mountain View, CA" }`
- **Output:** JSON with property metadata (size, price, bedrooms, etc.)

### `POST /api/generate-summary`
Generates an AI-powered property overview.
- **Input:** `{ "property_info": ... }`
- **Output:** AI-generated HTML summary

## Installation & Setup
1. Clone the repository and navigate to the project folder:
   ```bash
   git clone <repo_url>
   cd REAL-ESTATE-INFO
   ```
2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables in a `.env` file:
   ```
   PROPERTY_KEY=your_property_api_key
   PROPERTY_HOST=your_property_api_host
   OPENAI_API_KEY=your_openai_api_key
   ```
5. Run the application:
   ```bash
   python run.py
   ```
6. Access it at `http://127.0.0.1:5000/`.

## Assumptions
- The external property API provides accurate and complete details.
- AI-generated summaries are useful and informative.
- Error handling covers various API failures and input validation cases.

## Testing
Run unit tests using pytest:
```bash
pytest tests/test_services
```

## Future Enhancements
- Support for additional real estate APIs to improve data accuracy.
- Enhanced UI with interactive maps and better visual representation.
- Advanced AI summarization techniques to enhance accuracy.
