"""
hooks.account
This module defines provides lifecycle hooks for the account resource.
"""
import logging
import json
from flask import request as current_request
from hypermea.core.logging import trace
from hypermea.core.href import get_resource_id, add_etag_header_to_post, get_self_href_from_request
from hypermea.core.gateway import get_href_from_gateway
import settings
import affordances

LOG = logging.getLogger('hooks.account')


@trace
def add_hooks(app):
    """Wire up the hooks for account."""
    app.on_post_POST_accounts += add_etag_header_to_post
    app.on_post_POST_accounts += _post_accounts
    app.on_fetched_item_accounts += _add_links_to_account
    app.on_fetched_resource_accounts += _add_links_to_accounts_collection


@trace
def _post_accounts(request, payload):
    if payload.status_code == 201:
        j = json.loads(payload.data)
        if '_items' in j:
            _add_links_to_accounts_collection(j)
        else:
            _add_links_to_account(j)
        payload.data = json.dumps(j)


@trace
def _add_links_to_accounts_collection(accounts_collection):
    affordances.rfc6861.create_form.add_link(accounts_collection, 'accounts')
    for account in accounts_collection['_items']:
        _add_links_to_account(account)


@trace
def _add_links_to_account(account):
    _add_external_children_links(account)
    _add_external_parent_links(account)
    affordances.rfc6861.edit_form.add_link(account, 'accounts')


## The following two methods are here for use by `hy link create`
## Modifying them may make it more difficult to create a link from
## another resource to this one.

@trace
def _add_external_children_links(account):
    if not settings.hypermea.gateway_url:
        return
    account_id = get_resource_id(account, 'accounts')

    # == do not edit this method above this line ==


@trace
def _add_external_parent_links(account):
    if not settings.hypermea.gateway_url:
        return
    account_id = get_resource_id(account, 'accounts')

    # == do not edit this method above this line ==
