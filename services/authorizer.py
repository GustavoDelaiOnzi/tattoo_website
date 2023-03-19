import jwt
from datetime import datetime, timedelta
from django.conf import settings


class AuthorizationService:
    def __init__(self):
        self.secret_key = settings.SECRET_KEY

    def generate_access_token(self, username):
        payload = {
            'username': username,
            'exp': datetime.utcnow() + timedelta(minutes=15)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256').decode('utf-8')

    def generate_refresh_token(self, username):
        payload = {
            'username': username,
            'exp': datetime.utcnow() + timedelta(days=30)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256').decode('utf-8')

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload['username']
        except jwt.exceptions.DecodeError:
            raise Exception('Invalid token')

    def validate_token(self, token, username):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            if payload['username'] != username:
                raise Exception('Invalid token')
        except jwt.exceptions.ExpiredSignatureError:
            raise Exception('Token has expired')
        except jwt.exceptions.InvalidSignatureError:
            raise Exception('Invalid token signature')
        except jwt.exceptions.DecodeError:
            raise Exception('Invalid token')
