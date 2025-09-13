from fastapi import APIRouter
from app.worker import celery

router = APIRouter()

@router.get("/{task_id}")
async def get_results(task_id: str):
    task_result = celery.AsyncResult(task_id)
    if task_result.state == "PENDING":
        return {"status": "pending", "task_id": task_id}
    if task_result.state == "SUCCESS":
        return {"status": "complete", "task_id": task_id, "data": task_result.result}
    return {"status": task_result.state.lower(), "task_id": task_id}
