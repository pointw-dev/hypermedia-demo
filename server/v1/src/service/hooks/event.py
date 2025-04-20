"""
hooks.event
This module defines provides lifecycle hooks for the event resource.
"""
import logging
import json
import re
import isodate
from bson.objectid import ObjectId
from flask import request as current_request, abort
from hypermea.core.logging import trace
from hypermea.core.href import get_resource_id, add_etag_header_to_post, get_self_href_from_request
from hypermea.core.gateway import get_href_from_gateway
from hypermea.core.response import make_error_response
from hypermea.core.utils import get_db
import settings
import affordances

LOG = logging.getLogger('hooks.event')


@trace
def add_hooks(app):
    """Wire up the hooks for event."""
    app.on_post_POST_events += add_etag_header_to_post
    app.on_post_POST_events += _post_events
    app.on_fetched_item_events += _add_links_to_event
    app.on_fetched_resource_events += _add_links_to_events_collection

    app.on_fetched_item_venues_events += _add_links_to_event
    app.on_fetched_resource_venues_events += _add_links_to_events_collection
    app.on_post_POST_venues_events += add_etag_header_to_post
    app.on_post_POST_venues_events += _post_events

    #####
    app.on_pre_POST_events += _intercept
    app.on_insert_venues_events += _confirm_availability
    #####


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
#############################################################################################################



@trace
def _post_events(request, payload):
    if payload.status_code == 201:
        j = json.loads(payload.data)
        if '_items' in j:
            _add_links_to_events_collection(j)
        else:
            _add_links_to_event(j)
        payload.data = json.dumps(j)


@trace
def _add_links_to_events_collection(events_collection):
    affordances.rfc6861.create_form.add_link(events_collection, 'events')
    for event in events_collection['_items']:
        _add_links_to_event(event)


@trace
def _add_links_to_event(event):
    _add_external_children_links(event)
    _add_external_parent_links(event)
    affordances.rfc6861.edit_form.add_link(event, 'events')
    affordances.register.add_link(event, 'events')


## The following two methods are here for use by `hy link create`
## Modifying them may make it more difficult to create a link from
## another resource to this one.

@trace
def _add_external_children_links(event):
    if not settings.hypermea.gateway_url:
        return
    event_id = get_resource_id(event, 'events')

    # == do not edit this method above this line ==


@trace
def _add_external_parent_links(event):
    if not settings.hypermea.gateway_url:
        return
    event_id = get_resource_id(event, 'events')
    if '_venue_ref' in event:
        event['_links']['venue'] = {
            'href': f"{get_href_from_gateway('venue')}/{event['_venue_ref']}",
            
        }

    # == do not edit this method above this line ==
