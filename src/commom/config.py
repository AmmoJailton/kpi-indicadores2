import inspect
import os
import sys

from google.oauth2 import service_account

from commom.logger import get_log_level


def factory(env):
    classes_tuple = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    for current_class in classes_tuple:
        if hasattr(current_class[1], "ENV"):
            if env == current_class[1].ENV:
                return current_class[1]
    return DevConfig


class BaseConfig(object):
    LOG_LEVEL = get_log_level()
    GOOGLE_CREDENTIALS_FILEPATH = "/tmp/gcloud-api.json"
    credentials = service_account.Credentials.from_service_account_file(GOOGLE_CREDENTIALS_FILEPATH)
    scope_credentials = credentials.with_scopes(["https://www.googleapis.com/auth/cloud-platform"])


class ProdConfig(BaseConfig):
    """Production configuration."""

    ENV = "prod"


class DevConfig(BaseConfig):
    """Development configuration."""

    ENV = "dev"


config = factory(os.getenv("ENV"))
