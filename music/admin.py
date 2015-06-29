from django.contrib import admin

from .models import Instrument, InstrumentGroup, Composer, MusicalWork, MusicalWorkCategory, Rehearsal, Concert,\
    ConcertType

admin.site.register(Instrument)
admin.site.register(InstrumentGroup)
admin.site.register(Composer)
admin.site.register(MusicalWork)
admin.site.register(MusicalWorkCategory)
admin.site.register(Rehearsal)
admin.site.register(Concert)
admin.site.register(ConcertType)