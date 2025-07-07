import base64
import hmac
import hashlib
import json

# Use the public key or anything attacker-controlled as "secret"
with open('/app/utils/public.pem', 'rb') as f:
    SECRET_KEY = f.read().strip()

def b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip('=')

def b64url_decode(data: str) -> bytes:
    padding = '=' * (4 - len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)

def encode_jwt(payload: dict) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    header_b64 = b64url_encode(json.dumps(header).encode())
    payload_b64 = b64url_encode(json.dumps(payload).encode())

    message = f"{header_b64}.{payload_b64}".encode()
    signature = hmac.new(SECRET_KEY, message, hashlib.sha256).digest()
    signature_b64 = b64url_encode(signature)

    return f"{header_b64}.{payload_b64}.{signature_b64}"

def decode_jwt(token: str) -> dict:
    try:
        header_b64, payload_b64, signature_b64 = token.split('.')
        message = f"{header_b64}.{payload_b64}".encode()
        expected_sig = hmac.new(SECRET_KEY, message, hashlib.sha256).digest()
        if hmac.compare_digest(expected_sig, b64url_decode(signature_b64)):
            return json.loads(base64.urlsafe_b64decode(payload_b64 + "==").decode())
    except Exception as e:
        print("[JWT DECODE ERROR]", e)
    return None
