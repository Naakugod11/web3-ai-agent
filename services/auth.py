import secrets
from siwe import SiweMessage

nonce_store: dict[str, bool] = {}


def generate_nonce() -> str:
    nonce = secrets.token_hex(16)
    nonce_store[nonce] = True
    return nonce


def verify_siwe_message(message: str, signature: str) -> str:
    """Verify a SIWE message and return the wallet address."""
    siwe_message = SiweMessage.from_message(message)

    if siwe_message.nonce not in nonce_store:
        raise ValueError("Invalid nonce")

    siwe_message.verify(signature)

    del nonce_store[siwe_message.nonce]

    return siwe_message.address