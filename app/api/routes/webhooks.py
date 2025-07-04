from fastapi import APIRouter, Request
from app.services.payments import handle_stripe_webhook

router = APIRouter()

@router.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    payload = await request.json()
    try:
        handle_stripe_webhook(payload)
        return {"received": True}
    except Exception as e:
        # Optional: add logger or Sentry here
        return {"error": str(e)}
