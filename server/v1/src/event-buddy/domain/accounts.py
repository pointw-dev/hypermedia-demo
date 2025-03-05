"""
Defines the accounts resource.
"""
from domain._common import COMMON_FIELDS


SCHEMA = {
    'username': {
        'type': 'string',
        'required': True,
        'empty': False,
        'unique': True
    },
    'name': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'role': {
        'type': 'string',
        'required': True,
        'empty': False,
        'allowed': ['member', 'manager', 'hr']
    }
}

SCHEMA.update(COMMON_FIELDS)

DEFINITION = {
    'schema': SCHEMA,
    'datasource': {
        'projection': {'_tenant': 0}
    },
    'additional_lookup': {
        'url': r'regex("[\w]+")',
        'field': 'username'
    },
    'allowed_roles': ['admin', 'manager', 'hr'],
    'allowed_item_roles': ['admin', 'manager', 'hr']
}
