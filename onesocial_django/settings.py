from django.conf import settings
from django.urls import reverse_lazy


REQUIRED_SETTINGS = [
    'ONESOCIAL_CLIENT_ID',
    'ONESOCIAL_CLIENT_SECRET',
]

DEFAULTS = {
    'ONESOCIAL_ERROR_URL': '/',
}


def _raise_required_error():
    raise RuntimeError(
        "Please set {} in the settings".format(', '.join(REQUIRED_SETTINGS)))


def get_setting(name):
    if hasattr(settings, name):
        return getattr(settings, name)

    if name in REQUIRED_SETTINGS:
        _raise_required_error()
    elif name in DEFAULTS:
        return DEFAULTS[name]
    else:
        return None
