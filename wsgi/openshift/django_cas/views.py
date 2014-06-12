"""CAS login/logout replacement views"""

from urllib import urlencode
from urlparse import urljoin
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib import messages
import logging
from django.contrib.auth import login


__all__ = ['login', 'logout']


def _service_url(request, redirect_to):
    """Generates application service URL for CAS"""

    protocol = ('http://', 'https://')[request.is_secure()]
    host = request.get_host()
    service = protocol + host + '/login'
    if redirect_to:
        if '?' in service:
            service += '&'
        else:
            service += '?'
        service += urlencode({REDIRECT_FIELD_NAME: redirect_to})
    return service


def _redirect_url(request):
    """Redirects to referring page, or CAS_REDIRECT_URL if no referrer is
    set.
    """

    next = request.GET.get(REDIRECT_FIELD_NAME)
    if not next:
        if settings.CAS_IGNORE_REFERER:
            next = settings.CAS_REDIRECT_URL
        else:
            next = request.META.get('HTTP_REFERER', settings.CAS_REDIRECT_URL)
        prefix = (('http://', 'https://')[request.is_secure()] +
                  request.get_host())
        if next.startswith(prefix):
            next = next[len(prefix):]
    return next


def _login_url(service):
    """Generates CAS login URL"""

    params = {'service': service}
    if settings.CAS_EXTRA_LOGIN_PARAMS:
        params.update(settings.CAS_EXTRA_LOGIN_PARAMS)
    return urljoin(settings.CAS_SERVER_URL, 'login') + '?' + urlencode(params)


def _logout_url(request, next_page=''):
    """Generates CAS logout URL"""

    url = urljoin(settings.CAS_SERVER_URL, 'logout')
    if next_page:
        protocol = ('http://', 'https://')[request.is_secure()]
        host = request.get_host()
        url += '?' + urlencode({'url': protocol + host})
    return url


def login(request, next_page=None):
    """Forwards to CAS login URL or verifies CAS ticket"""
    if not next_page:
        next_page = _redirect_url(request)
    if request.user.is_authenticated():
        message = "You are logged in as %s." % request.user.username
        messages.success(request, message)
        if (settings.DEBUG):
            return HttpResponseRedirect("http://kalandar-oregonstate.rhcloud.com/done")
        else:
            return HttpResponseRedirect("http://localhost:8000/done")
    ticket = request.GET.get('ticket')
    # service = _service_url(request, next_page)
    service = 'http://kalandar-oregonstate.rhcloud.com/login'
    if ticket is not None:
        from django.contrib import auth
        user = auth.authenticate(ticket=ticket, service=service, request=request)
        if user is not None:
            auth.login(request, user)
            # Redirect to a success page.
            if (settings.DEBUG):
                return HttpResponseRedirect('http://kalandar-oregonstate.rhcloud.com/done')
            else:
                return HttpResponseRedirect('http://localhost:8000/done')
        else:
            error = "<h1>Error</h1><p>Could not find user.</p>"
            return HttpResponseForbidden(error)
    else:
        return HttpResponseRedirect(_login_url(service))


def logout(request, next_page="http://kalandar-oregonstate.rhcloud.com/"):
    """Redirects to CAS logout page"""

    from django.contrib.auth import logout

    logout(request)
    if not next_page:
        next_page = _redirect_url(request)
    if settings.CAS_LOGOUT_COMPLETELY:
        return HttpResponseRedirect(_logout_url(request, next_page))
    else:
        return HttpResponseRedirect(next_page)
