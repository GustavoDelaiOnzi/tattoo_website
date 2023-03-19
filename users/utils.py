import jwt
from datetime import datetime, timedelta
from django.conf import settings


def generate_access_token(username):
    """
    Generates an access token for the given user.
    """
    payload = {
        'username': username,
        'exp': datetime.utcnow() + timedelta(minutes=15)
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')


def generate_refresh_token(username):
    """
    Generates a refresh token for the given user.
    """
    payload = {
        'username': username,
        'exp': datetime.utcnow() + timedelta(days=30)
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')


def decode_token(token):
    """
    Decodes the given token and returns the username.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload['username']
    except jwt.exceptions.DecodeError:
        raise Exception('Invalid token')


def validate_token(token, username):
    """
    Validates the given token and checks if it belongs to the given user.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        if payload['username'] != username:
            raise Exception('Invalid token')
    except jwt.exceptions.ExpiredSignatureError:
        raise Exception('Token has expired')
    except jwt.exceptions.InvalidSignatureError:
        raise Exception('Invalid token signature')
    except jwt.exceptions.DecodeError:
        raise Exception('Invalid token')
