from fastapi import Request, APIRouter

router = APIRouter()

@router.post("/webhooks/stripe")
async def webhook_stripe(request: Request):
    payload = await request.json()
    print("📦 Received webhook payload:", payload)
    return {"status": "received", "type": payload.get("type")}
