"""
hooks.families
This module defines functions to add link relations to families.
"""
import logging
import json
from flask import current_app
from hypermea.core.logging import trace
from configuration import SETTINGS
from hypermea.core.utils import get_resource_id, get_id_field, get_my_base_url
from hypermea.core.gateway import get_href_from_gateway
import affordances

LOG = logging.getLogger('hooks.families')


@trace
def add_hooks(app):
    """Wire up the hooks for families."""
    app.on_fetched_item_families += _add_links_to_family
    app.on_fetched_resource_families += _add_links_to_families_collection
    app.on_post_POST_families += _post_families

    app.on_fetched_item_brands_families += _add_links_to_family
    app.on_fetched_resource_brands_families += _add_links_to_families_collection
    app.on_post_POST_brands_families += _post_families

    app.on_fetched_item_catalogs_families += _add_links_to_family
    app.on_fetched_resource_catalogs_families += _add_links_to_families_collection
    app.on_post_POST_catalogs_families += _post_families


@trace
def _post_families(request, payload):
    if payload.status_code == 201:
        j = json.loads(payload.data)
        if '_items' in j:
            for family in j['_items']:
                _add_links_to_family(family)
        else:
            _add_links_to_family(j)
        payload.data = json.dumps(j)


@trace
def _add_links_to_families_collection(families_collection):
    for family in families_collection['_items']:
        _add_links_to_family(family)
        
    if '_links' in families_collection:
        base_url = get_my_base_url()

        id_field = get_id_field('families')
        if id_field.startswith('_'):
            id_field = id_field[1:]        
                
        families_collection['_links']['item'] = {
            'href': f'{base_url}/families/{{{id_field}}}',
            'title': 'family',
            'templated': True
        }
        self_href = families_collection['_links']['self']['href']
        affordances.rfc6861.create_form.add_link(families_collection, 'families', self_href)                


@trace
def _add_links_to_family(family):
    base_url = get_my_base_url()
    family_id = get_resource_id(family, 'families')

    _add_remote_children_links(family)
    _add_remote_parent_links(family)

    family['_links']['self'] = {
        'href': f"{base_url}/families/{family_id}",
        'title': 'family'
    }
    affordances.rfc6861.edit_form.add_link(family, 'families')
    if family.get('_brand_ref'):
        family['_links']['parent'] = {
            'href': f'{base_url}/brands/{family["_brand_ref"]}',
            'title': 'brands'
        }
        family['_links']['collection'] = {
            'href': f'{base_url}/brands/{family["_brand_ref"]}/families',
            'title': 'brand_families'
        }
    else:
        family['_links']['parent'] = {
            'href': f'{base_url}/',
            'title': 'home'
        }
        family['_links']['collection'] = {
            'href': f'{base_url}/families',
            'title': 'families'
        }
    if family.get('_catalog_ref'):
        family['_links']['parent'] = {
            'href': f'{base_url}/catalogs/{family["_catalog_ref"]}',
            'title': 'catalogs'
        }
        family['_links']['collection'] = {
            'href': f'{base_url}/catalogs/{family["_catalog_ref"]}/families',
            'title': 'catalog_families'
        }
    else:
        family['_links']['parent'] = {
            'href': f'{base_url}/',
            'title': 'home'
        }
        family['_links']['collection'] = {
            'href': f'{base_url}/families',
            'title': 'families'
        }
    family['_links']['feature_displays'] = {
        'href': f'{base_url}/families/{family_id}/feature_displays',
        'title': 'feature_displays'
    }
    

    
@trace
def _add_remote_children_links(family):
    if not SETTINGS['HY_GATEWAY_URL']:
        return
    family_id = get_resource_id(family, 'families')

    # == do not edit this method above this line ==    

    
@trace
def _add_remote_parent_links(family):
    if not SETTINGS['HY_GATEWAY_URL']:
        return
    family_id = get_resource_id(family, 'families')

    # == do not edit this method above this line ==    
