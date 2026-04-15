import json
from anthropic import Anthropic
from core.config import settings
from core.models import TokenAnalysis
from services.chain import get_wallet_summary

client = Anthropic(api_key=settings.anthropic_api_key)

SYSTEM_PROMPT = """You are a Web3 AI analyst. When asked about a token or crypto topic,
respond ONLY with valid JSON matching this exact schema:

{
    "token": "TOKEN_SYMBOL",
    "price_usd": 0.0,
    "market_cap": null,
    "risk_score": 1-10,
    "summary": "Brief analysis"
}

No markdown, no explanation, just the JSON object."""

def analyze(prompt: str, wallet_address: str | None = None) -> TokenAnalysis:
    context=prompt
    if wallet_address:
        try:
            wallet_data = get_wallet_summary(wallet_address)
            context += f"\n\nUser wallet data: {json.dumps(wallet_data)}"
        except Exception:
            context += f"\n\nUser wallet: {wallet_address} (chain data unavailable)"
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": context}],
    )

    raw = response.content[0].text
    data = json.loads(raw)
    return TokenAnalysis(**data)
