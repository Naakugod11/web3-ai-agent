from fastapi import FastApi

app = FastApi(
    title="Web3 AI Agent",
    description="AI-powered Web3 agent with SIWE authentication",
    cersion="0.1.0",
)

@app.get("/health")
async def health():
    return {"status": "alive"}
