from django.test import TestCase

from .models import InstrumentGroup, Instrument, Composer, MusicalWork, MusicalWorkCategory


class InstrumentGroupTests(TestCase):

    def test_get_all_instruments(self):
        instrument_group_1 = InstrumentGroup.objects.create(name='Brass')
        instrument_group_2 = InstrumentGroup.objects.create(name='Low Brass', parent=instrument_group_1)
        Instrument.objects.create(name='Trumpet', instrument_group=instrument_group_1)
        Instrument.objects.create(name='Tuba', instrument_group=instrument_group_2)
        self.assertEqual(instrument_group_1.all_instruments.count(), 2)


class MusicalWorkTests(TestCase):

    def test_composers_display_list_no_composer(self):
        test_category = MusicalWorkCategory.objects.create(name='Classical')
        test_musical_work = MusicalWork.objects.create(library_id=102, name='Symphony No. 5', grade=6,
                                                       category=test_category)
        self.assertEqual(test_musical_work.composers_display_list, '')

    def test_composers_display_list_one_composer(self):
        test_category = MusicalWorkCategory.objects.create(name='Classical')
        test_musical_work = MusicalWork.objects.create(library_id=102, name='Symphony No. 5', grade=6,
                                                       category=test_category)
        test_composer = Composer.objects.create(first_name='Test', last_name='Composer')
        test_musical_work.composers.add(test_composer)
        self.assertEqual(test_musical_work.composers_display_list, 'Test Composer')

    def test_composers_display_list_multiple_composers(self):
        test_category = MusicalWorkCategory.objects.create(name='Classical')
        test_musical_work = MusicalWork.objects.create(library_id=102, name='Symphony No. 5', grade=6,
                                                       category=test_category)
        test_composer1 = Composer.objects.create(first_name='Test', last_name='Composer')
        test_composer2 = Composer.objects.create(first_name='John', last_name='Doe')
        test_musical_work.composers.add(test_composer1)
        test_musical_work.composers.add(test_composer2)
        self.assertEqual(test_musical_work.composers_display_list, 'Composer, Doe')