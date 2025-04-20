"""
Defines the "registration" resource, and its "registrations" resource collection.
"""
from typing import Optional
from pydantic import BaseModel, Field
from hypermea.core.domain import ResourceModel

class Registration(ResourceModel):    
    pass
        
    class Config:
        plural = 'registrations'
