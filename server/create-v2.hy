#!/bin/bash

mkdir event-service
mkdir venue-service
mkdir registration-service
mkdir account-service


cd event-service
hy service create event-service -ad
hy resource create event
hy link create external:venue events
hy link create event external:registrations

hy affordance create register event
cp ../../v1/src/service/auth/*.py src/service/auth
echo
cd ..

cd venue-service
hy service create venue-service -ad
hy resource create venue
hy link create venue external:events
cp ../../v1/src/service/auth/*.py src/service/auth
echo
cd ..


cd registration-service
hy service create registration-service -ad
hy resource create registration
hy link create external:event registrations
hy link create external:account registrations
cp ../../v1/src/service/auth/*.py src/service/auth
echo
cd ..


cd account-service
hy service create account-service -ad
hy resource create account
hy link create account external:registrations
cp ../../v1/src/service/auth/*.py src/service/auth
echo
cd ..

echo 
echo - Now modify the src/service/settings/auth.py for each
