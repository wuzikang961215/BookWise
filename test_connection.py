from dotenv import load_dotenv
load_dotenv()

from app.tasks.celery_app import celery_app  # 👈 这行确保 Celery 用你配置的 Redis
from app.tasks.stripe import create_stripe_payment_intent

result = create_stripe_payment_intent.delay(
    "339f1b21-79e8-48fe-bcd6-0388fb187685",
    "da86cf5a-2285-40dd-995a-91e8bf9d6cf3",
    "f8a328d0-a686-4dfc-bc78-f3d384be5029",
    88.8
)
print(result)
