from fastapi import FastAPI
from app.routes import search_router, monitor_router, results_router
from app.logger import log

app = FastAPI(title="OSINT Dark Web Scraper Microservice")

# include routers
app.include_router(search_router, prefix="", tags=["Search"])
app.include_router(monitor_router, prefix="", tags=["Monitor"])
app.include_router(results_router, prefix="", tags=["Results"])

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "service": "darkweb-scraper"}
