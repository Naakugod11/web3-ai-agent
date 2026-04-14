from fastapi import APIRouter
from core.models import AgentQuery, AgentResponse
from services.agent import analyze

router = APIRouter(prefix="/agent", tags=["agent"])

@router.post("/analyze", response_model=AgentResponse)
async def agent_analyze(query: AgentQuery):
    try:
        analysis = analyze(query.prompt, query.wallet_address)
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
