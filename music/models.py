from django.db import models

from common.models import AbstractBaseModel, AbstractMPTTBaseModel
from content.models import Event
from members.models import User


class InstrumentGroup(AbstractMPTTBaseModel):
    name = models.CharField(max_length=100, unique=True)

    @property
    def all_instruments(self):
        return self._get_all_instruments()

    def _get_all_instruments(self):
        """
        Retrieves all active instrument records that are a part of this group and its descendant groups.
        """
        descendants = self.get_descendants(include_self=True)
        descendant_pks = [descendant.pk for descendant in descendants if descendant.is_active]
        return Instrument.objects.filter(instrument_group__in=descendant_pks).exclude(is_active=False)


class Instrument(AbstractBaseModel):
    name = models.CharField(max_length=100, unique=True)
    instrument_group = models.ForeignKey(InstrumentGroup, related_name='instruments')
    users = models.ManyToManyField(User, related_name='instruments')


class Composer(AbstractBaseModel):
    pass


class MusicalWorkCategory(AbstractBaseModel):
    name = models.CharField(max_length=50, unique=True)


class MusicalWork(AbstractBaseModel):
    GRADE_CHOICES = (
        (1, 'I'),
        (2, 'II'),
        (3, 'III'),
        (4, 'IV'),
        (5, 'V'),
        (6, 'VI'),
    )

    library_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=500)
    composers = models.ManyToManyField(Composer, related_name='composed_works')
    arrangers = models.ManyToManyField(Composer, related_name='arranged_works')
    category = models.ForeignKey(MusicalWorkCategory, related_name='musical_works')
    grade = models.PositiveSmallIntegerField(null=True, blank=True, choices=GRADE_CHOICES)
    notes = models.TextField(blank=True, default='')


class Rehearsal(Event):
    pass


class Concert(Event):
    program_selections = models.ManyToManyField(MusicalWork, related_name='concerts')