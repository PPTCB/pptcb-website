from django.test import TestCase

from .models import InstrumentGroup, Instrument


class InstrumentGroupTests(TestCase):

    def test_get_all_instruments(self):
        instrument_group_1 = InstrumentGroup.objects.create(name='Brass')
        instrument_group_2 = InstrumentGroup.objects.create(name='Low Brass', parent=instrument_group_1)
        Instrument.objects.create(name='Trumpet', instrument_group=instrument_group_1)
        Instrument.objects.create(name='Tuba', instrument_group=instrument_group_2)
        self.assertEqual(instrument_group_1.all_instruments.count(), 2)