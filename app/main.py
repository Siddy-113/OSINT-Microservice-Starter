from fastapi import FastAPI, BackgroundTasks, HTTPException, Header
from celery import Celery
from celery.result import AsyncResult
import os
from typing import Optional
from dotenv import load_dotenv
from uvicorn import run

# --- Configuration ---
# It's recommended to use environment variables for these settings
load_dotenv()
API_KEY = os.getenv("API_KEY", "your-secret-api-key") # Replace with a secure key management system
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

# --- FastAPI App Initialization ---
app = FastAPI(
    title="OSINT Microservice Template",
    description="A starter template for an OSINT microservice.",
    version="1.0.0"
)

# --- Celery Initialization ---
celery_app = Celery(
    "tasks",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND
)
# Import tasks so Celery can find them
celery_app.conf.imports = ('app.tasks',)


# --- Security Dependency ---
async def verify_api_key(x_api_key: str = Header(...)):
    """Dependency to verify the API key."""
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

# --- API Endpoints ---
@app.get("/", tags=["General"])
async def read_root():
    """Root endpoint with a welcome message."""
    return {"message": "Welcome to the OSINT Microservice."}

@app.get("/health", tags=["General"])
async def health_check():
    """Health check endpoint to verify service is running."""
    return {"status": "ok"}

@app.post("/analyze", status_code=202, tags=["Analysis"], dependencies=[]) # Add `dependencies=[verify_api_key]` to secure
async def start_analysis(payload: dict):
    """
    Accepts a payload and starts a background analysis task.
    This is an example endpoint. You should replace the payload
    with a Pydantic model specific to your service's needs.
    """
    # Example: a placeholder task is called.
    # Replace 'app.tasks.placeholder_task' with your actual task.
    task = celery_app.send_task('app.tasks.placeholder_task', args=[payload])
    return {"message": "Analysis task accepted.", "task_id": task.id}


@app.get("/results/{task_id}", tags=["Analysis"], dependencies=[]) # Add `dependencies=[verify_api_key]` to secure
async def get_task_results(task_id: str):
    """
    Retrieves the status and result of a background task.
    """
    task_result = AsyncResult(task_id, app=celery_app)

    if task_result.state == 'PENDING':
        # Task is waiting or does not exist
        return {"task_id": task_id, "status": "PENDING", "data": None}
    elif task_result.state == 'FAILURE':
        # Task failed, return the error
        return {"task_id": task_id, "status": "FAILURE", "data": str(task_result.info)}
    else:
        # Task is complete or in progress
        return {
            "task_id": task_id,
            "status": task_result.state,
            "data": task_result.result
        }

if __name__=="__main__":
    run(app)