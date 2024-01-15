"""
hooks.regions
This module defines functions to add link relations to regions.
"""
import logging
import json
from flask import current_app
from hypermea.core.logging import trace
from configuration import SETTINGS
from hypermea.core.utils import get_resource_id, get_id_field, get_my_base_url
from hypermea.core.gateway import get_href_from_gateway
import affordances

LOG = logging.getLogger('hooks.regions')


@trace
def add_hooks(app):
    """Wire up the hooks for regions."""
    app.on_fetched_item_regions += _add_links_to_region
    app.on_fetched_resource_regions += _add_links_to_regions_collection
    app.on_post_POST_regions += _post_regions


@trace
def _post_regions(request, payload):
    if payload.status_code == 201:
        j = json.loads(payload.data)
        if '_items' in j:
            for region in j['_items']:
                _add_links_to_region(region)
        else:
            _add_links_to_region(j)
        payload.data = json.dumps(j)


@trace
def _add_links_to_regions_collection(regions_collection):
    for region in regions_collection['_items']:
        _add_links_to_region(region)
        
    if '_links' in regions_collection:
        base_url = get_my_base_url()

        id_field = get_id_field('regions')
        if id_field.startswith('_'):
            id_field = id_field[1:]        
                
        regions_collection['_links']['item'] = {
            'href': f'{base_url}/regions/{{{id_field}}}',
            'title': 'region',
            'templated': True
        }
        self_href = regions_collection['_links']['self']['href']
        affordances.rfc6861.create_form.add_link(regions_collection, 'regions', self_href)                


@trace
def _add_links_to_region(region):
    base_url = get_my_base_url()
    region_id = get_resource_id(region, 'regions')

    _add_remote_children_links(region)
    _add_remote_parent_links(region)

    region['_links']['self'] = {
        'href': f"{base_url}/regions/{region_id}",
        'title': 'region'
    }
    affordances.rfc6861.edit_form.add_link(region, 'regions')
    region['_links']['brands'] = {
        'href': f'{base_url}/regions/{region_id}/brands',
        'title': 'brands'
    }
    region['_links']['notifications'] = {
        'href': f'{base_url}/regions/{region_id}/notifications',
        'title': 'notifications'
    }
    region['_links']['catalogs'] = {
        'href': f'{base_url}/regions/{region_id}/catalogs',
        'title': 'catalogs'
    }
    

    
@trace
def _add_remote_children_links(region):
    if not SETTINGS['HY_GATEWAY_URL']:
        return
    region_id = get_resource_id(region, 'regions')

    # == do not edit this method above this line ==    

    
@trace
def _add_remote_parent_links(region):
    if not SETTINGS['HY_GATEWAY_URL']:
        return
    region_id = get_resource_id(region, 'regions')

    # == do not edit this method above this line ==    
