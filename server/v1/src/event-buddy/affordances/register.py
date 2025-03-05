"""
This module defines functions to add affordances.register.
"""
import json
import logging
from flask import make_response, request
from hypermea.core.utils import (make_error_response, unauthorized_message,
                                 get_resource_id, get_my_base_url, get_db, get_api)
from bson import ObjectId

LOG = logging.getLogger("affordances.register")


def add_affordance(app):
    @app.route("/events/<event_id>/register", methods=["PUT"])
    def do_register_event(event_id):
        if app.auth and (not app.auth.authorized(None, "register", "PUT")):
            return make_error_response(unauthorized_message, 401)

        return _do_register_event(ObjectId(event_id), app.auth.account)


def add_link(resource, collection_name):
    base_url = get_my_base_url()
    resource_id = get_resource_id(resource, collection_name)

    resource['_links']['register'] = {
        'href': f'{base_url}/{collection_name}/{resource_id}/register',
        'title': 'PUT to register for this event (admin only: with {"username": username} in the body)'
    }


def _do_register_event(event_id, account):
    if account['role'] == 'member':
        if request.data:
            return make_error_response(
                "Body found in PUT. Members are not allowed to register on other's behalf", 403
            )

        return _register({'_event_ref': event_id, '_account_ref': account['_id']})

    # For managers or HR
    if not request.is_json or not request.data:
        return make_error_response(f"As a member of the '{account['role']}' role, "
                                   "you must specify who you are registering.", 403)

    username = request.json.get('username')
    if not username:
        return make_error_response(
            f"As a member of the '{account['role']}' role, you must specify who you are"
            " registering.",
            403)

    my_username = account['username']
    account = get_db()['accounts'].find_one({'username': username})
    if not account:
        return make_error_response(f"user '{username}' is not a valid member", 403)

    return _register({'_event_ref': event_id, '_account_ref': account['_id']},
                     username if not username == username else None)


def _register(registration, username=None):
    registrations = get_db()['registrations']

    if registrations.find_one(registration):
        return make_response("already registered", 200)

    events = get_db()['events']
    event = events.find_one({'_id': ObjectId(registration['_event_ref'])})
    venues = get_db()['venues']
    venue = venues.find_one({'_id': event['_venue_ref']})
    attendee_count = registrations.count_documents({'_event_ref': registration['_event_ref']})

    if attendee_count >= venue['capacity']:
        return make_error_response("The venue for this event is at capacity and "
                                   "can accept no more registrations", 409)

    if registrations.find_one(registration):
        return make_response("already registered", 200)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': request.headers.get("authorization")
    }

    response = get_api().post(
        f"/events/{registration['_event_ref']}/registrations",
        data=json.dumps(registration, default=str),
        headers=headers
    )

    if response.status_code != 201:
        return make_error_response("Registration failed", response.status_code)

    if username:
        registrations.find_one_and_update(registration, {'$set': {'_tenant': username}})

    return make_response("registered", 200)
