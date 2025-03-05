hy api create event-buddy --add-auth --add-docker --add-validation

hy resource create event
hy resource create venue
hy resource create registration
hy resource create account

hy link create venue events
hy link create event registrations
hy link create account registrations

hy affordance create register event
