from .integrations import *

class Config:
    INTEGRATIONS = {
        "honeybadger": {
            "integration_class": HoneyBadger,
        },
        "github": {
            "integration_class": Github,
        },
        "railway": {
            "integration_class": Railway,
        }
    }
