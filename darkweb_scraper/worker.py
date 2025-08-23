from celery import Celery
from app.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

celery = Celery(
    "darkweb_scraper",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)

celery.conf.task_routes = {
    "app.tasks.search_tasks.*": {"queue": "search"},
    "app.tasks.monitor_tasks.*": {"queue": "monitor"},
}
