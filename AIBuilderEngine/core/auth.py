import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from sqlalchemy.orm import Session
from core.database import get_db
from core.config import settings
from models import User
from services.notifier import send_activation_link
import requests

# OAuth2 for Swagger and FastAPI
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"https://{settings.AUTH0_DOMAIN}/authorize",
    tokenUrl=f"https://{settings.AUTH0_DOMAIN}/oauth/token",
)


def verify_token(token: str):
    try:
        jwks_client = jwt.PyJWKClient(f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json")
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=settings.AUTH0_AUDIENCE,
            issuer=f"https://{settings.AUTH0_DOMAIN}/"
        )
        return payload
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_token(token)
    auth0_id = payload.get("sub")
    email = payload.get("https://api-builder.touch-craft.com/email")
    full_name = payload.get("https://api-builder.touch-craft.com/name")

    if not auth0_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = db.query(User).filter(User.id == auth0_id).first()

    if not user:
        if not email or not full_name:
            userinfo_url = f"https://{settings.AUTH0_DOMAIN}/userinfo"
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(userinfo_url, headers=headers)

            if response.status_code == 200:
                userinfo = response.json()
                email = email or userinfo.get("email")
                full_name = full_name or userinfo.get("name") or userinfo.get("nickname")

        user = User(
            id=auth0_id,
            email=email,
            full_name=full_name,
            is_active=False
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        await send_activation_link(user.id, user.email)

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Registration successful. Please wait for admin activation."
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is pending activation by admin."
        )

    return user
