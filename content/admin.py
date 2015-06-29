from django.contrib import admin

from .models import Address, Location, Event

admin.site.register(Address)
admin.site.register(Location)
admin.site.register(Event)