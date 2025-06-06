"""
This file is mainly for hypermea use.  It is managed by hypermea and it is
not recommended to modify it.  Its two main purposes are
* dump settings to the log
* for tests (to override settings to drive test scenarios)
"""

from pydantic import BaseModel

from . import _registry, get_hypermea, get_logging, get_rate_limit, get_mongo, get_smtp, get_auth

from .hypermea import HypermeaSettings
from .logging import LoggingSettings
from .rate_limit import RateLimitSettings
from .auth import AuthSettings

from integration.mongo.settings import MongoSettings
from integration.smtp.settings import SmtpSettings



class AllSettings(BaseModel):
    hypermea: HypermeaSettings
    logging: LoggingSettings
    rate_limit: RateLimitSettings
    mongo: MongoSettings
    smtp: SmtpSettings
    auth: AuthSettings


def get_settings() -> AllSettings:
    return AllSettings(
        hypermea=get_hypermea(),
        logging=get_logging(),
        rate_limit=get_rate_limit(),
        mongo=get_mongo(),
        smtp=get_smtp(),
        auth=get_auth()
    )


def build_settings(
    hypermea: HypermeaSettings = None,
    logging: LoggingSettings = None,
    rate_limit: RateLimitSettings = None,
    mongo: MongoSettings = None,
    smtp: SmtpSettings = None,
    auth: AuthSettings = None
) -> AllSettings:
    defaults = get_settings()
    return AllSettings(
        hypermea=hypermea or defaults.hypermea,
        logging=logging or defaults.logging,
        rate_limit=rate_limit or defaults.rate_limit,
        mongo=mongo or defaults.mongo,
        smtp=smtp or defaults.smtp,
        auth=auth or defaults.auth
    )


def inject_settings(overrides: AllSettings):
    current = get_settings()

    for key, override in overrides.model_dump(exclude_none=True).items():
        base = getattr(current, key)
        merged = {**base.model_dump(), **override}
        _registry[key] = base.__class__(**merged)


def reset_settings():
    all_settings = get_settings()
    for key in _registry:
        _registry[key] = getattr(all_settings, key)


def settings_dump(pretty: bool = False) -> str | dict:
    settings_dict = get_settings().model_dump()
    if pretty:
        import json
        return json.dumps(settings_dict, indent=2)
    return settings_dict


def devops_settings_dump(pretty: bool = False) -> str | list[dict]:
    settings_models = [
        ("hypermea", get_hypermea()),
        ("logging", get_logging()),
        ("rate_limit", get_rate_limit()),
        ("mongo", get_mongo()),
        ("smtp", get_smtp()),
        ("auth", get_auth())
    ]

    result = []
    for _, model in settings_models:
        fields = model.model_fields
        values = model.model_dump()
        section = {
            "description": model.__doc__.strip() if model.__doc__ else "",
            "settings": {}
        }

        env_prefix = model.model_config.get("env_prefix", "")

        for field_name, field_info in fields.items():
            alias = field_info.alias or (env_prefix + field_name).upper()
            section["settings"][alias] = values[field_name]

        result.append(section)

    if pretty:
        import json
        return json.dumps(result, indent=2)

    return result
