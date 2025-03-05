"""
Defines the resources that comprise the events-service domain.
"""
from . import _settings
from ._common import OBJECT_ID_REGEX
from . import events


DOMAIN_DEFINITIONS = {
    '_settings': _settings.DEFINITION,
    'events': events.DEFINITION
}


DOMAIN_RELATIONS = {
    'venues_events': {
        'schema': events.SCHEMA,
        'url': f'events/venue/<regex("{OBJECT_ID_REGEX}"):_venue_ref>',
        'resource_title': 'events',
        'datasource': {'source': 'events'}
    }
}


DOMAIN = {**DOMAIN_DEFINITIONS, **DOMAIN_RELATIONS}
