"""
hooks.registrations
This module defines functions to add link relations to registrations.
"""
import logging
import json
from flask import current_app
from hypermea.core.logging import trace
from configuration import SETTINGS
from hypermea.core.utils import get_resource_id, get_id_field, get_my_base_url
from hypermea.core.gateway import get_href_from_gateway
import affordances

LOG = logging.getLogger('hooks.registrations')


@trace
def add_hooks(app):
    """Wire up the hooks for registrations."""
    app.on_fetched_item_registrations += _add_links_to_registration
    app.on_fetched_resource_registrations += _add_links_to_registrations_collection
    app.on_post_POST_registrations += _post_registrations

    app.on_fetched_item_events_registrations += _add_links_to_registration
    app.on_fetched_resource_events_registrations += _add_links_to_registrations_collection
    app.on_post_POST_events_registrations += _post_registrations

    app.on_fetched_item_accounts_registrations += _add_links_to_registration
    app.on_fetched_resource_accounts_registrations += _add_links_to_registrations_collection
    app.on_post_POST_accounts_registrations += _post_registrations


@trace
def _post_registrations(request, payload):
    if payload.status_code == 201:
        j = json.loads(payload.data)
        if '_items' in j:
            _add_links_to_registrations_collection(j, request.url)
        else:
            _add_links_to_registration(j)
        payload.data = json.dumps(j)


@trace
def _add_links_to_registrations_collection(registrations_collection, self_href=None):
    for registration in registrations_collection['_items']:
        _add_links_to_registration(registration)

    if '_links' not in registrations_collection:
        registrations_collection['_links'] = {
            'self': {
                'href': self_href
            }
        }

    base_url = get_my_base_url()

    id_field = get_id_field('registrations')
    if id_field.startswith('_'):
        id_field = id_field[1:]

    registrations_collection['_links']['item'] = {
        'href': f'{base_url}/registrations/{{{id_field}}}',
        'title': 'registration',
        'templated': True
    }
    
    self_href = registrations_collection['_links']['self']['href']
    affordances.rfc6861.create_form.add_link(registrations_collection, 'registrations', self_href)


@trace
def _add_links_to_registration(registration):
    base_url = get_my_base_url()
    registration_id = get_resource_id(registration, 'registrations')

    _add_remote_children_links(registration)
    _add_remote_parent_links(registration)

    registration['_links']['self'] = {
        'href': f"{base_url}/registrations/{registration_id}",
        'title': 'registration'
    }
    affordances.rfc6861.edit_form.add_link(registration, 'registrations')
    if registration.get('_event_ref'):
        registration['_links']['parent'] = {
            'href': f'{base_url}/events/{registration["_event_ref"]}',
            'title': 'events'
        }
        registration['_links']['collection'] = {
            'href': f'{base_url}/events/{registration["_event_ref"]}/registrations',
            'title': 'event_registrations'
        }
    else:
        registration['_links']['parent'] = {
            'href': f'{base_url}/',
            'title': 'home'
        }
        registration['_links']['collection'] = {
            'href': f'{base_url}/registrations',
            'title': 'registrations'
        }
    if registration.get('_account_ref'):
        registration['_links']['parent'] = {
            'href': f'{base_url}/accounts/{registration["_account_ref"]}',
            'title': 'accounts'
        }
        registration['_links']['collection'] = {
            'href': f'{base_url}/accounts/{registration["_account_ref"]}/registrations',
            'title': 'account_registrations'
        }
    else:
        registration['_links']['parent'] = {
            'href': f'{base_url}/',
            'title': 'home'
        }
        registration['_links']['collection'] = {
            'href': f'{base_url}/registrations',
            'title': 'registrations'
        }



@trace
def _add_remote_children_links(registration):
    if not SETTINGS['HY_GATEWAY_URL']:
        return
    registration_id = get_resource_id(registration, 'registrations')

    # == do not edit this method above this line ==


@trace
def _add_remote_parent_links(registration):
    if not SETTINGS['HY_GATEWAY_URL']:
        return
    registration_id = get_resource_id(registration, 'registrations')

    # == do not edit this method above this line ==
