from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.jwt import verify_token

security = HTTPBearer()

async def require_auth(request: Request) -> str:
    """Dependancy that extracts and verifies JWT from Authorization header."""
    auth = request.headers.get("Authorization")

    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing auth token")

    token = auth.split(" ")[1]

    try:
        wallet_address = verify_token(token)
        return wallet_address
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
