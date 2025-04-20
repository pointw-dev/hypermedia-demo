"""
The auth module used for HY.
"""
from bson.objectid import ObjectId
from hypermea_negotiable_auth import NegotiableAuth, auth_parser

from hypermea.core.utils import get_db
from .auth_handlers import basic

import settings

auth_parser.add_handler('Basic', basic, realm=f'{settings.auth.realm}')


class HypermeaAuthorization(NegotiableAuth):
    def __init__(self):
        super(HypermeaAuthorization, self).__init__()
        self.account = None

    def authorized(self, allowed_roles, resource, method):
        get_home_allowed = settings.auth.allow_get_home or not settings.hypermea.gateway_url
        if get_home_allowed and method == 'GET' and resource is None:
            return True

        return super().authorized(allowed_roles, resource, method)

    def process_claims(self, claims, allowed_roles, resource, method):
        authorized = "user" in claims and "permissions" in claims
        if not authorized:
            return False

        if method == 'HEAD':
            return True

        is_admin = claims.get('role') == 'admin'

        if is_admin:
            self.account = {'username': 'root', 'role': 'admin'}
        else:
            auth_value = 'all-denied'
            accounts = get_db()['accounts']
            account = accounts.find_one({'user_id': claims['user']})
            if account:
                self.account = account
                auth_value = account['username']
                claims['role'] = account['role']
                if allowed_roles:
                    authorized = claims['role'] in allowed_roles
            else:
                authorized = False

            self.set_request_auth_value(auth_value)

        # if resource in ['accounts', 'roles'] and not is_admin:
        #     authorized = False

        # NOTE: To set the tenant value, pass it to self.set_request_auth_value(), for example:
        # tenent_field = 'replace this with the name of the field'
        # tenent = claims[tenent_field].upper() if tenent_field in claims else 'unknown'
        # self.set_request_auth_value(tenent)

        return authorized
