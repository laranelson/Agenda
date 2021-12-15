import environ

from agenda.settings.base import *

env = environ.Env()

DEBUG = env.bool("DEBUG", False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
