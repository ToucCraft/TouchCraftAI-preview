import subprocess
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, timedelta
from sqlalchemy import func
from starlette.responses import RedirectResponse

# --- SQLAdmin Imports ---
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from core.database import get_db
from models import User, Project, Lead

router = APIRouter(prefix="/admin")


# ==========================================
# 1. FASTAPI ADMIN API ROUTES (Your existing code)
# ==========================================

class SubscriptionUpdate(BaseModel):
    tier: str


@router.get("/users")
async def admin_get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [
        {
            "id": u.id,
            "email": u.email,
            "is_active": u.is_active,
            "project_count": len(u.projects),
            "created_at": u.created_at,
            "subscription_tier": u.subscription_tier,
            "subscription_status": u.subscription_status
        } for u in users
    ]


@router.post("/users/{user_id}/subscription")
async def admin_update_subscription(user_id: str, data: SubscriptionUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user: raise HTTPException(404, "User not found")

    if data.tier not in ["freemium", "starter", "pro"]:
        raise HTTPException(400, "Invalid tier")

    user.subscription_tier = data.tier
    db.commit()
    return {"status": "success", "tier": user.subscription_tier}


@router.post("/users/{user_id}/toggle")
async def admin_toggle_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user: raise HTTPException(404, "User not found")
    user.is_active = not user.is_active
    db.commit()
    return {"status": "success", "is_active": user.is_active}


@router.get("/projects")
async def admin_get_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    return [
        {
            "id": p.id, "name": p.business_name, "status": p.status,
            "user_email": p.owner.email if p.owner else "No Owner",
            "url": p.preview_url, "port": p.port, "created_at": p.created_at
        } for p in projects
    ]


@router.get("/projects/{project_id}/logs")
async def admin_get_project_logs(project_id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project or not project.container_id:
        raise HTTPException(404, "Project or active container not found")
    try:
        result = subprocess.check_output(["docker", "logs", "--tail", "100", project.container_id],
                                         stderr=subprocess.STDOUT)
        return {"logs": result.decode("utf-8")}
    except Exception as e:
        return {"logs": f"Error retrieving logs: {str(e)}"}


@router.get("/kpi")
async def admin_get_kpis(db: Session = Depends(get_db)):
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)

    total_users = db.query(User).count()
    new_users_30d = db.query(User).filter(User.created_at >= thirty_days_ago).count()

    freemium_count = db.query(User).filter(User.subscription_tier == "freemium").count()
    starter_count = db.query(User).filter(User.subscription_tier == "starter").count()
    pro_count = db.query(User).filter(User.subscription_tier == "pro").count()

    active_starter = db.query(User).filter(User.subscription_tier == "starter",
                                           User.subscription_status == "active").count()
    active_pro = db.query(User).filter(User.subscription_tier == "pro", User.subscription_status == "active").count()

    mrr = (active_starter * 29) + (active_pro * 79)

    total_projects = db.query(Project).count()
    total_ai_used = db.query(func.sum(User.ai_generations_used)).scalar() or 0

    return {
        "mrr": mrr,
        "total_users": total_users,
        "new_users_30d": new_users_30d,
        "subscriptions": {
            "freemium": freemium_count,
            "starter": starter_count,
            "pro": pro_count
        },
        "total_projects": total_projects,
        "total_ai_generations": total_ai_used
    }


# ==========================================
# 2. SQLADMIN UI CONFIGURATION
# ==========================================

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form.get("username"), form.get("password")

        if username == "username" and password == "password":
            # Set the session token
            request.session.update({"token": "admin_session_token"})
            return True

        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        # Check if the token exists and is correct
        if not token or token != "admin_session_token":
            return False

        return True


authentication_backend = AdminAuth(secret_key="secret_key")


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.full_name, User.is_active, User.subscription_tier]
    column_searchable_list = [User.email, User.full_name]
    icon = "fa-solid fa-user"


class ProjectAdmin(ModelView, model=Project):
    column_list = [Project.id, Project.business_name, Project.status, Project.user_id]
    column_searchable_list = [Project.business_name]
    icon = "fa-solid fa-folder-open"


class LeadAdmin(ModelView, model=Lead):
    column_list = [Lead.id, Lead.project_id, Lead.created_at]
    icon = "fa-solid fa-envelope"


def setup_admin(app, engine):
    admin = Admin(app, engine, authentication_backend=authentication_backend, title="TouchCraft Admin")
    admin.add_view(UserAdmin)
    admin.add_view(ProjectAdmin)
    admin.add_view(LeadAdmin)
    return admin
