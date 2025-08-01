from fastapi import Request, HTTPException, status
import os
from dotenv import load_dotenv
from itsdangerous import URLSafeSerializer
from fastapi.responses import RedirectResponse

load_dotenv()

# --- Configurable Secrets ---
API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY", "mathrocks123")
USERNAME = os.getenv("USERNAME", "admin")
PASSWORD = os.getenv("PASSWORD", "demo123")

# --- Serializer for cookie-based login ---
serializer = URLSafeSerializer(SECRET_KEY)

# --- API Header Authorization (for curl, CLI, Postman, etc.) ---
def authorize(request: Request):
    key = request.headers.get("X-API-Key")
    print("Received key:", key)
    print("Expected key:", API_KEY)
    if key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing API key"
        )

# --- Session-based browser login (for /login UI access) ---
def set_session(username: str):
    return serializer.dumps({"user": username})

def get_session(token: str):
    try:
        data = serializer.loads(token)
        return data.get("user")
    except Exception:
        return None

def ensure_logged_in(request: Request):
    token = request.cookies.get("session")
    user = get_session(token) if token else None
    if user != USERNAME:
        return RedirectResponse(url="/login", status_code=302)

def authorize_combined(request: Request):
    # Check session login first
    token = request.cookies.get("session")
    user = get_session(token) if token else None
    if user == USERNAME:
        return

    # Fallback to API key
    key = request.headers.get("X-API-Key")
    if key == API_KEY:
        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Unauthorized"
    )
