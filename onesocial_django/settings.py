"""
Этот модуль предоставляет вспомогательные функции, с помощью которых пакет
может работать с настройками проекта.
"""
import importlib

from django.conf import settings


# Обязательные настройки
REQUIRED_SETTINGS = [
    'ONESOCIAL_CLIENT_ID',
    'ONESOCIAL_CLIENT_SECRET',
]

# Дефолты для необязательных настроек
DEFAULTS = {
    'ONESOCIAL_ERROR_URL': '/',
    'ONESOCIAL_LOGGED_IN_URL': '/',
    'ONESOCIAL_VALIDATE_FUNC': 'onesocial_django.utils.default_validate',
    'ONESOCIAL_REGISTER_FUNC': 'onesocial_django.utils.default_register',
}


def _raise_required_error():
    raise RuntimeError(
        "Please set {} in the settings".format(', '.join(REQUIRED_SETTINGS)))


def get_setting(name):
    """
    Возвращает значение для настройки, или дефолт, если он задан, или None.
    Если настройка обязательная, но она не задана - выбрасывает исключение.
    """
    if hasattr(settings, name):
        return getattr(settings, name)

    if name in REQUIRED_SETTINGS:
        _raise_required_error()
    elif name in DEFAULTS:
        return DEFAULTS[name]
    else:
        return None


def get_func(path):
    """
    Возвращает объект функции по ее пути. Например 'onesocial_django.utils.default_validate'.
    """
    module_name, func_name = path.rsplit('.', maxsplit=1)
    module = importlib.import_module(module_name)
    func = getattr(module, func_name)
    return func
