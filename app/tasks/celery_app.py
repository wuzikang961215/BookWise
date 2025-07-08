import os
from dotenv import load_dotenv
load_dotenv()

from celery import Celery

celery_app = Celery(
    "bookwise",
    broker=os.getenv("REDIS_URL"),
    backend=os.getenv("REDIS_BACKEND"),
)

celery_app.conf.update(
    task_routes={
        "app.tasks.stripe.*": {"queue": "payment_intents"},
        "app.tasks.emails.*": {"queue": "emails"},
        "app.tasks.cleanup.*": {"queue": "maintenance"}
    },
    broker_transport_options={
        "queue_name_prefix": "bookwise::"
    },
    redis_backend_transport_options={
        "key_prefix": "bookwise::"
    }
)
