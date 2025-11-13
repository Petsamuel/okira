from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from routes import scraping

app = FastAPI(
    title="Okira API",
    description="API for helping Nigerian businesses automate lead generation and outreach.",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Endpoints ---

@app.get("/", include_in_schema=False)
async def root():
    """Redirects the root URL to the API documentation."""
    return RedirectResponse(url="/docs")

@app.get("/health", tags=["Health"])
def health_check():
    """Endpoint to check if the API is running."""
    return {"status": "healthy"}

app.include_router(scraping.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)