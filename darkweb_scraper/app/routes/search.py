from fastapi import APIRouter, HTTPException
from app.models import SearchRequest, SearchAcceptedResponse
from app.tasks.search_tasks import run_search
from app.logger import log

router = APIRouter()

@router.post("/search", response_model=SearchAcceptedResponse, tags=["Search"])
async def submit_search(req: SearchRequest):
    # Simple validation done by pydantic
    try:
        task = run_search.apply_async(args=[req.identifier_type, req.identifier_value])
        log.info("submitted_search_task", extra={"task_id": task.id, "id_type": req.identifier_type})
        return {"message": "Dark web search task accepted.", "task_id": task.id}
    except Exception as e:
        log.warning("submit_search_failed", extra={"err": str(e)})
        raise HTTPException(status_code=500, detail="Failed to enqueue search task")
