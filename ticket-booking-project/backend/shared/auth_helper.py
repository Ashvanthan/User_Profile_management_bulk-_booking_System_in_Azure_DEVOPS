'''import os, jwt, bcrypt
from datetime import datetime, timedelta

JWT_SECRET = os.environ.get("JWT_SECRET", "your-secret-key-change-in-prod")
JWT_EXPIRY_HOURS = 24

def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())

def create_token(user_id: str, email: str, role: str) -> str:
    payload = {
        "sub": user_id,
        "email": email,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRY_HOURS)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def decode_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])

def get_token_from_request(req) -> dict:
    auth = req.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header")
    token = auth.split(" ", 1)[1]
    return decode_token(token)

def require_role(req, allowed_roles: list) -> dict:
    claims = get_token_from_request(req)
    if claims.get("role") not in allowed_roles:
        raise PermissionError(f"Role '{claims.get('role')}' not allowed")
    return claims'''



'''import os, jwt, bcrypt
from datetime import datetime, timedelta

JWT_SECRET = os.environ.get("JWT_SECRET", "ashvanthan-project-secret-key-240701056")
JWT_EXPIRY_HOURS = 24

def hash_password(plain: str) -> str:
    # Explicitly encoding to utf-8 before hashing
    return bcrypt.hashpw(plain.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain: str, hashed: str) -> bool:
    try:
        # CRITICAL FIX: Ensure both plain and hashed are encoded to bytes for the check
        return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))
    except Exception as e:
        print(f"[AUTH ERROR] Password verification failed: {e}")
        return False

def create_token(user_id: str, email: str, role: str) -> str:
    payload = {
        "sub": user_id,
        "email": email,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRY_HOURS)
    }
    # Some PyJWT versions return bytes, some return strings. We ensure it's a string.
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return token.decode('utf-8') if isinstance(token, bytes) else token

def decode_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])

def get_token_from_request(req) -> dict:
    auth = req.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header")
    token = auth.split(" ", 1)[1]
    return decode_token(token)

def require_role(req, allowed_roles: list) -> dict:
    claims = get_token_from_request(req)
    if claims.get("role") not in allowed_roles:
        raise PermissionError(f"Role '{claims.get('role')}' not allowed")
    return claims'''


import os, jwt
from datetime import datetime, timedelta

JWT_SECRET = os.environ.get("JWT_SECRET", "ashvanthan-project-secret-key-240701056")
JWT_EXPIRY_HOURS = 24

def hash_password(plain: str) -> str:
    # No hashing, just return the plain string
    return plain

def verify_password(plain: str, stored: str) -> bool:
    # Direct string comparison
    return plain == stored

def create_token(user_id: str, email: str, role: str) -> str:
    payload = {
        "sub": user_id,
        "email": email,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRY_HOURS)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    # Handle both string and bytes return types
    return token.decode('utf-8') if isinstance(token, bytes) else token

def decode_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])

def get_token_from_request(req) -> dict:
    auth = req.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header")
    token = auth.split(" ", 1)[1]
    return decode_token(token)

def require_role(req, allowed_roles: list) -> dict:
    claims = get_token_from_request(req)
    if claims.get("role") not in allowed_roles:
        raise PermissionError(f"Role '{claims.get('role')}' not allowed")
    return claims
