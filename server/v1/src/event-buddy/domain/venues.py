"""
Defines the venues resource.
"""
from domain._common import COMMON_FIELDS


SCHEMA = {
    'name': {
        'type': 'string',
        'required': True,
        'empty': False,
        'unique': True
    },
    'description': {
        'type': 'string'
    },
    'capacity': {
        'type': 'integer'
    }
}

SCHEMA.update(COMMON_FIELDS)

DEFINITION = {
    'schema': SCHEMA,
    'public_methods': ['GET'],
    'public_item_methods': ['GET'],
    ''
    'datasource': {
        'projection': {'_tenant': 0}
    },
    'additional_lookup': {
        'url': r'regex("[\w]+")',
        'field': 'name'
    }
}
