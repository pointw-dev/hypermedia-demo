from typing import Optional
from pydantic import SecretStr, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from settings.helpers import SecretField

class AuthSettings(BaseSettings):
    """
    HypermeaService authorization settings.
    """
    model_config = SettingsConfigDict(env_prefix='AUTH_')

    realm: str = Field(
        default='event-buddy.hypermea.com',
        description='The realm value used to build in auth challenges.'
    )
    allow_get_home: bool = Field(
        default=True
    )

    claims_namespace: str = Field(
        default='uri://hypermea.com/event-buddy/claims',
        description='The namespace used for unique claims issued by your auth provider.'
    )
    jwt_domain: str = Field(
        default='event-buddy.us.auth0.com'
    )
    jwt_issuer: str = Field(
        default='https://event-buddy.us.auth0.com'
    )
    jwt_audience: str = Field(
        default='uri://hypermea.com/event-buddy'
    )

    add_basic: bool = Field(
        default=True,
        description='When enabled, the basic auth handler will be in effect.'
    )
    enable_root_user: Optional[bool] = Field(
        default=True
    )
    root_password: Optional[SecretStr] = SecretField(
        default='password',
        description='Password for the root user (if enabled).'
    )
