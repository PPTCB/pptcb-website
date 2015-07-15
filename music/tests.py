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

    def test_composers_short_display_no_composer(self):
        test_category = MusicalWorkCategory.objects.create(name='Classical')
        test_musical_work = MusicalWork.objects.create(library_id=102, name='Symphony No. 5', grade=6,
                                                       category=test_category)
        self.assertEqual(test_musical_work.composers_short_display, '')

    def test_composers_short_display_one_composer(self):
        test_category = MusicalWorkCategory.objects.create(name='Classical')
        test_musical_work = MusicalWork.objects.create(library_id=102, name='Symphony No. 5', grade=6,
                                                       category=test_category)
        test_composer = Composer.objects.create(first_name='Test', last_name='Composer')
        test_musical_work.composers.add(test_composer)
        self.assertEqual(test_musical_work.composers_short_display, 'Test Composer')

    def test_composers_short_display_multiple_composers(self):
        test_category = MusicalWorkCategory.objects.create(name='Classical')
        test_musical_work = MusicalWork.objects.create(library_id=102, name='Symphony No. 5', grade=6,
                                                       category=test_category)
        test_composer1 = Composer.objects.create(first_name='Test', last_name='Composer')
        test_composer2 = Composer.objects.create(first_name='John', last_name='Doe')
        test_musical_work.composers.add(test_composer1)
        test_musical_work.composers.add(test_composer2)
        self.assertEqual(test_musical_work.composers_short_display, 'Composer, Doe')


class ComposerTests(TestCase):

    def test_name_from_string_one_name(self):
        test_name = 'Beethoven'
        name_dict = Composer.name_from_string(test_name)
        self.assertNotIn('first_name', name_dict)
        self.assertNotIn('middle_name', name_dict)
        self.assertIn('last_name', name_dict)
        self.assertEqual(name_dict['last_name'], test_name)

    def test_name_from_string_two_names(self):
        test_name = 'George Harrison'
        name_dict = Composer.name_from_string(test_name)
        self.assertIn('first_name', name_dict)
        self.assertNotIn('middle_name', name_dict)
        self.assertIn('last_name', name_dict)
        self.assertEqual(name_dict['first_name'], 'George')
        self.assertEqual(name_dict['last_name'], 'Harrison')

    def test_name_from_string_three_names(self):
        test_name = 'Johann Sebastian Bach'
        name_dict = Composer.name_from_string(test_name)
        self.assertIn('first_name', name_dict)
        self.assertIn('middle_name', name_dict)
        self.assertIn('last_name', name_dict)
        self.assertEqual(name_dict['first_name'], 'Johann')
        self.assertEqual(name_dict['middle_name'], 'Sebastian')
        self.assertEqual(name_dict['last_name'], 'Bach')