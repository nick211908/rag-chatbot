import asyncio
import jwt
from supabase import create_client, Client
from backend.config import settings
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def get_supabase_client() -> Client:
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise HTTPException(
            status_code=500,
            detail="Supabase credentials not configured"
        )
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

async def signup_user(email: str, password: str):
    supabase = get_supabase_client()
    try:
        response = await asyncio.to_thread(
            lambda: supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {"data": {}}
            })
        )
        return {
            "user": response.user,
            "session": response.session
        }
    except Exception as e:
        print(f"Signup error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

async def login_user(email: str, password: str):
    supabase = get_supabase_client()
    try:
        response = await asyncio.to_thread(
            lambda: supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
        )
        if not response.session:
            raise HTTPException(status_code=401, detail="Login failed - no session")
        return {
            "user": response.user,
            "session": response.session,
            "access_token": response.session.access_token,
            "user_id": response.user.id
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {str(e)}")
        raise HTTPException(status_code=401, detail=f"Invalid credentials: {str(e)}")

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        
        if settings.SUPABASE_JWT_SECRET:
            payload = jwt.decode(
                token,
                settings.SUPABASE_JWT_SECRET,
                algorithms=["HS256"],
                options={"verify_aud": False}
            )
        else:
            supabase = get_supabase_client()
            user_response = await asyncio.to_thread(
                lambda: supabase.auth.get_user(token)
            )
            if not user_response or not user_response.user:
                raise HTTPException(status_code=401, detail="Invalid token")
            return {"id": user_response.user.id, "email": user_response.user.email}
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"id": user_id, "email": payload.get("email")}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
