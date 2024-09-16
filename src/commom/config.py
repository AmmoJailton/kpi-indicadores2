import inspect
import logging
import os
import sys

from google.oauth2 import service_account

LOG_LEVELS = {
    "notset": logging.NOTSET,
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}


def factory(env):
    classes_tuple = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    for current_class in classes_tuple:
        if hasattr(current_class[1], "ENV"):
            if env == current_class[1].ENV:
                return current_class[1]
    return DevConfig


class BaseConfig(object):
    LOG_LEVEL = LOG_LEVELS.get(str.lower(os.environ.get("LOG_LEVEL", "info")))
    # GOOGLE_CREDENTIALS_FILEPATH = "/tmp/gcloud-api.json"
    # os.environ["GCP_CREDENTIALS_SECRET"] = GOOGLE_CREDENTIALS_FILEPATH
    credentials = service_account.Credentials.from_service_account_file(os.environ["GCP_CREDENTIALS_SECRET"])
    # credentials = service_account.Credentials.from_service_account_info()
    scope_credentials = credentials.with_scopes(["https://www.googleapis.com/auth/cloud-platform"])


class ProdConfig(BaseConfig):
    """Production configuration."""

    ENV = "prod"


class DevConfig(BaseConfig):
    """Development configuration."""

    ENV = "dev"


config = factory(os.getenv("ENV"))
