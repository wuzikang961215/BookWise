from app.tasks.celery_app import celery_app
from app.tasks import stripe

print("✅ Celery worker booting from app.tasks.worker")
