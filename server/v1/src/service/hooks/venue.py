"""
hooks.venue
This module defines provides lifecycle hooks for the venue resource.
"""
import logging
import json
from flask import request as current_request
from hypermea.core.logging import trace
from hypermea.core.href import get_resource_id, add_etag_header_to_post, get_self_href_from_request
from hypermea.core.gateway import get_href_from_gateway
import settings
import affordances

LOG = logging.getLogger('hooks.venue')


@trace
def add_hooks(app):
    """Wire up the hooks for venue."""
    app.on_post_POST_venues += add_etag_header_to_post
    app.on_post_POST_venues += _post_venues
    app.on_fetched_item_venues += _add_links_to_venue
    app.on_fetched_resource_venues += _add_links_to_venues_collection


@trace
def _post_venues(request, payload):
    if payload.status_code == 201:
        j = json.loads(payload.data)
        if '_items' in j:
            _add_links_to_venues_collection(j)
        else:
            _add_links_to_venue(j)
        payload.data = json.dumps(j)


@trace
def _add_links_to_venues_collection(venues_collection):
    affordances.rfc6861.create_form.add_link(venues_collection, 'venues')
    for venue in venues_collection['_items']:
        _add_links_to_venue(venue)


@trace
def _add_links_to_venue(venue):
    _add_external_children_links(venue)
    _add_external_parent_links(venue)
    affordances.rfc6861.edit_form.add_link(venue, 'venues')


## The following two methods are here for use by `hy link create`
## Modifying them may make it more difficult to create a link from
## another resource to this one.

@trace
def _add_external_children_links(venue):
    if not settings.hypermea.gateway_url:
        return
    venue_id = get_resource_id(venue, 'venues')

    # == do not edit this method above this line ==


@trace
def _add_external_parent_links(venue):
    if not settings.hypermea.gateway_url:
        return
    venue_id = get_resource_id(venue, 'venues')
    if '_owner_ref' in venue:
        venue['_links']['owner'] = {
            'href': f"{get_href_from_gateway('owner')}/{venue['_owner_ref']}",
            
        }

    # == do not edit this method above this line ==
