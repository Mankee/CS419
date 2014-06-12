import logging
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django_cas.views import _service_url, _login_url
from models import CredentialsModel, Event
from django.contrib.auth import logout as auth_logout, login
import settings


def index(request):
    # Obtain the context from the HTTP request.
    context = RequestContext(request)

    # Query the database for a list of ALL events stored per Calendar.
    all_events = Event.objects.all()
    context_dict = {'Events': all_events}

    # Render the response and send it back!
    return render_to_response('schedules/index.html', context_dict, context)

# @login_required()
def render_schedule(request, next_page=None, required=True):
    if request.user.is_authenticated():
        # Query the database for a list of ALL events stored per Calendar.
        all_events = Event.objects.all()
        data = {'Events': all_events}
        return render_to_response('schedules/main.html', data)
    else:
        logging.error(
            'redirecting to login from render_schedule... could not authenticate user ' + request.user.username)
        service = _service_url(request, next_page)
        return HttpResponseRedirect(_login_url(service))

# @login_required
def done(request):
    """Login complete view, displays user data"""
    return render_to_response('schedules/done.html', {'user': request.user},
                              RequestContext(request))

def logout(request):
    """Logs out user"""
    auth_logout(request)
    return render_to_response('schedules/home.html', {}, RequestContext(request))


def home(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        return redirect('done')
    return render_to_response('schedules/home.html', {
        'plus_id': getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None)
    }, RequestContext(request))

def signup_email(request):
    return render_to_response('schedules/email_signup.html', {}, RequestContext(request))


def validation_sent(request):
    return render_to_response('schedules/validation_sent.html', {
        'email': request.session.get('email_validation_address')
    }, RequestContext(request))


def require_email(request):
    if request.method == 'POST':
        request.session['saved_email'] = request.POST.get('email')
        backend = request.session['partial_pipeline']['backend']
        return redirect('social:complete', backend=backend)
    return render_to_response('schedules/email.html', RequestContext(request))