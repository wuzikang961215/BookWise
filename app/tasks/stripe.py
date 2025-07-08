import os
import requests
import logging
from app.tasks.celery_app import celery_app  # 👈 force app registration
from app.models import Payment
from app.db import SessionLocal

STRIPE_URL = os.getenv("STRIPE_URL", "https://stripe-small-leaf-5404.fly.dev")

@celery_app.task(
    name="app.tasks.stripe.create_stripe_payment_intent",  # 👈 this line is key
    bind=True,
    max_retries=5,
    default_retry_delay=10
)
def create_stripe_payment_intent(self, payment_id: str, booking_id: str, user_id: str, amount: float):
    idempotency_key = f"{user_id}-{booking_id}-{payment_id}"

    try:
        response = requests.post(
            f"{STRIPE_URL}/v1/payment_intents",
            json={
                "amount": int(amount * 100),
                "metadata": {
                    "booking_id": booking_id,
                    "user_id": user_id
                }
            },
            headers={"Idempotency-Key": idempotency_key}
        )
        response.raise_for_status()
        pi_id = response.json()["id"]
        logging.warning(f"[TASK] Got Stripe PaymentIntent ID: {pi_id}")

        with SessionLocal() as db:
            payment = db.query(Payment).filter(Payment.id == payment_id).first()
            if payment:
                payment.payment_intent_id = pi_id
                db.commit()
                logging.warning(f"[TASK] Updated DB for payment {payment_id}")
            else:
                logging.error(f"[TASK] Payment {payment_id} not found in DB")

    except requests.RequestException as e:
        logging.warning(f"[TASK] Stripe failed, retrying: {e}")
        self.retry(exc=e)
    except requests.RequestException as e:
        logging.warning(f"Stripe failed, retrying: {e}")
        self.retry(exc=e)
    except Exception as e:
        logging.exception(f"[FATAL] Stripe task failed permanently: {e}")
