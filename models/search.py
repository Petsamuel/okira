from pydantic import BaseModel, Field
from typing import Optional

class CompanySearch(BaseModel):
    name: Optional[str] = Field(None, description="Company name to search for.", alias="companyname")
    size: Optional[str] = Field(None, description="Company size (e.g., '11-50 employees').")
    industry: Optional[str] = Field(None, description="Industry of the company.")
    description: Optional[str] = Field(None, description="Keywords in company description.")
    company_type: Optional[str] = Field(None, description="Company type (e.g., 'Public Company', 'Privately Held').")
    location: Optional[str] = Field(None, description="Company's location.")
    country: Optional[str] = Field(None, description="Company's country.")
    url: Optional[str] = Field(None, description="Company's website URL.")

class PeopleSearch(BaseModel):
    name: Optional[str] = Field(None, description="Person's name to search for.")
    company_name: Optional[str] = Field(None, description="Company the person works at.", alias="companyName")
    job_title: Optional[str] = Field(None, description="Person's job title.", alias="jobTitle")
    location: Optional[str] = Field(None, description="Person's location.")
    url: Optional[str] = Field(None, description="URL of the person's LinkedIn profile.")

class LinkedInSearchRequest(BaseModel):
    company: Optional[CompanySearch] = None
    people: Optional[PeopleSearch] = None