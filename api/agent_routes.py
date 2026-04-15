from fastapi import APIRouter, Depends, HTTPException
from core.models import AgentQuery, AgentResponse, WalletAnalysis
from core.middleware import require_auth
from services.agent import analyze
from services.chain import get_wallet_summary

router = APIRouter(prefix="/agent", tags=["agent"])

@router.post("/analyze", response_model=AgentResponse)
async def agent_analyze(query: AgentQuery, wallet: str = Depends(require_auth)):
    try:
        analysis = analyze(query.prompt, wallet)
        return AgentResponse(
            query=query.prompt,
            analysis=analysis,
            raw_response=analysis.model_dumpt_json(),
        )
    except Exception as e:
        return AgentResponse(
            query=query.prompt,
            analysis=None,
            raw_response=str(e),
        )

@router.get("/wallet", response_model=WalletAnalysis)
async def wallet_info(wallet: str = Depends(require_auth)):
    try:
        data = get_wallet_summary(wallet)
        return WalletAnalysis(
            address=data["address"],
            eth_balance=data["eth_balance"],
            transaction_count=data["transaction_count"],
            is_contract=data["is_contract"],
            risk_level="low" if data["transaction_count"] > 10 else "medium",
            summary=f"Wallet holds {data['eth_balance']:.4f} ETH with {data['transaction_count']} transactions",
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))