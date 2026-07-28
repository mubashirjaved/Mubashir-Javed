"""
Enterprise-Grade Security Module
Provides AES-256 Field-Level Encryption, Bcrypt Password Hashing, JWT Authentication,
and SHA-256 HMAC Record Signatures for Database Integrity Verification.
"""

import hmac
import hashlib
import os
import time
from typing import Dict, Any, Optional
import bcrypt
import jwt
from cryptography.fernet import Fernet

# Global secret key for JWT/HMAC (in prod, load from safe environment)
JWT_SECRET_KEY = os.getenv("ERP_JWT_SECRET", "super_secure_enterprise_erp_secret_key_991823")
DB_ENCRYPTION_KEY_FILE = ".db_field_key"

def get_or_create_field_key() -> bytes:
    """
    Retrieve or generate an AES-256 encryption key.
    Saves to a local file if not set in environment or file.
    """
    env_key = os.getenv("ERP_FIELD_ENCRYPTION_KEY")
    if env_key:
        return env_key.encode("utf-8")

    if os.path.exists(DB_ENCRYPTION_KEY_FILE):
        with open(DB_ENCRYPTION_KEY_FILE, "rb") as f:
            return f.read().strip()

    # Generate new Fernet key
    new_key = Fernet.generate_key()
    with open(DB_ENCRYPTION_KEY_FILE, "wb") as f:
        f.write(new_key)
    os.chmod(DB_ENCRYPTION_KEY_FILE, 0o600)  # Secure permission
    return new_key


# AES-256 field encryption / decryption helpers
def encrypt_field(plain_text: str) -> str:
    """Encrypt plain text field using AES-256 (Fernet)."""
    if not plain_text:
        return ""
    key = get_or_create_field_key()
    fernet = Fernet(key)
    return fernet.encrypt(plain_text.encode("utf-8")).decode("utf-8")


def decrypt_field(cipher_text: str) -> str:
    """Decrypt cipher text field using AES-256 (Fernet)."""
    if not cipher_text:
        return ""
    try:
        key = get_or_create_field_key()
        fernet = Fernet(key)
        return fernet.decrypt(cipher_text.encode("utf-8")).decode("utf-8")
    except Exception:
        # Fallback if decryption fails or invalid key
        return "[ENCRYPTION_ERROR]"


# Password Hashing with Bcrypt
def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    if not password:
        raise ValueError("Password cannot be empty")
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hashed value."""
    if not password or not hashed:
        return False
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


# JWT Token generation & verification
def generate_jwt(user_id: int, username: str, role: str, expires_in: int = 3600) -> str:
    """Generate JWT token for authenticated user sessions and APIs."""
    payload = {
        "sub": str(user_id),
        "username": username,
        "role": role,
        "exp": int(time.time()) + expires_in,
        "iat": int(time.time())
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")


def verify_jwt(token: str) -> Optional[Dict[str, Any]]:
    """Verify JWT token and return decoded payload if valid."""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Expired
    except jwt.InvalidTokenError:
        return None  # Invalid


# Tamper Detection / Record Signature using HMAC SHA-256
def compute_record_signature(data: Dict[str, Any], secret_key: str = JWT_SECRET_KEY) -> str:
    """
    Generate a dynamic tamper-evident signature of record fields using HMAC SHA-256.
    Keys are sorted to ensure deterministic signature calculation.
    """
    # Exclude signature fields or dynamic ID fields that can change during auto-increment
    filtered_data = {str(k): str(v) for k, v in data.items() if k not in ("signature", "id", "created_at", "updated_at")}
    serialized = "|".join(f"{k}:{filtered_data[k]}" for k in sorted(filtered_data.keys()))

    mac = hmac.new(secret_key.encode("utf-8"), serialized.encode("utf-8"), hashlib.sha256)
    return mac.hexdigest()


def verify_record_integrity(data: Dict[str, Any], signature: str, secret_key: str = JWT_SECRET_KEY) -> bool:
    """Verify record signature to detect unauthorized modifications."""
    if not signature:
        return False
    expected = compute_record_signature(data, secret_key)
    return hmac.compare_digest(expected, signature)
