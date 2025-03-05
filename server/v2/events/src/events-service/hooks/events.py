"""
hooks.events
This module defines functions to add link relations to events.
"""
import logging
import re
import json
import isodate
from flask import request as current_request
from bson import ObjectId
from hypermea.core.logging import trace
from configuration import SETTINGS
from hypermea.core.utils import get_resource_id, get_id_field, get_my_base_url, get_db
from hypermea.core.gateway import get_href_from_gateway
import affordances

LOG = logging.getLogger('hooks.events')


@trace
def add_hooks(app):
    """Wire up the hooks for events."""
    app.on_fetched_item_events += _add_links_to_event
    app.on_fetched_resource_events += _add_links_to_events_collection
    app.on_post_POST_events += _post_events
    app.on_pre_POST_events += _intercept

    app.on_insert_venues_events += _confirm_availability
    app.on_fetched_item_venues_events += _add_links_to_event
    app.on_fetched_resource_venues_events += _add_links_to_events_collection
    app.on_post_POST_venues_events += _post_events


#############################################################################################################
@trace
def _event_to_datetime_boundaries(event):
    start = isodate.parse_datetime(f"{event['date']}T{event['time']}")
    end = start + isodate.parse_duration(event['duration'])
    return start, end

@trace
def _is_overlapping(scheduled_event, new_event):
    new_event_start, new_event_end = _event_to_datetime_boundaries(new_event)
    scheduled_event_start, scheduled_event_end = _event_to_datetime_boundaries(scheduled_event)

    return (scheduled_event_start <= new_event_start < scheduled_event_end) or (
            scheduled_event_start < new_event_end <= scheduled_event_end)

@trace
def _overlaps_with(new_event, scheduled_events):
    for scheduled_event in scheduled_events:
        if _is_overlapping(scheduled_event, new_event):
            return scheduled_event['name']
    return

@trace
def _get_scheduled_events():
    venue = None
    if match := re.search(r'.*venues/(.*?)/events', current_request.base_url):
        venue = match.group(1)

    events_db = get_db()['events']
    return list(events_db.find({'_venue_ref': ObjectId(venue)}))

#############################################################################################################


@trace
def _intercept(request):
    abort(make_error_response('POST to a venue\'s event list', 403))


@trace
def _confirm_availability(incoming_events):
    schedule_events = _get_scheduled_events()

    for new_event in incoming_events:
        overlap = _overlaps_with(new_event, schedule_events)
        if overlap:
            abort(make_error_response(f'The "{new_event["name"]}" event overlaps with the "{overlap}" event at this venue', 409))
        else:
            schedule_events.append(new_event)


@trace
def _post_events(request, payload):
    if payload.status_code == 201:
        j = json.loads(payload.data)
        if '_items' in j:
            _add_links_to_events_collection(j, request.url)
        else:
            _add_links_to_event(j)
        payload.data = json.dumps(j)


@trace
def _add_links_to_events_collection(events_collection, self_href=None):
    events_collection['_items'] = sorted(events_collection['_items'], key=lambda item: item['date'] + item['time'])

    for event in events_collection['_items']:
        _add_links_to_event(event)

    if '_links' not in events_collection:
        events_collection['_links'] = {
            'self': {
                'href': self_href
            }
        }

    base_url = get_my_base_url()

    id_field = get_id_field('events')
    if id_field.startswith('_'):
        id_field = id_field[1:]

    events_collection['_links']['item'] = {
        'href': f'{base_url}/events/{{{id_field}}}',
        'title': 'event',
        'templated': True
    }
    
    self_href = events_collection['_links']['self']['href']
    affordances.rfc6861.create_form.add_link(events_collection, 'events', self_href)


@trace
def _add_links_to_event(event):
    base_url = get_my_base_url()
    event_id = get_resource_id(event, 'events')

    _add_remote_children_links(event)
    _add_remote_parent_links(event)

    event['_links']['self'] = {
        'href': f"{base_url}/events/{event_id}",
        'title': 'event'
    }
    affordances.rfc6861.edit_form.add_link(event, 'events')
    affordances.register.add_link(event, 'events')



@trace
def _add_remote_children_links(event):
    if not SETTINGS['HY_GATEWAY_URL']:
        return
    event_id = get_resource_id(event, 'events')
    event['_links']['registrations'] = {
        'href': f"{get_href_from_gateway('registrations')}/event/{event_id}",
        'title': 'registrations'
    }

    # == do not edit this method above this line ==


@trace
def _add_remote_parent_links(event):
    if not SETTINGS['HY_GATEWAY_URL']:
        return
    event_id = get_resource_id(event, 'events')
    if '_venue_ref' in event:
        event['_links']['venues'] = {
            'href': f"{get_href_from_gateway('venues')}/{event['_venue_ref']}",
            'title': 'venue_events'
        }

    # == do not edit this method above this line ==
