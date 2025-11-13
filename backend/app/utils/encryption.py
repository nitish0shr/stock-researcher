import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Generate or load encryption key
ENCRYPTION_PASSWORD = os.getenv("ENCRYPTION_PASSWORD", "default-password-change-in-production")

password = ENCRYPTION_PASSWORD.encode()
salt = b'stock_research_salt'  # In production, use a proper salt
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
)
key = base64.urlsafe_b64encode(kdf.derive(password))
f = Fernet(key)

def encrypt_key(plain_key: str) -> str:
    """Encrypt an API key"""
    return f.encrypt(plain_key.encode()).decode()

def decrypt_key(encrypted_key: str) -> str:
    """Decrypt an API key"""
    return f.decrypt(encrypted_key.encode()).decode()

def mask_key(key: str) -> str:
    """Mask an API key for display"""
    if len(key) > 8:
        return f"{key[:4]}...{key[-4:]}"
    return "***"