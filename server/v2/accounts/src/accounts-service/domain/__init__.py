"""
Defines the resources that comprise the accounts-service domain.
"""
from . import _settings
from ._common import OBJECT_ID_REGEX
from . import accounts


DOMAIN_DEFINITIONS = {
    '_settings': _settings.DEFINITION,
    'accounts': accounts.DEFINITION
}


DOMAIN_RELATIONS = {
}


DOMAIN = {**DOMAIN_DEFINITIONS, **DOMAIN_RELATIONS}
