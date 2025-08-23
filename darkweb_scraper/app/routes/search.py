from fastapi import APIRouter
from pydantic import BaseModel
import uuid
from app.tasks.search_tasks import run_search

router = APIRouter()

class SearchRequest(BaseModel):
    identifier_type: str
    identifier_value: str

@router.post("/")
async def search_target(request: SearchRequest):
    task = run_search.apply_async(args=[request.identifier_type, request.identifier_value])
    return {
        "message": "Dark web search task accepted.",
        "task_id": task.id
    }
