"""
hooks.feature_displays
This module defines functions to add link relations to feature_displays.
"""
import logging
import json
from flask import current_app
from hypermea.core.logging import trace
from configuration import SETTINGS
from hypermea.core.utils import get_resource_id, get_id_field, get_my_base_url
from hypermea.core.gateway import get_href_from_gateway
import affordances

LOG = logging.getLogger('hooks.feature_displays')


@trace
def add_hooks(app):
    """Wire up the hooks for feature_displays."""
    app.on_fetched_item_feature_displays += _add_links_to_feature_display
    app.on_fetched_resource_feature_displays += _add_links_to_feature_displays_collection
    app.on_post_POST_feature_displays += _post_feature_displays

    app.on_fetched_item_families_feature_displays += _add_links_to_feature_display
    app.on_fetched_resource_families_feature_displays += _add_links_to_feature_displays_collection
    app.on_post_POST_families_feature_displays += _post_feature_displays

    app.on_fetched_item_catalogs_feature_displays += _add_links_to_feature_display
    app.on_fetched_resource_catalogs_feature_displays += _add_links_to_feature_displays_collection
    app.on_post_POST_catalogs_feature_displays += _post_feature_displays


@trace
def _post_feature_displays(request, payload):
    if payload.status_code == 201:
        j = json.loads(payload.data)
        if '_items' in j:
            for feature_display in j['_items']:
                _add_links_to_feature_display(feature_display)
        else:
            _add_links_to_feature_display(j)
        payload.data = json.dumps(j)


@trace
def _add_links_to_feature_displays_collection(feature_displays_collection):
    for feature_display in feature_displays_collection['_items']:
        _add_links_to_feature_display(feature_display)
        
    if '_links' in feature_displays_collection:
        base_url = get_my_base_url()

        id_field = get_id_field('feature_displays')
        if id_field.startswith('_'):
            id_field = id_field[1:]        
                
        feature_displays_collection['_links']['item'] = {
            'href': f'{base_url}/feature_displays/{{{id_field}}}',
            'title': 'feature_display',
            'templated': True
        }
        self_href = feature_displays_collection['_links']['self']['href']
        affordances.rfc6861.create_form.add_link(feature_displays_collection, 'feature_displays', self_href)                


@trace
def _add_links_to_feature_display(feature_display):
    base_url = get_my_base_url()
    feature_display_id = get_resource_id(feature_display, 'feature_displays')

    _add_remote_children_links(feature_display)
    _add_remote_parent_links(feature_display)

    feature_display['_links']['self'] = {
        'href': f"{base_url}/feature_displays/{feature_display_id}",
        'title': 'feature_display'
    }
    affordances.rfc6861.edit_form.add_link(feature_display, 'feature_displays')
    if feature_display.get('_family_ref'):
        feature_display['_links']['parent'] = {
            'href': f'{base_url}/families/{feature_display["_family_ref"]}',
            'title': 'families'
        }
        feature_display['_links']['collection'] = {
            'href': f'{base_url}/families/{feature_display["_family_ref"]}/feature_displays',
            'title': 'family_feature_displays'
        }
    else:
        feature_display['_links']['parent'] = {
            'href': f'{base_url}/',
            'title': 'home'
        }
        feature_display['_links']['collection'] = {
            'href': f'{base_url}/feature_displays',
            'title': 'feature_displays'
        }
    if feature_display.get('_catalog_ref'):
        feature_display['_links']['parent'] = {
            'href': f'{base_url}/catalogs/{feature_display["_catalog_ref"]}',
            'title': 'catalogs'
        }
        feature_display['_links']['collection'] = {
            'href': f'{base_url}/catalogs/{feature_display["_catalog_ref"]}/feature_displays',
            'title': 'catalog_feature_displays'
        }
    else:
        feature_display['_links']['parent'] = {
            'href': f'{base_url}/',
            'title': 'home'
        }
        feature_display['_links']['collection'] = {
            'href': f'{base_url}/feature_displays',
            'title': 'feature_displays'
        }
    

    
@trace
def _add_remote_children_links(feature_display):
    if not SETTINGS['HY_GATEWAY_URL']:
        return
    feature_display_id = get_resource_id(feature_display, 'feature_displays')

    # == do not edit this method above this line ==    

    
@trace
def _add_remote_parent_links(feature_display):
    if not SETTINGS['HY_GATEWAY_URL']:
        return
    feature_display_id = get_resource_id(feature_display, 'feature_displays')

    # == do not edit this method above this line ==    
