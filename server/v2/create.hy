# hy api create event-buddy --add-auth --add-docker --add-validation

# in events-service
hy resource create event
hy link create remote:venue events
hy link create event remote:registrations

hy affordance create register event


# in venues-service
hy resource create venue
hy link create venue remote:events


# in registrations-service
hy resource create registration
hy link create remote:event registrations
hy link create remote:account registrations


#in accounts-service
hy resource create account
hy link create account remote:registrations
