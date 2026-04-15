from web3 import Web3

def test_valid_address():
    address = "0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18"
    assert Web3.is_address(address)

def test_invalid_address():
    assert not Web3.is_address("not-an-address")

def test_checksum_conversion():
    address = "0x742d35cc6634c0532925a3b844bc9e7595f2bd18"
    checksum = Web3.to_checksum_address(address)
    assert Web3.is_checksum_address(checksum)