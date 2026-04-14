from fastapi import APIRouter, HTTPException
from core.models import SiweNonceResponse, SiweVerifyRequest, SiweSession
from services.auth import generate_nonce, verify_siwe_message

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/nonce", response_model=SiweNonceResponse)
async def get_nonce():
    nonce = generate_nonce()
    return SiweNonceResponse(nonce=nonce)

@router.pos("/verify", response_model=SiweSession)
async def verify(request: SiweVerifyRequest):
    try:
        address = verify_siwe_message(request.message, request.signature)
        return SiweSession(address=address, chain_id=1)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Verification failed: {str(e)}")