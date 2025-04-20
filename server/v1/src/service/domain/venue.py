"""
Defines the "venue" resource, and its "venues" resource collection.
"""
from typing import Optional
from pydantic import BaseModel, Field
from hypermea.core.domain import ResourceModel

class Venue(ResourceModel):    
    name: str
    description: Optional[str] = None
    capacity: int
    
    class Config:
        plural = 'venues'
