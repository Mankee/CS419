from django.contrib import admin
from schedules.models import Event, Faculty

# https://docs.djangoproject.com/en/1.6/intro/tutorial02/

# adds event objects to each calendar in an inline fashion

class EventInline(admin.StackedInline):
    model = Event
    extra = 1

class FacultyAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Faculty Personnel', {'fields': ['department']}),
    ]

    inlines = [EventInline]

    list_display = ( 'first_initial', 'department')

admin.site.register(Faculty, FacultyAdmin)