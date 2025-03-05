"""
Defines the resources that comprise the venues-service domain.
"""
from . import _settings
from ._common import OBJECT_ID_REGEX
from . import venues


DOMAIN_DEFINITIONS = {
    '_settings': _settings.DEFINITION,
    'venues': venues.DEFINITION
}


DOMAIN_RELATIONS = {
}


DOMAIN = {**DOMAIN_DEFINITIONS, **DOMAIN_RELATIONS}
