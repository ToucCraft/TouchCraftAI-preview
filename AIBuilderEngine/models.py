from sqlalchemy import Column, String, Integer, JSON, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    smtp_config = Column(JSON, nullable=True)
    subscription_tier = Column(String, default="freemium")  # 'freemium', 'starter', 'pro'
    subscription_status = Column(String, default="active")  # 'active', 'past_due', 'canceled'
    stripe_customer_id = Column(String, nullable=True)
    stripe_subscription_id = Column(String, nullable=True)
    ai_generations_used = Column(Integer, default=0)
    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")


class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, index=True)  # UUID
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    business_name = Column(String)
    business_description = Column(Text)
    language = Column(String, default="en")
    site_config = Column(JSON)
    status = Column(String, default="draft")  # draft, active, stopped, building
    port = Column(Integer, unique=True, nullable=True)
    container_id = Column(String, nullable=True)
    preview_url = Column(String, nullable=True)
    theme_color = Column(String, default="#000000")
    logo_url = Column(String, nullable=True)
    favicon_url = Column(String, nullable=True)
    analytics_config = Column(JSON, nullable=True)  # {"google_id": "...", "fb_pixel": "..."}
    cookie_policy = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner = relationship("User", back_populates="projects")
    leads = relationship("Lead", back_populates="project", cascade="all, delete-orphan")


class Lead(Base):
    __tablename__ = "leads"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id"))
    form_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    project = relationship("Project", back_populates="leads")
