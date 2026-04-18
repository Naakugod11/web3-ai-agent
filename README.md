# web3-ai-agent

AI-powered Web3 agent with SIWE authentication and structured outputs — built with FastAPI, Web3.py, and Anthropic SDK.

## What is this?

A backend API that lets users authenticate with their Ethereum wallet (Sign-In with Ethereum), then interact with an AI agent that returns structured, validated analyses. The agent has access to real on-chain data — it reads your wallet's ETH balance, transaction history, and account type to provide context-aware responses.

Every AI response is forced through Pydantic schemas, meaning no hallucinated garbage — just clean, typed JSON you can pipe into any frontend or downstream service.

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│   Client     │────▶│  FastAPI      │────▶│  Auth Service   │
│  (Wallet)    │     │  Middleware   │     │  SIWE + JWT     │
└─────────────┘     └──────┬───────┘     └─────────────────┘
                           │
                    ┌──────▼───────┐
                    │  Agent Route  │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              │                         │
     ┌────────▼────────┐     ┌─────────▼──────────┐
     │  Chain Service   │     │  AI Agent Service   │
     │  (Web3.py +      │     │  (Anthropic SDK +   │
     │   Alchemy RPC)   │     │   Structured Output) │
     └─────────────────┘     └────────────────────┘
```

## Auth Flow

1. Client requests a nonce → `GET /auth/nonce`
2. User signs the nonce with their Ethereum wallet (SIWE standard)
3. Client sends signed message → `POST /auth/verify`
4. Server verifies signature, returns a JWT token
5. Client includes JWT in all subsequent requests → `Authorization: Bearer <token>`
6. Middleware validates token and extracts wallet address automatically

## Tech Stack

- **FastAPI** — async API framework
- **Pydantic** — schema validation + structured AI outputs
- **SIWE** — Sign-In with Ethereum (wallet-based auth)
- **PyJWT** — JSON Web Token session management
- **Web3.py** — on-chain data (balances, tx counts, account types)
- **Anthropic SDK** — Claude AI for structured analysis
- **Alchemy** — Ethereum mainnet RPC provider

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/health` | No | Health check |
| `GET` | `/auth/nonce` | No | Get a signing nonce |
| `POST` | `/auth/verify` | No | Verify SIWE signature, get JWT |
| `POST` | `/agent/analyze` | JWT | AI-powered token/crypto analysis |
| `GET` | `/agent/wallet` | JWT | On-chain wallet summary |

## Structured Outputs

The AI agent doesn't return freeform text. Every response is validated against Pydantic models:

```json
{
  "token": "ETH",
  "price_usd": 3245.50,
  "market_cap": 390000000000,
  "risk_score": 4,
  "summary": "Strong fundamentals with upcoming network upgrades..."
}
```

If the LLM hallucinates or returns malformed data, Pydantic catches it before it reaches the client.

## Setup

```bash
# Clone
git clone https://github.com/Naakugod11/web3-ai-agent.git
cd web3-ai-agent

# Virtual environment
python3 -m venv venv
source venv/bin/activate

# Dependencies
pip install -r requirements.txt

# Environment
cp .env.example .env
# Edit .env with your keys:
#   ANTHROPIC_API_KEY — from console.anthropic.com
#   RPC_URL — from alchemy.com (Ethereum Mainnet)
#   JWT_SECRET — run: python3 -c "import secrets; print(secrets.token_hex(32))"

# Run
uvicorn api.main:app --reload

# Tests
python -m pytest tests/ -v -p no:pytest_ethereum
```

## Tests

```
tests/test_auth.py      — nonce generation, uniqueness
tests/test_jwt.py       — token creation, verification, rejection
tests/test_middleware.py — address validation, checksum conversion
```

All 7 tests passing.

## Project Structure

```
web3-ai-agent/
├── api/
│   ├── main.py            # FastAPI app + router registration
│   ├── routes.py          # Auth endpoints (nonce, verify)
│   └── agent_routes.py    # Agent endpoints (analyze, wallet)
├── core/
│   ├── config.py          # Settings + env loader
│   ├── models.py          # Pydantic schemas
│   ├── middleware.py       # JWT auth + address validation
│   └── exceptions.py      # Error handling
├── services/
│   ├── auth.py            # SIWE nonce + verification
│   ├── jwt.py             # Token creation + validation
│   ├── agent.py           # AI agent with structured outputs
│   └── chain.py           # On-chain data via Web3.py
├── tests/
├── .env.example
├── requirements.txt
└── README.md
```

## Roadmap

This project is Phase 1 of a larger Web3 + AI development track.

**This repo:**
- [x] Rate limiting per wallet
- [x] Redis for nonce + session storage
- [x] Frontend demo with wallet connect
- [x] Docker deployment

**Upcoming projects:**
- Phase 2 — RAG system for crypto knowledge (separate repo)
- Phase 3 — Autonomous agent with tool use (separate repo)
- Phase 4 — Multi-agent trading bot combining all phases (separate repo)
- Phase 5 — ZK proof integration with Noir/Circom (separate repo)

## Built by

[@naaku_builds](https://x.com/naaku_builds)