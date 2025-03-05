"""
Defines the resources that comprise the event-buddy domain.
"""
from . import _settings
from ._common import OBJECT_ID_REGEX
from . import events
from . import venues
from . import registrations
from . import accounts


DOMAIN_DEFINITIONS = {
    '_settings': _settings.DEFINITION,
    'events': events.DEFINITION,
    'venues': venues.DEFINITION,
    'registrations': registrations.DEFINITION,
    'accounts': accounts.DEFINITION
    
}


DOMAIN_RELATIONS = {
    'venues_events': {
        'schema': events.SCHEMA,
        'url': f'venues/<regex("{OBJECT_ID_REGEX}"):_venue_ref>/events',
        'resource_title': 'events',
        'datasource': {'source': 'events'},
        'public_methods': ['GET', 'POST'],
        'public_item_methods': ['GET', 'PATCH']
    },
    'events_registrations': {
        'schema': registrations.SCHEMA,
        'url': f'events/<regex("{OBJECT_ID_REGEX}"):_event_ref>/registrations',
        'resource_title': 'registrations',
        'datasource': {'source': 'registrations'}
    },
    'accounts_registrations': {
        'schema': registrations.SCHEMA,
        'url': f'accounts/<regex("{OBJECT_ID_REGEX}"):_account_ref>/registrations',
        'resource_title': 'registrations',
        'datasource': {'source': 'registrations'}
    }
}


DOMAIN = {**DOMAIN_DEFINITIONS, **DOMAIN_RELATIONS}
