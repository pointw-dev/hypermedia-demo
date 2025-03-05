#!/usr/bin/env python3

import json
from halchemy import Api

API = Api('http://localhost:2112')
ROOT = API.root.get()

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


def clear_resources():
	API.follow(ROOT).to('registrations').delete()
	API.follow(ROOT).to('events').delete()
	API.follow(ROOT).to('venues').delete()
	API.follow(ROOT).to('accounts').delete()


def populate_resources():
	for account in ACCOUNTS:
		result = API.follow(ROOT).to('accounts').post(account)		

	for venue in VENUES:
		events = venue['events']
		del venue['events']
		venue = API.follow(ROOT).to('venues').post(venue)
		first = True
		for event in events:
			new_event = API.follow(venue).to('events').post(event)
			if first:
				first = False
				for index in range(0,4):
					result = API.follow(new_event).to('register').put({'username': ACCOUNTS[index]['username']})


def reset_scenario():
	clear_resources()
	populate_resources()


if __name__ == "__main__":
	reset_scenario()
