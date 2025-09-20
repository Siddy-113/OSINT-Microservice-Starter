from fastapi import APIRouter, HTTPException
from app.models import KeywordRequest, KeywordAcceptedResponse
from app.tasks.monitor_tasks import monitor_keywords
from app.logger import log

router = APIRouter()

# Temporary in-memory watchlist (migrate to DB later)
_watchlist = set()

@router.post("/monitor/keywords", response_model=KeywordAcceptedResponse, tags=["Monitor"])
async def manage_keywords(req: KeywordRequest):
    if req.action == "add":
        _watchlist.update(req.keywords)
        task = monitor_keywords.apply_async(args=[list(req.keywords)])
        log.info("monitor_keywords_added", extra={"count": len(req.keywords), "task_id": task.id})
        return {"status": "success", "message": "Keywords added and monitoring started.", "task_id": task.id}
    elif req.action == "remove":
        for k in req.keywords:
            _watchlist.discard(k)
        log.info("monitor_keywords_removed", extra={"count": len(req.keywords)})
        return {"status": "success", "message": "Keywords removed.", "task_id": None}
    else:
        raise HTTPException(status_code=400, detail="Invalid action")
