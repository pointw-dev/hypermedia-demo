import json
import requests
from event import Event
from api import Api
from console import Console
from utils import format_duration


class Venue(dict):
    def __init__(self, data):
        super().__init__(data)

    @property
    def name(self):
        return self.get('name')

    # <<api>>
    def get_events(self):
        url = Api.url_from_resource(self, 'events')
        result = requests.get(url, headers=Api.get_headers())
        events_data = result.json()['_items']
        return [Event(event) for event in events_data]

    # <<api>>
    def add_event(self, event_data):
        data = json.dumps(event_data)
        url = Api.url_from_resource(self, 'events')
        result = requests.post(url, data=data, headers=Api.get_headers())
        if result.ok:
            print('\n> Success')
        else:
            Api.display_error(result)

    def manage_events(self):
        managing_events = True
        while managing_events:
            events = self.get_events()
            self._display_events(events)

            choice = self._get_user_choice()
            if choice == 'q' or choice is None:
                managing_events = False
            else:
                self._handle_choice(choice, events)

    def _display_events(self, events):
        print()
        Console.title(f'Events for {self.name}')

        current_date = ''
        for idx, event in enumerate(events, start=1):
            if event['date'] != current_date:
                current_date = event['date']
                print(event['date'])
            print(f"  {idx}. {event['time']} {event.name} ({format_duration(event['duration'])})")

    def _get_user_choice(self):
        rtn = Console.input_with_quit_or_cancel('[A]dd an event, [R]egister, [V]iew attendees')
        if rtn:
            rtn = rtn.lower()
        return rtn

    def _handle_choice(self, choice, events):
        if choice == 'a':
            self._add_event()
        elif choice in ['r', 'v']:
            self._select_event_and_perform_action(choice, events)
        else:
            print('\nInvalid selection')

    def _add_event(self):
        new_event = Event.get_new_event()
        if new_event:
            self.add_event(new_event)

    def _select_event_and_perform_action(self, choice, events):
        event_number = Console.select_from_menu('Select an event', len(events))
        if event_number is None:
            return

        event = events[event_number]

        if choice == 'r':
            event.register()
        elif choice == 'v':
            event.view_attendees()

    # <<api>>
    @staticmethod
    def select_venue():
        root = Api.get_root_resource()
        url = Api.url_from_resource(root, 'venues')
        result = requests.get(url, headers=Api.get_headers())
        venues_data = result.json()['_items']
        venues = [Venue(venue) for venue in venues_data]

        Console.title('Venues')
        for idx, venue in enumerate(venues, start=1):
            print(f'{idx}. {venue.name}')
        choice = Console.select_from_menu('\nPlease select a venue to manage', len(venues))
        return None if choice is None else venues[choice]
