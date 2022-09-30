from django.contrib import admin
from events.models import Event


@admin.register(Event)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'attendees', 'event_date', 'notes', 'status', 'customer', 'user')


# admin.site.register(Event)
