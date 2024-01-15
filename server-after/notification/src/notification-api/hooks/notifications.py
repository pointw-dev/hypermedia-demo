"""
hooks.notifications
This module defines functions to add link relations to notifications.
"""
import logging
import json
from flask import current_app
from hypermea.core.logging import trace
from configuration import SETTINGS
from hypermea.core.utils import get_resource_id, get_id_field, get_my_base_url
from hypermea.core.gateway import get_href_from_gateway
import affordances

LOG = logging.getLogger('hooks.notifications')


@trace
def add_hooks(app):
    """Wire up the hooks for notifications."""
    app.on_fetched_item_notifications += _add_links_to_notification
    app.on_fetched_resource_notifications += _add_links_to_notifications_collection
    app.on_post_POST_notifications += _post_notifications


@trace
def _post_notifications(request, payload):
    if payload.status_code == 201:
        j = json.loads(payload.data)
        if '_items' in j:
            for notification in j['_items']:
                _add_links_to_notification(notification)
        else:
            _add_links_to_notification(j)
        payload.data = json.dumps(j)


@trace
def _add_links_to_notifications_collection(notifications_collection):
    for notification in notifications_collection['_items']:
        _add_links_to_notification(notification)
        
    if '_links' in notifications_collection:
        base_url = get_my_base_url()

        id_field = get_id_field('notifications')
        if id_field.startswith('_'):
            id_field = id_field[1:]        
                
        notifications_collection['_links']['item'] = {
            'href': f'{base_url}/notifications/{{{id_field}}}',
            'title': 'notification',
            'templated': True
        }
        self_href = notifications_collection['_links']['self']['href']
        affordances.rfc6861.create_form.add_link(notifications_collection, 'notifications', self_href)                


@trace
def _add_links_to_notification(notification):
    base_url = get_my_base_url()
    notification_id = get_resource_id(notification, 'notifications')

    _add_remote_children_links(notification)
    _add_remote_parent_links(notification)

    notification['_links']['self'] = {
        'href': f"{base_url}/notifications/{notification_id}",
        'title': 'notification'
    }
    affordances.rfc6861.edit_form.add_link(notification, 'notifications')
    

    
@trace
def _add_remote_children_links(notification):
    if not SETTINGS['HY_GATEWAY_URL']:
        return
    notification_id = get_resource_id(notification, 'notifications')

    # == do not edit this method above this line ==    

    
@trace
def _add_remote_parent_links(notification):
    if not SETTINGS['HY_GATEWAY_URL']:
        return
    notification_id = get_resource_id(notification, 'notifications')
    if '_region_ref' in notification:
        notification['_links']['regions'] = {
            'href': f"{get_href_from_gateway('regions')}/{notification['_region_ref']}",
            'title': 'region_notifications'
        }

    # == do not edit this method above this line ==    
