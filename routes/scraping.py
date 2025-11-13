from fastapi import APIRouter
from models.search import LinkedInSearchRequest
from utils.scrape import scrape_linkedin_data

router = APIRouter(
    prefix="/scrape",
    tags=["Scraping"]
)

@router.post("/linkedin")
async def scrape_linkedin(search_request: LinkedInSearchRequest):
    """
    Searches LinkedIn based on company and/or people criteria provided in the request body.
    """
    # The Pydantic model is converted to a dict.
    # `exclude_unset=True` ensures that only provided fields are in the dictionary,
    # which is useful for the scraping function.
    search_criteria = search_request.model_dump(exclude_unset=True, by_alias=True)

    # TODO: Replace this mock implementation with a real scraping task.
    # For long-running tasks, consider using background tasks.
    scraped_leads = scrape_linkedin_data(search_criteria)

    return {"status": "search complete", "results": scraped_leads}