"""
Defines the resources that comprise the registrations-service domain.
"""
from . import _settings
from ._common import OBJECT_ID_REGEX
from . import registrations


DOMAIN_DEFINITIONS = {
    '_settings': _settings.DEFINITION,
    'registrations': registrations.DEFINITION
}


DOMAIN_RELATIONS = {
    'events_registrations': {
        'schema': registrations.SCHEMA,
        'url': f'registrations/event/<regex("{OBJECT_ID_REGEX}"):_event_ref>',
        'resource_title': 'registrations',
        'datasource': {'source': 'registrations'}
    },
    'accounts_registrations': {
        'schema': registrations.SCHEMA,
        'url': f'registrations/account/<regex("{OBJECT_ID_REGEX}"):_account_ref>',
        'resource_title': 'registrations',
        'datasource': {'source': 'registrations'}
    }
}


DOMAIN = {**DOMAIN_DEFINITIONS, **DOMAIN_RELATIONS}
