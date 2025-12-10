# Google My Business Scraper Setup

## Installation

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

**That's it!** No browser downloads needed. This scraper uses BeautifulSoup4 to parse Google Search results - lightweight and fast!

## Usage

### API Endpoint

**POST** `/scrape/gmb`

### Request Body

```json
{
  "query": "tech companies",
  "location": "Lagos, Nigeria",
  "max_results": 20
}
```

### Example with cURL

```bash
curl -X POST "http://localhost:8000/scrape/gmb" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "restaurants",
    "location": "Victoria Island, Lagos",
    "max_results": 10
  }'
```

### Example with Python Requests

```python
import requests

response = requests.post(
    "http://localhost:8000/scrape/gmb",
    json={
        "query": "tech companies",
        "location": "Lagos, Nigeria",
        "max_results": 15
    }
)

businesses = response.json()["results"]
for business in businesses:
    print(f"{business['name']} - {business.get('phone', 'No phone')}")
```

## Response Format

```json
{
  "status": "success",
  "query": "tech companies",
  "location": "Lagos, Nigeria",
  "total_found": 15,
  "results": [
    {
      "name": "Tech Solutions Ltd",
      "address": "123 Herbert Macaulay Way, Lagos",
      "phone": "+234 803 123 4567",
      "website": "https://techsolutions.ng",
      "rating": 4.5,
      "reviews_count": 120,
      "category": "Software Company",
      "gmb_url": "https://maps.google.com/..."
    }
  ]
}
```

## Search Tips

### Good Query Examples
- "software companies" + "Lagos, Nigeria"
- "digital marketing agencies" + "Abuja, Nigeria"
- "restaurants" + "Victoria Island, Lagos"
- "lawyers" + "Ikeja, Lagos"

### Location Specificity
- **More specific** = Better results
- ✅ "Victoria Island, Lagos, Nigeria"
- ✅ "Lekki Phase 1, Lagos"
- 🔶 "Lagos, Nigeria" (broader)
- ❌ "Nigeria" (too broad)

## Running the Server

```bash
cd backend
python main.py
```

The API will be available at:
- **Swagger Docs**: http://localhost:8000/docs
- **API Base**: http://localhost:8000

## Troubleshooting

### Error: "playwright not installed"
Run: `pip install playwright && playwright install chromium`

### Error: "Browser executable not found"
Run: `playwright install chromium`

### Network Timeout
- Increase timeout in `gmb_scraper.py`
- Check your internet connection
- Try with fewer max_results

### No Results Found
- Try broader queries
- Check if location is spelled correctly
- Some areas may have limited GMB listings

## Performance

- **Expected Speed**: 2-5 seconds per business (including page load)
- **Max Results**: Recommended 20-50 per request
- **For Large Scrapes**: Implement background tasks (Celery/ARQ)
