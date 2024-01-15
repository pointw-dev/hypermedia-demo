"""
Defines the resources that comprise the catalog-api domain.
"""
from . import _settings
from ._common import OBJECT_ID_REGEX
from . import brands
from . import catalogs
from . import families
from . import feature_displays


DOMAIN_DEFINITIONS = {
    '_settings': _settings.DEFINITION,
    'brands': brands.DEFINITION,
    'catalogs': catalogs.DEFINITION,
    'families': families.DEFINITION,
    'feature_displays': feature_displays.DEFINITION
}


DOMAIN_RELATIONS = {
    'regions_brands': {
        'schema': brands.SCHEMA,
        'url': f'brands/region/<regex("{OBJECT_ID_REGEX}"):_region_ref>',
        'resource_title': 'brands',
        'datasource': {'source': 'brands'}
    },
    'regions_catalogs': {
        'schema': catalogs.SCHEMA,
        'url': f'catalogs/region/<regex("{OBJECT_ID_REGEX}"):_region_ref>',
        'resource_title': 'catalogs',
        'datasource': {'source': 'catalogs'}
    },
    'brands_families': {
        'schema': families.SCHEMA,
        'url': f'brands/<regex("{OBJECT_ID_REGEX}"):_brand_ref>/families',
        'resource_title': 'families',
        'datasource': {'source': 'families'}
    },
    'catalogs_families': {
        'schema': families.SCHEMA,
        'url': f'catalogs/<regex("{OBJECT_ID_REGEX}"):_catalog_ref>/families',
        'resource_title': 'families',
        'datasource': {'source': 'families'}
    },
    'families_feature_displays': {
        'schema': feature_displays.SCHEMA,
        'url': f'families/<regex("{OBJECT_ID_REGEX}"):_family_ref>/feature_displays',
        'resource_title': 'feature_displays',
        'datasource': {'source': 'feature_displays'}
    },
    'catalogs_feature_displays': {
        'schema': feature_displays.SCHEMA,
        'url': f'catalogs/<regex("{OBJECT_ID_REGEX}"):_catalog_ref>/feature_displays',
        'resource_title': 'feature_displays',
        'datasource': {'source': 'feature_displays'}
    }
}


DOMAIN = {**DOMAIN_DEFINITIONS, **DOMAIN_RELATIONS}
