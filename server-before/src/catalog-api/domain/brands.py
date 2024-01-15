"""
Defines the brands resource.
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
    '_region_ref': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'regions',
            'embeddable': True
        }
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
        'field': 'name'
    }
}
