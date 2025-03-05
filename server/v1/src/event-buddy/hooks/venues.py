"""
hooks.venues
This module defines functions to add link relations to venues.
"""
import logging
import json
from flask import current_app
from hypermea.core.logging import trace
from configuration import SETTINGS
from hypermea.core.utils import get_resource_id, get_id_field, get_my_base_url
from hypermea.core.gateway import get_href_from_gateway
import affordances

LOG = logging.getLogger('hooks.venues')


@trace
def add_hooks(app):
    """Wire up the hooks for venues."""
    app.on_fetched_item_venues += _add_links_to_venue
    app.on_fetched_resource_venues += _add_links_to_venues_collection
    app.on_post_POST_venues += _post_venues


@trace
def _post_venues(request, payload):
    if payload.status_code == 201:
        j = json.loads(payload.data)
        if '_items' in j:
            _add_links_to_venues_collection(j, request.url)
        else:
            _add_links_to_venue(j)
        payload.data = json.dumps(j)


@trace
def _add_links_to_venues_collection(venues_collection, self_href=None):
    for venue in venues_collection['_items']:
        _add_links_to_venue(venue)

    if '_links' not in venues_collection:
        venues_collection['_links'] = {
            'self': {
                'href': self_href
            }
        }

    base_url = get_my_base_url()

    id_field = get_id_field('venues')
    if id_field.startswith('_'):
        id_field = id_field[1:]

    venues_collection['_links']['item'] = {
        'href': f'{base_url}/venues/{{{id_field}}}',
        'title': 'venue',
        'templated': True
    }
    
    self_href = venues_collection['_links']['self']['href']
    affordances.rfc6861.create_form.add_link(venues_collection, 'venues', self_href)


@trace
def _add_links_to_venue(venue):
    base_url = get_my_base_url()
    venue_id = get_resource_id(venue, 'venues')

    _add_remote_children_links(venue)
    _add_remote_parent_links(venue)

    venue['_links']['self'] = {
        'href': f"{base_url}/venues/{venue_id}",
        'title': 'venue'
    }
    affordances.rfc6861.edit_form.add_link(venue, 'venues')
    venue['_links']['events'] = {
        'href': f'{base_url}/venues/{venue_id}/events',
        'title': 'events'
    }



@trace
def _add_remote_children_links(venue):
    if not SETTINGS['HY_GATEWAY_URL']:
        return
    venue_id = get_resource_id(venue, 'venues')

    # == do not edit this method above this line ==


@trace
def _add_remote_parent_links(venue):
    if not SETTINGS['HY_GATEWAY_URL']:
        return
    venue_id = get_resource_id(venue, 'venues')

    # == do not edit this method above this line ==
