import pytest
from services.jwt import create_token, verify_token

def test_create_and_verify_token():
    address = "0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18"
    token = create_token(address)
    result = verify_token(token)
    assert result == address

def test_invalid_token():
    with pytest.raises(Exception):
        verify_token("garbage.token.here")