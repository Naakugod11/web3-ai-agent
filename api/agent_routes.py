from fastapi import APIRouter, Depends
from core.models import AgentQuery, AgentResponse
from core.middleware import require_auth
from services.agent import analyze

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
