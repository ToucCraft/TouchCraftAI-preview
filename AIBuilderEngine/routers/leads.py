from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from core.database import get_db
from core.auth import get_current_user
from models import User, Project, Lead
from services.email_sender import send_lead_email
from services.notifier import send_landing_contact_email

router = APIRouter()

class LeadSubmission(BaseModel):
    form_data: Dict[str, Any]

class LandingContactRequest(BaseModel):
    name: str
    email: str
    message: str
    honeypot: str = ""

@router.get("/{project_id}/leads")
async def get_project_leads(project_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project: raise HTTPException(404, "Project not found")
    leads = db.query(Lead).filter(Lead.project_id == project_id).order_by(Lead.created_at.desc()).all()
    return {"status": "success", "leads": leads}

@router.post("/{project_id}/submit")
async def submit_lead(project_id: str, submission: LeadSubmission, db: Session = Depends(get_db)):
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project: raise HTTPException(404, "Project not found")

        new_lead = Lead(project_id=project_id, form_data=submission.form_data)
        db.add(new_lead)
        db.commit()

        if project.owner and project.owner.smtp_config:
            smtp_config = project.owner.smtp_config
            recipient_email = smtp_config.get('from_email') or smtp_config.get('username') or project.owner.email
            await send_lead_email(
                smtp_config=smtp_config, to_email=recipient_email,
                lead_data=submission.form_data, project_name=project.business_name or project_id
            )
        return {"status": "success", "message": "Message sent!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/contact")
async def submit_landing_contact(request: LandingContactRequest):
    try:
        if request.honeypot: return {"status": "success", "message": "Message sent!"}
        await send_landing_contact_email(name=request.name, email=request.email, message_text=request.message)
        return {"status": "success", "message": "Message sent successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
