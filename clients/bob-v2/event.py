import json
import requests
from config import REGISTRATIONS_BASE_API_URL, EVENTS_BASE_API_URL
from api import Api
from console import Console


class Event(dict):
    def __init__(self, data):
        super().__init__(data)

    @property
    def name(self):
        return self.get('name')

    # <<api>>
    def register(self, username=None):
        user_spec = json.dumps({'username': username}) if username else {}
        url = Api.url_join(EVENTS_BASE_API_URL, f'/events/{self["_id"]}/register')
        result = requests.put(url, data=user_spec, headers=Api.get_headers())

        if result.ok:
            print(f'\n- Registered for {self.name}')
        else:
            Api.display_error(result)
            if result.status_code == 403 and not username:
                username = Console.input_with_quit_or_cancel('Please enter a username to register').lower()
                if username:
                    self.register(username)

    # <<api>>
    def view_attendees(self):
        url = Api.url_join(REGISTRATIONS_BASE_API_URL, f'/registrations/event/{self["_id"]}')
        url += '?embed=account'
        result = requests.get(url, headers=Api.get_headers())
        registrations = result.json()
        print(f'\nAttending "{self.name}" on {self["date"]} at {self["time"]}:')

        if not registrations['_embedded']['registration']:
            print('- no one has registered yet')
        else:
            for registration in registrations['_embedded']['registration']:
                print(f"- {registration['_embedded']['account'].get('name', 'Not authorized to view attendees')}")

    @staticmethod
    def get_new_event():
        new_event = Console.prompt_for_fields({
            'name': 'Please enter the name of your event',
            'date': 'What date is your event? [YYYY-MM-DD]',
            'time': 'What time does the event start? [HH:MM:SS]',
            'duration': 'How long is the event? [#m or #h]'
        })

        if new_event:
            new_event['duration'] = 'PT' + new_event['duration'].upper()
        return new_event
