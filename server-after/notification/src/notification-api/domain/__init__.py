"""
Defines the resources that comprise the notification-api domain.
"""
from . import _settings
from ._common import OBJECT_ID_REGEX
from . import notifications


DOMAIN_DEFINITIONS = {
    '_settings': _settings.DEFINITION,
    'notifications': notifications.DEFINITION
}


DOMAIN_RELATIONS = {
    'regions_notifications': {
        'schema': notifications.SCHEMA,
        'url': f'notifications/region/<regex("{OBJECT_ID_REGEX}"):_region_ref>',
        'resource_title': 'notifications',
        'datasource': {'source': 'notifications'}
    }
}


DOMAIN = {**DOMAIN_DEFINITIONS, **DOMAIN_RELATIONS}
