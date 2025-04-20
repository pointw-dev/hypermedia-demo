#!/bin/bash

hy service create event-buddy

hy resource create venue
hy resource create event
hy resource create registration
hy resource create account

hy link create venue events
hy link create event registrations
hy link create account registrations

hy service addin -g
