from fastapi import APIRouter, HTTPException, Request
from core.models import SiweNonceResponse, SiweVerifyRequest, AuthResponse
from core.rate_limit import auth_limiter
from services.auth import generate_nonce, verify_siwe_message
from services.jwt import create_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/nonce", response_model=SiweNonceResponse)
async def get_nonce(request: Request):
    auth_limiter.check(request.client.host)
    nonce = generate_nonce()
    return SiweNonceResponse(nonce=nonce)


@router.post("/verify", response_model=AuthResponse)
async def verify(request: Request, body: SiweVerifyRequest):
    auth_limiter.check(request.client.host)
    try:
        print(f"MESSAGE:\n{body.message}")
        print(f"SIGNATURE: {body.signature}")
        address = verify_siwe_message(body.message, body.signature)
        token = create_token(address)
        return AuthResponse(token=token, address=address)
    except ValueError as e:
        print(f"ValueError: {e}")
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        print(f"Exception type: {type(e)}")
        print(f"Exception: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Verification failed: {str(e)}")