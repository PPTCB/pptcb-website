from django.db import models
from django.utils.functional import cached_property

from core.models import AbstractBaseModel, AbstractMPTTBaseModel
from content.models import Event, Page
from members.models import User


class InstrumentGroup(AbstractMPTTBaseModel):
    name = models.CharField(max_length=100, unique=True)
    concert_order = models.PositiveIntegerField(unique=True, null=True, blank=True)

    @cached_property
    def all_instruments(self):
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

    @staticmethod
    def name_from_string(name):
        names = name.strip().split()
        if len(names) == 0:
            return dict()
        elif len(names) == 1:
            return {'last_name': names[0]}
        elif len(names) == 2:
            return {'first_name': names[0], 'last_name': names[1]}
        else:
            return {'first_name': names[0], 'middle_name': ' '.join(names[1:-1]) , 'last_name': names[-1]}

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

    @property
    def composers_display_list(self):
        return self._person_display_list(self.composers)

    @property
    def arrangers_display_list(self):
        return self._person_display_list(self.arrangers)

    @staticmethod
    def _person_display_list(collection):
        if collection.count() > 1:
            return ', '.join([person.last_name for person in collection.all()])
        elif collection.count() == 1:
            return collection.all()[0].full_name
        else:
            return ''


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


class ConcertPage(Page):
    concert = models.OneToOneField(Concert, related_name='page')

    def pre_save(self, is_new):
        if not self.title or self.title.strip() == '':
            self.title = self.concert.name
        super(ConcertPage, self).pre_save(is_new)