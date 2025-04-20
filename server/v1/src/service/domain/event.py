"""
Defines the "event" resource, and its "events" resource collection.
"""
from typing import Optional
from pydantic import BaseModel, Field
from hypermea.core.domain import ResourceModel

class Event(ResourceModel):    
    name: str
    description: Optional[str] = None
    date: str       # iso_date
    time: str       # iso_time
    duration: str   # iso_duration

    
    class Config:
        plural = 'events'

