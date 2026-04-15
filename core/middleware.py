from fastapi import Request, HTTPException
from web3 import Web3
from services.jwt import verify_token


async def require_auth(request: Request) -> str:
    auth = request.headers.get("Authorization")

    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing auth token")

    token = auth.split(" ")[1]

    try:
        wallet_address = verify_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    if not Web3.is_address(wallet_address):
        raise HTTPException(status_code=401, detail="Invalid wallet address in token")

    return Web3.to_checksum_address(wallet_address)