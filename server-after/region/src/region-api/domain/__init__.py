"""
Defines the resources that comprise the region-api domain.
"""
from . import _settings
from ._common import OBJECT_ID_REGEX
from . import regions


DOMAIN_DEFINITIONS = {
    '_settings': _settings.DEFINITION,
    'regions': regions.DEFINITION
}


DOMAIN_RELATIONS = {
}


DOMAIN = {**DOMAIN_DEFINITIONS, **DOMAIN_RELATIONS}
