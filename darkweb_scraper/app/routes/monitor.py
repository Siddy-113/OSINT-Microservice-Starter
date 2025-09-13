from fastapi import APIRouter
from pydantic import BaseModel
from app.tasks.monitor_tasks import monitor_keywords

router = APIRouter()

class KeywordRequest(BaseModel):
    action: str
    keywords: list[str]

@router.post("/keywords", response_model=KeywordAcceptedResponse)
async def manage_keywords(request: KeywordRequest):
    if request.action == "add":
        task = monitor_keywords.apply_async(args=[request.keywords])
        return {"status": "success", "message": "Monitoring started", "task_id": task.id}
    elif request.action == "remove":
        # Integration point: remove from persistent keyword store (to be added)
        return {"status": "success", "message": f"Removed keywords: {request.keywords}"}
