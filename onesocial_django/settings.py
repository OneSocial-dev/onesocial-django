import importlib

from django.conf import settings


REQUIRED_SETTINGS = [
    'ONESOCIAL_CLIENT_ID',
    'ONESOCIAL_CLIENT_SECRET',
]

DEFAULTS = {
    'ONESOCIAL_ERROR_URL': '/',
    'ONESOCIAL_VALIDATE_FUNC': 'onesocial_django.utils.default_validate',
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


def get_func(path):
    module_name, func_name = path.rsplit('.', maxsplit=1)
    module = importlib.import_module(module_name)
    func = getattr(module, func_name)
    return func
