"""
hooks.catalogs
This module defines functions to add link relations to catalogs.
"""
import logging
import json
from flask import current_app
from hypermea.core.logging import trace
from configuration import SETTINGS
from hypermea.core.utils import get_resource_id, get_id_field, get_my_base_url
from hypermea.core.gateway import get_href_from_gateway
import affordances

LOG = logging.getLogger('hooks.catalogs')


@trace
def add_hooks(app):
    """Wire up the hooks for catalogs."""
    app.on_fetched_item_catalogs += _add_links_to_catalog
    app.on_fetched_resource_catalogs += _add_links_to_catalogs_collection
    app.on_post_POST_catalogs += _post_catalogs


@trace
def _post_catalogs(request, payload):
    if payload.status_code == 201:
        j = json.loads(payload.data)
        if '_items' in j:
            for catalog in j['_items']:
                _add_links_to_catalog(catalog)
        else:
            _add_links_to_catalog(j)
        payload.data = json.dumps(j)


@trace
def _add_links_to_catalogs_collection(catalogs_collection):
    for catalog in catalogs_collection['_items']:
        _add_links_to_catalog(catalog)
        
    if '_links' in catalogs_collection:
        base_url = get_my_base_url()

        id_field = get_id_field('catalogs')
        if id_field.startswith('_'):
            id_field = id_field[1:]        
                
        catalogs_collection['_links']['item'] = {
            'href': f'{base_url}/catalogs/{{{id_field}}}',
            'title': 'catalog',
            'templated': True
        }
        self_href = catalogs_collection['_links']['self']['href']
        affordances.rfc6861.create_form.add_link(catalogs_collection, 'catalogs', self_href)                


@trace
def _add_links_to_catalog(catalog):
    base_url = get_my_base_url()
    catalog_id = get_resource_id(catalog, 'catalogs')

    _add_remote_children_links(catalog)
    _add_remote_parent_links(catalog)

    catalog['_links']['self'] = {
        'href': f"{base_url}/catalogs/{catalog_id}",
        'title': 'catalog'
    }
    affordances.rfc6861.edit_form.add_link(catalog, 'catalogs')
    catalog['_links']['families'] = {
        'href': f'{base_url}/catalogs/{catalog_id}/families',
        'title': 'families'
    }
    catalog['_links']['feature_displays'] = {
        'href': f'{base_url}/catalogs/{catalog_id}/feature_displays',
        'title': 'feature_displays'
    }
    

    
@trace
def _add_remote_children_links(catalog):
    if not SETTINGS['HY_GATEWAY_URL']:
        return
    catalog_id = get_resource_id(catalog, 'catalogs')

    # == do not edit this method above this line ==    

    
@trace
def _add_remote_parent_links(catalog):
    if not SETTINGS['HY_GATEWAY_URL']:
        return
    catalog_id = get_resource_id(catalog, 'catalogs')
    if '_region_ref' in catalog:
        catalog['_links']['regions'] = {
            'href': f"{get_href_from_gateway('regions')}/{catalog['_region_ref']}",
            'title': 'region_catalogs'
        }

    # == do not edit this method above this line ==    
