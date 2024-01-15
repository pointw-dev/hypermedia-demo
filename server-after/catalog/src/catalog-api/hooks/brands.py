"""
hooks.brands
This module defines functions to add link relations to brands.
"""
import logging
import json
from flask import current_app
from hypermea.core.logging import trace
from configuration import SETTINGS
from hypermea.core.utils import get_resource_id, get_id_field, get_my_base_url
from hypermea.core.gateway import get_href_from_gateway
import affordances

LOG = logging.getLogger('hooks.brands')


@trace
def add_hooks(app):
    """Wire up the hooks for brands."""
    app.on_fetched_item_brands += _add_links_to_brand
    app.on_fetched_resource_brands += _add_links_to_brands_collection
    app.on_post_POST_brands += _post_brands


@trace
def _post_brands(request, payload):
    if payload.status_code == 201:
        j = json.loads(payload.data)
        if '_items' in j:
            for brand in j['_items']:
                _add_links_to_brand(brand)
        else:
            _add_links_to_brand(j)
        payload.data = json.dumps(j)


@trace
def _add_links_to_brands_collection(brands_collection):
    for brand in brands_collection['_items']:
        _add_links_to_brand(brand)
        
    if '_links' in brands_collection:
        base_url = get_my_base_url()

        id_field = get_id_field('brands')
        if id_field.startswith('_'):
            id_field = id_field[1:]        
                
        brands_collection['_links']['item'] = {
            'href': f'{base_url}/brands/{{{id_field}}}',
            'title': 'brand',
            'templated': True
        }
        self_href = brands_collection['_links']['self']['href']
        affordances.rfc6861.create_form.add_link(brands_collection, 'brands', self_href)                


@trace
def _add_links_to_brand(brand):
    base_url = get_my_base_url()
    brand_id = get_resource_id(brand, 'brands')

    _add_remote_children_links(brand)
    _add_remote_parent_links(brand)

    brand['_links']['self'] = {
        'href': f"{base_url}/brands/{brand_id}",
        'title': 'brand'
    }
    affordances.rfc6861.edit_form.add_link(brand, 'brands')
    brand['_links']['families'] = {
        'href': f'{base_url}/brands/{brand_id}/families',
        'title': 'families'
    }
    

    
@trace
def _add_remote_children_links(brand):
    if not SETTINGS['HY_GATEWAY_URL']:
        return
    brand_id = get_resource_id(brand, 'brands')

    # == do not edit this method above this line ==    

    
@trace
def _add_remote_parent_links(brand):
    if not SETTINGS['HY_GATEWAY_URL']:
        return
    brand_id = get_resource_id(brand, 'brands')
    if '_region_ref' in brand:
        brand['_links']['regions'] = {
            'href': f"{get_href_from_gateway('regions')}/{brand['_region_ref']}",
            'title': 'region_brands'
        }

    # == do not edit this method above this line ==    
