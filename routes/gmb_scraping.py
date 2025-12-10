from fastapi import APIRouter, HTTPException, BackgroundTasks
from models.gmb_search import GMBSearchRequest, BusinessLead
from utils.gmb_scraper import scrape_gmb_data
from typing import List

router = APIRouter(
    prefix="/scrape",
    tags=["Scraping"]
)

@router.post("/gmb", response_model=dict)
async def scrape_google_my_business(search_request: GMBSearchRequest):
    """
    Scrapes Google My Business (Google Maps) for business leads based on search criteria.
    
    **Example Request:**
    ```json
    {
        "query": "tech companies",
        "location": "Lagos, Nigeria",
        "max_results": 20
    }
    ```
    
    **Returns:**
    - List of business leads with contact information
    - Total count of businesses found
    """
    try:
        print(f"🚀 Starting GMB scraping: {search_request.query} in {search_request.location}")
        
        # Call the scraper (synchronous function)
        businesses = scrape_gmb_data(
            query=search_request.query,
            location=search_request.location,
            max_results=search_request.max_results
        )
        
        return {
            "status": "success",
            "query": search_request.query,
            "location": search_request.location,
            "total_found": len(businesses),
            "results": businesses
        }
        
    except Exception as e:
        print(f"❌ GMB scraping error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Scraping failed: {str(e)}"
        )
