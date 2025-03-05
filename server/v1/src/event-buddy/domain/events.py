"""
Defines the events resource.
"""
from ._common import COMMON_FIELDS


SCHEMA = {
    'name': {
        'type': 'string',
        'required': True,
        'empty': False,
        'unique': False
    },
    'description': {
        'type': 'string'
    },
    'date': {
        'type': 'iso_date',
        'required': True
    },
    'time': {
        'type': 'iso_time',
        'required': True
    },
    'duration': {
        'type': 'iso_duration',
        'required': True
    },
    '_venue_ref': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'venues',
            'embeddable': True
        }
    }
}

SCHEMA.update(COMMON_FIELDS)

DEFINITION = {
    'schema': SCHEMA,
    'public_methods': ['GET', 'POST'],
    'public_item_methods': ['GET', 'PATCH'],
    'datasource': {
        'projection': {'_tenant': 0}
    }
}
