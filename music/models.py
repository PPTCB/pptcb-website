from django.db import models

from common.models import AbstractBaseModel


class InstrumentGroup(AbstractBaseModel):
    pass


class Instrument(AbstractBaseModel):
    instrument_group = models.ForeignKey(InstrumentGroup)