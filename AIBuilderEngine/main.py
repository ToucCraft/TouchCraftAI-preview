import secrets
from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
import subprocess

from starlette.middleware.sessions import SessionMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from core.config import settings
from core.database import engine, Base, SessionLocal
from models import Project
from routers import users, projects, generation, leads, billing
from admin import setup_admin
from admin import router as admin_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

# 1. Fixes the Mixed Content (HTTP/HTTPS) issue behind your proxy
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")

# 2. Enables session cookies for the Admin Panel login token
app.add_middleware(
    SessionMiddleware,
    secret_key="lC8YDIy6Jdf33cBDXLhi4mBQIKD1323jZgXdphk1",
    same_site="lax",
    https_only=True # Since you are running behind an HTTPS proxy
)

# --- START OF SWAGGER AUTHENTICATION ---
security = HTTPBasic()

def get_current_admin_user(credentials: HTTPBasicCredentials = Depends(security)):
    # Updated to match admin.py credentials
    correct_username = secrets.compare_digest(credentials.username, "grifnawtizec")
    correct_password = secrets.compare_digest(credentials.password, "_hOTry|K7BT1)3Y99i+D2|bds")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint(username: str = Depends(get_current_admin_user)):
    return get_openapi(title=app.title, version=app.version, routes=app.routes)

@app.get("/docs", include_in_schema=False)
async def get_documentation(username: str = Depends(get_current_admin_user)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="API Documentation")
# --- END OF SWAGGER AUTHENTICATION ---

origins = [
    "https://api-builder.touch-craft.com",
    "https://builder.touch-craft.com",
    "https://touchcraftai.com",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.touch-craft\.com",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- FAVICON ---
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)


@app.on_event("startup")
def restore_containers():
    print("🔄 Checking active sites status...")
    db = SessionLocal()
    try:
        active_projects = db.query(Project).filter(Project.status == "active").all()
        for proj in active_projects:
            if proj.container_id:
                try:
                    subprocess.run(["docker", "start", proj.container_id], check=False)
                    print(f"✅ Restored site {proj.business_name} on port {proj.port}")
                except Exception as e:
                    print(f"⚠️ Could not restore {proj.id}: {e}")
    finally:
        db.close()

app.include_router(users.router, prefix="/api/v1", tags=["Users"])
app.include_router(generation.router, prefix="/api/v1", tags=["Generation & AI"])
app.include_router(leads.router, prefix="/api/v1", tags=["Leads & Forms"])
app.include_router(projects.router, prefix="/api/v1", tags=["Projects"])
app.include_router(admin_router, prefix="/api/v1", tags=["Admin Custom"])
app.include_router(billing.router, prefix="/api/v1", tags=["Billing"])

# Mount the sqladmin panel
setup_admin(app, engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, proxy_headers=True, forwarded_allow_ips="*")