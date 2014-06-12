from django.contrib.auth.models import User
from django.db import models
from oauth2client.django_orm import FlowField, CredentialsField

# Django model field types
# https://docs.djangoproject.com/en/1.6/ref/models/fields/
from django.forms import ModelForm


class Faculty(models.Model):
    title = models.CharField('Title', max_length=30)
    first_initial = models.CharField('Initial', max_length=2)
    department = models.CharField('Department', max_length=100)
    django_user = models.ForeignKey(User, blank=True)

    def __unicode__(self):
        return self.first_initial + ' ' + self.last_name


class Event(models.Model):
    start_time = models.DateTimeField('Start Time')
    end_time = models.DateTimeField('End Time')
    description = models.CharField('Description', max_length=200, default='Busy')
    is_event_viewable = models.BooleanField('Publicly Viewable', default=True)
    faculty_user = models.ForeignKey(Faculty)

    def __unicode__(self):
        return self.description


class FlowModel(models.Model):
    id = models.ForeignKey(User, primary_key=True)
    flow = FlowField()


class CredentialsModel(models.Model):
    id = models.ForeignKey(User, primary_key=True)
    credential = CredentialsField()