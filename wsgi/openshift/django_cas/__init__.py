"""Django CAS 1.0/2.0 authentication backend"""

from django.conf import settings

__all__ = []

_DEFAULTS = {
    'CAS_ADMIN_PREFIX': None,
    'CAS_EXTRA_LOGIN_PARAMS': None,
    'CAS_IGNORE_REFERER': True,
    'CAS_LOGOUT_COMPLETELY': True,
    'CAS_REDIRECT_URL': 'http://kalandar-oregonstate.rhcloud.com/',
    'CAS_RETRY_LOGIN': True,
    'CAS_SERVER_URL': 'https://login.oregonstate.edu/cas/',
    'CAS_VERSION': '2',
}

for key, value in _DEFAULTS.iteritems():
    try:
        getattr(settings, key)
    except AttributeError:
        setattr(settings, key, value)
    # Suppress errors from DJANGO_SETTINGS_MODULE not being set
    except ImportError:
        pass
