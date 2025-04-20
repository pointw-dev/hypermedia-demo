import jwt
from base64 import b64decode
import settings


def basic(token, **kwargs):
    try:
        username, password = b64decode(token).decode().split(':', 1)
        is_root = False
        if username.lower() == 'root':
            if password == settings.auth.root_password.get_secret_value():
                is_root = True
            else:
                return {}

        rtn = {
            'user': username,
            'role': 'admin' if is_root else '',
            'permissions': []
        }
    except:
        rtn = {}

    return rtn
