from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from schedules import views

urlpatterns = patterns('',
    # ex: /schedules/
    url(r'^$', views.render_schedule, name='main'),
    # url(r'^(?P<username>\w+)', 'schedules.views.render_schedule')

    # ex: /schedules/5/
    # url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    # ex: /schedules/5/results/
    # url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
    # ex: /schedules/5/vote/
    # url(r'^(?P<schedule_id>\d+)/vote/$', views.vote, name='vote'),
)

urlpatterns += staticfiles_urlpatterns()