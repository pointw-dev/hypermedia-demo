"""
Defines the registrations resource.
"""
from domain._common import COMMON_FIELDS


SCHEMA = {
    '_event_ref': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'events',
            'embeddable': True
        }
    },
    '_account_ref': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'accounts',
            'embeddable': True
        }
    }
}

SCHEMA.update(COMMON_FIELDS)

DEFINITION = {
    'schema': SCHEMA,
    'datasource': {
        'projection': {'_tenant': 0}
    }
}
