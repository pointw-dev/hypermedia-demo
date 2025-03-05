#!/usr/bin/env python3

import sys
from api import Api
from venue import Venue
from console import Console


def login():
    Api.logged_in_as = 'root'
    if len(sys.argv) == 1:
        return
    username = sys.argv[1].lower()
    if username not in Api.usernames:
        return
    Api.logged_in_as = username


def main():
    login()

    while True:
        Console.clear_screen()
        Console.title('Meeting Buddy', '=')

        venue = Venue.select_venue()
        if venue is None:
            continue
        venue.manage_events()


if __name__ == '__main__':
    main()
