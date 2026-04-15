from pydantic import BaseModel

# --- SIWE Auth ---

class SiweNonceResponse(BaseModel):
    nonce: str

class SiweVerifyRequest(BaseModel):
    message: str
    signature: str

class SiweSession(BaseModel):
    address: str
    chain_id: int

# --- AI Agent ---

class AgentQuery(BaseModel):
    prompt: str
    wallet_address: str | None = None

class TokenAnalysis(BaseModel):
    token: str
    price_usd: float
    market_cap: float | None = None
    risk_score: int
    summary: str

class WalletAnalysis(BaseModel):
    address: str
    eth_balance: float
    transaction_count: int
    is_contract: bool
    risk_level: str
    summary: str

class AgentResponse(BaseModel):
    query: str
    analysis: TokenAnalysis | WalletAnalysis | None = None
    raw_response: str

class AuthResponse(BaseModel):
    token: str
    address: str