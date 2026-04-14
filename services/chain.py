from web3 import Web3
from core.config import settings

w3 = Web3(Web3.HTTPProvider(settings.rpc_url))


def get_eth_balance(address: str) -> float:
    """Get ETH balance for a wallet address."""
    checksum = Web3.to_checksum_address(address)
    balance_wei = w3.eth.get_balance(checksum)
    return float(Web3.from_wei(balance_wei, "ether"))


def get_wallet_summary(address: str) -> dict:
    """Get basic wallet info."""
    checksum = Web3.to_checksum_address(address)
    balance = get_eth_balance(address)
    tx_count = w3.eth.get_transaction_count(checksum)

    return {
        "address": address,
        "eth_balance": balance,
        "transaction_count": tx_count,
        "is_contract": w3.eth.get_code(checksum) != b"",
    }
