from fastapi import FastAPI
from app.routes import search, monitor, results

# Initialize FastAPI app
app = FastAPI(
    title="Dark Web Scraper Microservice",
    description="Microservice for targeted and continuous dark web scraping with OPSEC measures.",
    version="1.0.0",
)

# Register routers
app.include_router(search.router, prefix="/search", tags=["Search"])
app.include_router(monitor.router, prefix="/monitor", tags=["Monitor"])
app.include_router(results.router, prefix="/results", tags=["Results"])

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "message": "Dark Web Scraper API is running"}
