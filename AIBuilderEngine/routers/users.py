from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

from core.database import get_db
from core.auth import get_current_user
from models import User
from fastapi import UploadFile, File, Form
from typing import List, Optional
from services.notifier import send_support_email, send_approval_email

router = APIRouter()


class SMTPConfigRequest(BaseModel):
    host: str
    port: int
    username: str
    password: str
    from_email: str


def get_activation_layout(content: str):
    return f"""
    <html>
    <head>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
        <style>body {{ font-family: 'Inter', sans-serif; }}</style>
    </head>
    <body class="bg-slate-50 flex items-center justify-center min-h-screen">
        <div class="max-w-md w-full mx-4 bg-white p-8 rounded-2xl shadow-xl border border-slate-100 text-center">
            <div class="mb-6">
                <span class="text-2xl font-bold text-slate-900">Touch<span class="text-blue-600">Craft</span></span>
            </div>
            {content}
            <div class="mt-8 pt-6 border-t border-slate-100">
                <p class="text-xs text-slate-400">© 2024 TouchCraft Builder Admin Panel</p>
            </div>
        </div>
    </body>
    </html>
    """


@router.get("/activate-user/{user_id:path}", response_class=HTMLResponse)
async def activate_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return get_activation_layout("<h2 class='text-xl'>User Not Found</h2>")
    if user.is_active:
        return get_activation_layout("<h2 class='text-xl'>Already Active</h2>")

    try:
        user.is_active = True
        db.commit()

        # Отправляем письмо пользователю
        user_name = user.full_name if user.full_name else "TouchCraft User"
        await send_approval_email(user_email=user.email, user_name=user_name)

        return get_activation_layout("<h2 class='text-xl'>Success!</h2>")
    except Exception as e:
        db.rollback()
        return get_activation_layout(f"<p class='text-red-500'>Error: {str(e)}</p>")

PLAN_LIMITS = {
    "freemium": {"max_sites": 1, "custom_domains": False, "ai_images": False, "lead_forms": False},
    "starter": {"max_sites": 5, "custom_domains": True, "ai_images": True, "lead_forms": True},
    "pro": {"max_sites": 10, "custom_domains": True, "ai_images": True, "lead_forms": True, "catalogs": True}
}


@router.get("/user/me")
async def get_user_profile(current_user: User = Depends(get_current_user)):
    tier = (current_user.subscription_tier or "freemium").lower()

    active_count = sum(1 for p in current_user.projects if p.status == "active")

    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "is_active": current_user.is_active,
        "subscription_tier": tier,
        "subscription_status": current_user.subscription_status,
        "limits": PLAN_LIMITS.get(tier, PLAN_LIMITS["freemium"]),
        "ai_generations_used": current_user.ai_generations_used,
        "project_count": len(current_user.projects),
        "active_project_count": active_count,
        "smtp_config": current_user.smtp_config or {
            "host": "", "port": 587, "username": "", "password": "", "from_email": ""
        }
    }

class UserProfileUpdate(BaseModel):
    full_name: str

@router.patch("/user/me")
async def update_user_profile(
    profile_data: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    current_user.full_name = profile_data.full_name
    db.commit()
    return {"status": "success", "message": "Профиль обновлен"}


@router.post("/user/smtp")
async def save_smtp_config(
        config: SMTPConfigRequest,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    current_user.smtp_config = config.dict()
    db.commit()
    return {"status": "success", "message": "SMTP настройки сохранены"}


@router.post("/user/support")
async def submit_support_ticket(
        subject: str = Form(...),
        message: str = Form(...),
        files: List[UploadFile] = File(default=[]),
        current_user: User = Depends(get_current_user)
):
    attachments = []

    for f in files:
        if f.filename:
            content = await f.read()
            attachments.append({
                "filename": f.filename,
                "content": content,
                "content_type": f.content_type or "application/octet-stream"
            })

    await send_support_email(
        user_email=current_user.email,
        user_name=current_user.full_name or "TouchCraft User",
        subject=subject,
        message_text=message,
        attachments=attachments
    )

    return {"status": "success", "message": "Support ticket sent successfully"}
