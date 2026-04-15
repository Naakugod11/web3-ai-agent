from fastapi import FastAPI
from api.routes import router as auth_router
from api.agent_routes import router as agent_router
from core.exceptions import AppException, app_exception_handler

app = FastAPI(
    title="Web3 AI Agent",
    description="AI-powered Web3 agent with SIWE authentication",
    cersion="0.1.0",
)

app.add_exception_handler(AppException, app_exception_handler)
app.include_router(auth_router)
app.include_router(agent_router)

@app.get("/health")
async def health():
    return {"status": "alive"}
