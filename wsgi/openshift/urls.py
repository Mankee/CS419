from django.conf.urls import patterns, include, url

from django.contrib import admin
from schedules import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'schedules.views.index'),
    url(r'^schedule/', include('schedules.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),

    url(r'^signup-email/', 'schedules.views.signup_email'),
    url(r'^email-sent/', 'schedules.views.validation_sent'),
    url(r'^done/$', 'schedules.views.done', name='done'),

    # CAS URLS for logging users in and out of the web application (temporarly disabled)
    url(r'^login/$', 'django_cas.views.login'),
    url(r'^logout/$', 'django_cas.views.logout'),

)
