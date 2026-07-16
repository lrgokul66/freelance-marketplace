"""
Auth token service — generates and validates signed tokens for
password reset and email verification using itsdangerous.
"""
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask import current_app


def generate_token(data, salt='general'):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return s.dumps(data, salt=salt)


def verify_token(token, salt='general', max_age=3600):
    """
    Verify a token.
    Returns the serialized data or None if invalid/expired.
    """
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token, salt=salt, max_age=max_age)
        return data
    except (SignatureExpired, BadSignature):
        return None
