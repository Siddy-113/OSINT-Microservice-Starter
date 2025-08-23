from fastapi import APIRouter
from pydantic import BaseModel
from app.tasks.monitor_tasks import monitor_keywords

router = APIRouter()

class KeywordRequest(BaseModel):
    action: str
    keywords: list[str]

@router.post("/keywords")
async def manage_keywords(request: KeywordRequest):
    if request.action == "add":
        task = monitor_keywords.apply_async(args=[request.keywords])
        return {"status": "success", "message": "Monitoring started", "task_id": task.id}
    elif request.action == "remove":
        # For now just simulate
        return {"status": "success", "message": f"Removed keywords: {request.keywords}"}
    else:
        return {"status": "error", "message": "Invalid action"}
