"""
Defines the registrations resource.
"""
from domain._common import COMMON_FIELDS


SCHEMA = {
    '_event_ref': {
        'type': 'objectid',
        'remote_relation': {
            'rel': 'events',
            'embeddable': True
        }
    },
    '_account_ref': {
        'type': 'objectid',
        'remote_relation': {
            'rel': 'accounts',
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
