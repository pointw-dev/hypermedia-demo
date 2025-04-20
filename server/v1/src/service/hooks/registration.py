"""
hooks.registration
This module defines provides lifecycle hooks for the registration resource.
"""
import logging
import json
from flask import request as current_request
from hypermea.core.logging import trace
from hypermea.core.href import get_resource_id, add_etag_header_to_post, get_self_href_from_request
from hypermea.core.gateway import get_href_from_gateway
import settings
import affordances

LOG = logging.getLogger('hooks.registration')


@trace
def add_hooks(app):
    """Wire up the hooks for registration."""
    app.on_post_POST_registrations += add_etag_header_to_post
    app.on_post_POST_registrations += _post_registrations
    app.on_fetched_item_registrations += _add_links_to_registration
    app.on_fetched_resource_registrations += _add_links_to_registrations_collection

    app.on_fetched_item_events_registrations += _add_links_to_registration
    app.on_fetched_resource_events_registrations += _add_links_to_registrations_collection
    app.on_post_POST_events_registrations += add_etag_header_to_post
    app.on_post_POST_events_registrations += _post_registrations

    app.on_fetched_item_accounts_registrations += _add_links_to_registration
    app.on_fetched_resource_accounts_registrations += _add_links_to_registrations_collection
    app.on_post_POST_accounts_registrations += add_etag_header_to_post
    app.on_post_POST_accounts_registrations += _post_registrations

    app.on_fetched_item_venues_registrations += _add_links_to_registration
    app.on_fetched_resource_venues_registrations += _add_links_to_registrations_collection
    app.on_post_POST_venues_registrations += add_etag_header_to_post
    app.on_post_POST_venues_registrations += _post_registrations


@trace
def _post_registrations(request, payload):
    if payload.status_code == 201:
        j = json.loads(payload.data)
        if '_items' in j:
            _add_links_to_registrations_collection(j)
        else:
            _add_links_to_registration(j)
        payload.data = json.dumps(j)


@trace
def _add_links_to_registrations_collection(registrations_collection):
    affordances.rfc6861.create_form.add_link(registrations_collection, 'registrations')
    for registration in registrations_collection['_items']:
        _add_links_to_registration(registration)


@trace
def _add_links_to_registration(registration):
    _add_external_children_links(registration)
    _add_external_parent_links(registration)
    affordances.rfc6861.edit_form.add_link(registration, 'registrations')


## The following two methods are here for use by `hy link create`
## Modifying them may make it more difficult to create a link from
## another resource to this one.

@trace
def _add_external_children_links(registration):
    if not settings.hypermea.gateway_url:
        return
    registration_id = get_resource_id(registration, 'registrations')

    # == do not edit this method above this line ==


@trace
def _add_external_parent_links(registration):
    if not settings.hypermea.gateway_url:
        return
    registration_id = get_resource_id(registration, 'registrations')
    if '_event_ref' in registration:
        registration['_links']['event'] = {
            'href': f"{get_href_from_gateway('event')}/{registration['_event_ref']}",
            
        }
    if '_account_ref' in registration:
        registration['_links']['account'] = {
            'href': f"{get_href_from_gateway('account')}/{registration['_account_ref']}",
            
        }
    if '_venue_ref' in registration:
        registration['_links']['venue'] = {
            'href': f"{get_href_from_gateway('venue')}/{registration['_venue_ref']}",
            
        }

    # == do not edit this method above this line ==
