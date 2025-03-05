"""
hooks.accounts
This module defines functions to add link relations to accounts.
"""
import logging
import json
from flask import current_app
from hypermea.core.logging import trace
from configuration import SETTINGS
from hypermea.core.utils import get_resource_id, get_id_field, get_my_base_url
from hypermea.core.gateway import get_href_from_gateway
import affordances

LOG = logging.getLogger('hooks.accounts')


@trace
def add_hooks(app):
    """Wire up the hooks for accounts."""
    app.on_fetched_item_accounts += _add_links_to_account
    app.on_fetched_resource_accounts += _add_links_to_accounts_collection
    app.on_post_POST_accounts += _post_accounts


@trace
def _post_accounts(request, payload):
    if payload.status_code == 201:
        j = json.loads(payload.data)
        if '_items' in j:
            _add_links_to_accounts_collection(j, request.url)
        else:
            _add_links_to_account(j)
        payload.data = json.dumps(j)


@trace
def _add_links_to_accounts_collection(accounts_collection, self_href=None):
    for account in accounts_collection['_items']:
        _add_links_to_account(account)

    if '_links' not in accounts_collection:
        accounts_collection['_links'] = {
            'self': {
                'href': self_href
            }
        }

    base_url = get_my_base_url()

    id_field = get_id_field('accounts')
    if id_field.startswith('_'):
        id_field = id_field[1:]

    accounts_collection['_links']['item'] = {
        'href': f'{base_url}/accounts/{{{id_field}}}',
        'title': 'account',
        'templated': True
    }
    
    self_href = accounts_collection['_links']['self']['href']
    affordances.rfc6861.create_form.add_link(accounts_collection, 'accounts', self_href)


@trace
def _add_links_to_account(account):
    base_url = get_my_base_url()
    account_id = get_resource_id(account, 'accounts')

    _add_remote_children_links(account)
    _add_remote_parent_links(account)

    account['_links']['self'] = {
        'href': f"{base_url}/accounts/{account_id}",
        'title': 'account'
    }
    affordances.rfc6861.edit_form.add_link(account, 'accounts')



@trace
def _add_remote_children_links(account):
    if not SETTINGS['HY_GATEWAY_URL']:
        return
    account_id = get_resource_id(account, 'accounts')
    account['_links']['registrations'] = {
        'href': f"{get_href_from_gateway('registrations')}/account/{account_id}",
        'title': 'registrations'
    }

    # == do not edit this method above this line ==


@trace
def _add_remote_parent_links(account):
    if not SETTINGS['HY_GATEWAY_URL']:
        return
    account_id = get_resource_id(account, 'accounts')

    # == do not edit this method above this line ==
