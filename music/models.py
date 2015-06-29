from django.db import models

from common.models import AbstractBaseModel, AbstractMPTTBaseModel
from content.models import Event
from members.models import User


class InstrumentGroup(AbstractMPTTBaseModel):
    name = models.CharField(max_length=100, unique=True)
    concert_order = models.PositiveIntegerField(unique=True, null=True, blank=True)

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

    def __unicode__(self):
        return self.name


class Instrument(AbstractBaseModel):
    name = models.CharField(max_length=100, unique=True)
    instrument_group = models.ForeignKey(InstrumentGroup, related_name='instruments')
    users = models.ManyToManyField(User, related_name='instruments')
    concert_order = models.PositiveIntegerField(unique=True, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Composer(AbstractBaseModel):
    first_name = models.CharField(max_length=30, blank=True, default='')
    middle_name = models.CharField(max_length=30, blank=True, default='')
    last_name = models.CharField(max_length=30)

    @property
    def full_name(self):
        names = [self.first_name, self.middle_name, self.last_name]
        names = [name.strip() for name in names if name.strip() != '']
        return ' '.join(names)

    def __unicode__(self):
        return self.full_name

    class Meta:
        unique_together = ('first_name', 'middle_name', 'last_name')


class MusicalWorkCategory(AbstractBaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'musical work categories'


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
    musical_works = models.ManyToManyField(MusicalWork, through='RehearsalPlan', related_name='rehearsals')
    notes = models.TextField(blank=True, default='')


class ConcertType(AbstractBaseModel):
    name = models.CharField(max_length=50, unique=True)


class Concert(Event):
    musical_works = models.ManyToManyField(MusicalWork, through='ConcertProgram', related_name='concerts')
    type = models.ForeignKey(ConcertType, related_name='concerts')
    attendance_cost = models.DecimalField(null=True, max_digits=5, decimal_places=2)


class RehearsalPlan(models.Model):
    rehearsal = models.ForeignKey(Rehearsal)
    musical_work = models.ForeignKey(MusicalWork)
    notes = models.TextField(blank=True, default='')
    order = models.SmallIntegerField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)

    class Meta:
        unique_together = ('rehearsal', 'order')


class ConcertProgram(models.Model):
    concert = models.ForeignKey(Concert)
    musical_work = models.ForeignKey(MusicalWork)
    notes = models.TextField(blank=True, default='')
    order = models.SmallIntegerField(null=True, blank=True)

    class Meta:
        unique_together = (('concert', 'musical_work'), ('concert', 'order'))