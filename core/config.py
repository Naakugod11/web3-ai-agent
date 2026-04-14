from pydantic_settings import BaseSettings

class Settings(BaseSettings)
    anthropic_api_key: str = ""
    rpc_url: str = "https://eth-mainnet.g.alchemy.com/v2/demo"
    env: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()