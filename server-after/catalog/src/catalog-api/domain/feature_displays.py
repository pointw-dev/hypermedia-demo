"""
Defines the feature_displays resource.
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
    '_family_ref': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'families',
            'embeddable': True
        }
    },
    '_catalog_ref': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'catalogs',
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
