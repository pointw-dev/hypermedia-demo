"""
Defines the "event" resource, and its "events" resource collection.
"""
from typing import Optional
from datetime import date, time, timedelta
from pydantic import BaseModel, Field
from hypermea.core.domain import ResourceModel

class Event(ResourceModel):    
    name: str
    description: Optional[str] = None
    date: date
    time: time
    duration: timedelta


    class Config:
        plural = 'events'

