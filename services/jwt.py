import jwt
from datetime import datetime, timedelta, timezone
from core.config import settings

def create_token(wallet_address: str) -> str:
    payload = {
        "sub": wallet_address,
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")

def verify_token(token: str) -> str:
    """Verify JWT and return wallet address. Raises on invalid/expired."""
    payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
    return payload["sub"]
