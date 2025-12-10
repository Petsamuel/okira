from pydantic import BaseModel, Field
from typing import Optional

class GMBSearchRequest(BaseModel):
    """
    Request model for Google My Business search.
    """
    query: str = Field(..., description="Search query (e.g., 'restaurants', 'tech companies', 'lawyers')")
    location: str = Field(..., description="Location to search in (e.g., 'Lagos, Nigeria', 'Abuja, Nigeria')")
    max_results: Optional[int] = Field(20, description="Maximum number of results to return (default: 20, max: 100)", ge=1, le=100)
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "tech companies",
                "location": "Lagos, Nigeria",
                "max_results": 20
            }
        }

class BusinessLead(BaseModel):
    """
    Model representing a business lead from GMB.
    """
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    rating: Optional[float] = None
    reviews_count: Optional[int] = None
    category: Optional[str] = None
    gmb_url: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Tech Solutions Ltd",
                "address": "123 Herbert Macaulay Way, Lagos, Nigeria",
                "phone": "+234 803 123 4567",
                "website": "https://techsolutions.ng",
                "rating": 4.5,
                "reviews_count": 120,
                "category": "Software Company",
                "gmb_url": "https://maps.google.com/..."
            }
        }
