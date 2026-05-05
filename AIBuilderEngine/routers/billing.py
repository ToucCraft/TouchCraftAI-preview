import stripe
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from core.database import get_db
from core.auth import get_current_user
from core.config import settings
from models import User

router = APIRouter()
stripe.api_key = settings.STRIPE_SECRET_KEY

STRIPE_PRICES = {
    "starter": "price_...",
    "pro": "price_..."
}

class CheckoutRequest(BaseModel):
    plan: str

@router.post("/stripe/create-checkout-session")
async def create_checkout_session(
    request: CheckoutRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    plan = request.plan
    if plan not in STRIPE_PRICES:
        raise HTTPException(400, "Invalid plan")

    try:
        checkout_session = stripe.checkout.Session.create(
            customer=current_user.stripe_customer_id,
            customer_email=current_user.email if not current_user.stripe_customer_id else None,
            payment_method_types=['card'],
            line_items=[{'price': STRIPE_PRICES[plan], 'quantity': 1}],
            mode='subscription',
            success_url=f"{settings.FRONTEND_URL.rstrip('/')}/settings?tab=billing&status=success",
            cancel_url=f"{settings.FRONTEND_URL.rstrip('/')}/settings?tab=billing",
            metadata={"user_id": current_user.id, "plan": plan}
        )
        return {"url": checkout_session.url}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/stripe/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        print(f"❌ Webhook signature error: {e}")
        raise HTTPException(400, "Invalid payload")

    if event.type == 'checkout.session.completed':
        session = event.data.object
        metadata = getattr(session, 'metadata', None)
        user_id = getattr(metadata, 'user_id', None) if metadata else None
        plan = getattr(metadata, 'plan', None) if metadata else None

        if not user_id:
            print("⚠️ Webhook received but no user_id found in metadata!")
            return {"status": "ignored", "reason": "no metadata"}

        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.stripe_customer_id = getattr(session, 'customer', None)
            user.stripe_subscription_id = getattr(session, 'subscription', None)
            user.subscription_tier = plan
            user.subscription_status = 'active'
            db.commit()
            print(f"✅ Successfully updated user {user_id} to plan {plan}")

    elif event.type == 'customer.subscription.deleted':
        subscription = event.data.object
        sub_id = getattr(subscription, 'id', None)

        user = db.query(User).filter(User.stripe_subscription_id == sub_id).first()
        if user:
            user.subscription_tier = 'freemium'
            user.subscription_status = 'canceled'
            db.commit()
            print("📉 Subscription canceled for user")

    return {"status": "success"}
