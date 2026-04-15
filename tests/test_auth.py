from services.auth import generate_nonce, nonce_store

def test_generate_nonce():
    nonce = generate_nonce()
    assert len(nonce) == 32
    assert nonce in nonce_store

def test_nonce_is_unique():
    nonce1 = generate_nonce()
    nonce2 = generate_nonce()
    assert nonce1 != nonce2

