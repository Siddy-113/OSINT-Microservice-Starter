from fastapi import APIRouter, HTTPException
from celery.result import AsyncResult
from worker import celery  # worker.py exposes celery
from app.logger import log

router = APIRouter()

@router.get("/results/{task_id}", tags=["Results"])
async def get_results(task_id: str):
    res = AsyncResult(task_id, app=celery)
    state = res.state
    if state == "PENDING":
        return {"status": "pending", "task_id": task_id}
    if state == "PROGRESS":
        return {"status": "in-progress", "meta": res.info}
    if state == "SUCCESS":
        return {"status": "complete", "task_id": task_id, "data": res.result}
    if state == "FAILURE":
        log.warning("task_failure", extra={"task_id": task_id, "err": str(res.result)})
        raise HTTPException(status_code=500, detail="Task failed")
    return {"status": state.lower()}
