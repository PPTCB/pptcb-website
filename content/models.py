from django.db import models

from common.intl import states
from common.models import AbstractBaseModel


class Address(AbstractBaseModel):
    STATE_CHOICES = (
        ('US', states.us_states_abbr),
        ('US Territories', states.us_territories_abbr),
        ('Canada', states.canada_provinces_abbr),
    )

    street_line_1 = models.CharField(max_length=255)
    street_line_2 = models.CharField(max_length=255, blank=True, default='')
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    postal_code = models.CharField(max_length=15)

    def __unicode__(self):
        if self.street_line_2:
            return "%s, %s, %s, %s %s" % (self.street_line_1, self.street_line_2, self.city, self.state, self.postal_code)
        else:
            return "%s, %s, %s %s" % (self.street_line_1, self.city, self.state, self.postal_code)

    class Meta:
        unique_together = ('street_line_1', 'street_line_2', 'city', 'state')
        verbose_name_plural = 'addresses'


class Location(AbstractBaseModel):
    name = models.CharField(max_length=255)
    address = models.ForeignKey(Address)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.address)

    class Meta:
        unique_together = ('name', 'address')


class Event(AbstractBaseModel):
    name = models.CharField(max_length=255)
    location = models.ForeignKey(Location)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.name