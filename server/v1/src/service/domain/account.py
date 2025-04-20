"""
Defines the "account" resource, and its "accounts" resource collection.
"""
from typing import Optional, Literal
from pydantic import BaseModel, Field
from hypermea.core.domain import ResourceModel

class Account(ResourceModel):    
    username: str       # unique
    name: str
    role: Literal['member', 'manager', 'hr']
    
    class Config:
        plural = 'accounts'
