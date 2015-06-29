from django.db import models

from common.models import AbstractBaseModel, AbstractMPTTBaseModel
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