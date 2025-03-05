from base64 import b64decode
from auth import SETTINGS, SIGNING_KEYS


def basic(token, **kwargs):
    try:
        username, password = b64decode(token).decode().split(':', 1)
        is_root = False
        if username.lower() in ['root', 'admin']:
            if password == SETTINGS.get('AUTH_ROOT_PASSWORD'):
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
