#!/usr/bin/env python3

import json
from halchemy import Api

api = Api('http://localhost:2112')
ROOT = api.root.get()
VERBOSE = True

VENUES = [
	{ "name": "Developer Meeting Room",
	  "capacity": 5,
	  "events": [
	  	{
	  		"name": "Daily Standup",
	  		"date": "2025-02-07",
	  		"time": "09:00:00",
	  		"duration": "PT15M"
	  	},
	  	{
	  		"name": "Requirements review",
	  		"date": "2025-02-07",
	  		"time": "10:00:00",
	  		"duration": "PT1H"
	  	}
	  ]
	},
	{ "name": "Customer Meeting Room 1",
	  "capacity": 15,
	  "events": [
	  ]
	},
	{ "name": "Customer Meeting Room 2",
	  "capacity": 15,
	  "events": [
	  ]
	},
	{ "name": "Main Boardroom",
	  "capacity": 25,
	  "events": [
	  	{
	  		"name": "All Hands",
	  		"date": "2025-02-07",
	  		"time": "10:00:00",
	  		"duration": "PT1H"
	  	}	  
	  ]
	}
]

ACCOUNTS = [
	{'username': 'phartman', 'name': 'Pat Hartman', 'role': 'member'},
	{'username': 'tgraves', 'name': 'Terry Graves', 'role': 'member'},
	{'username': 'jkelly', 'name': 'Jamie Kelly', 'role': 'member'},
	{'username': 'fwinters', 'name': 'Felicia Winters', 'role': 'member'},
	{'username': 'clopez', 'name': 'Courtney Lopez', 'role': 'member'},
	{'username': 'sheath', 'name': 'Samantha Heath', 'role': 'member'},
	{'username': 'gjohnson', 'name': 'Gail Johnson', 'role': 'member'},
	{'username': 'dthibideau', 'name': 'Denise Thibideau', 'role': 'member'},
	{'username': 'manderson', 'name': 'Mel Anderson', 'role': 'manager'},
	{'username': 'hreagan', 'name': 'Harper Reagan', 'role': 'hr'},
]


def vprint(message):
	if VERBOSE:
		print(message)

def rprint(result):
	emoji = '🚨 ' if result._halchemy.response.status_code >399 else ''
	vprint(f'- {result._halchemy.request.url}: {emoji}{result._halchemy.response.status_code}')
	


def clear_resources():
	vprint('Deleting...')
	result = api.follow(ROOT).to('registration').delete()
	rprint(result)
	result = api.follow(ROOT).to('event').delete()
	rprint(result)
	result = api.follow(ROOT).to('venue').delete()
	rprint(result)
	result = api.follow(ROOT).to('account').delete()
	rprint(result)


def populate_resources():
	vprint('Adding accounts...')
	for account in ACCOUNTS:
		result = api.follow(ROOT).to('account').post(account)
		rprint(result)


	vprint('Adding venues...')
	for venue in VENUES:
		events = venue['events']
		del venue['events']
		new_venue = api.follow(ROOT).to('venue').post(venue)
		rprint(new_venue)
		first = True
		vprint('Adding events...')
		for event in events:
			new_event = api.follow(new_venue).to('event').post(event)
			rprint(new_event)
			if first:
				first = False
				for index in range(0,4):
					vprint('Registering...')
					result = api.follow(new_event).to('register').put({'username': ACCOUNTS[index]['username']})
					rprint(result)


def reset_scenario():
	clear_resources()
	populate_resources()


if __name__ == "__main__":
	reset_scenario()
