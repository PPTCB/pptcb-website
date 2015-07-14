import os
import yaml

from django.conf import settings
from django.core.management import BaseCommand

from members.models import User
from music.models import Instrument, InstrumentGroup, MusicalWorkCategory, MusicalWork, Composer


class Command(BaseCommand):
    help = 'Seeds the database with data'

    def add_arguments(self, parser):
        parser.add_argument('--test', action='store_true', dest='test', default=False,
                            help='Use test data instead of real data')

    def handle(self, *args, **options):
        if options['test']:
            base_directory = os.path.join(settings.DATABASE_SEEDS_DIRECTORY, 'test')
        else:
            base_directory = os.path.join(settings.DATABASE_SEEDS_DIRECTORY, 'real')
        self.seed_instrument_groups(base_directory)
        self.seed_instruments(base_directory)
        self.seed_users(base_directory)
        self.seed_musical_works(base_directory)

    @classmethod
    def seed_users(cls, base_directory):
        users = cls._load_yaml_file(base_directory, 'user')
        instruments = {instrument.name : instrument for instrument in Instrument.objects.all()}
        for user in users:
            if 'superuser' in user and user['superuser']:
                user_object = User.objects.create_superuser(user['first_name'], user['last_name'], user['email'], user['password'])
            else:
                user_object = User.objects.create_user(user['first_name'], user['last_name'], user['email'], user['password'])
            if 'instruments' in user:
                for instrument in user['instruments']:
                    user_object.instruments.add(instruments[instrument['name']])

    @classmethod
    def seed_instrument_groups(cls, base_directory):
        instrument_groups = cls._load_yaml_file(base_directory, 'instrument_group')
        cnt = 1
        for group in instrument_groups:
            group_object = InstrumentGroup.objects.create(name=group['name'], concert_order=cnt)
            cnt += 1
            if 'children' in group:
                for child in group['children']:
                    InstrumentGroup.objects.create(name=child['name'], concert_order=cnt, parent=group_object)
                    cnt += 1

    @classmethod
    def seed_instruments(cls, base_directory):
        groups = {group.name : group for group in InstrumentGroup.objects.all()}
        instruments = cls._load_yaml_file(base_directory, 'instrument')
        cnt = 1
        for instrument in instruments:
            Instrument.objects.create(name=instrument['name'], instrument_group=groups[instrument['group']],
                                      concert_order=cnt)
            cnt += 1

    @classmethod
    def seed_musical_works(cls, base_directory):
        works = cls._load_yaml_file(base_directory, 'musical_work')
        for work in works:
            if 'notes' not in work:
                work['notes'] = ''
            if 'composers' not in work:
                work['composers'] = []
            if 'arrangers' not in work:
                work['arrangers'] = []
            category, created = MusicalWorkCategory.objects.get_or_create(name=work['category'])
            musical_work = MusicalWork.objects.create(library_id=work['library_id'], name=work['name'],
                                                      category=category, grade=work['grade'], notes=work['notes'])
            for type in ['composers', 'arrangers']:
                for person in work[type]:
                    if isinstance(person, dict):
                        composer, created = Composer.objects.get_or_create(**person)
                    else:
                        composer, created = Composer.objects.get_or_create(**Composer.name_from_string(person))
                    if type == 'composers':
                        musical_work.composers.add(composer)
                    else:
                        musical_work.arrangers.add(composer)


    @staticmethod
    def _load_yaml_file(base_directory, file_name):
        file_path = os.path.join(base_directory, file_name + '.yaml')

        with open(file_path, 'r') as fh:
            yaml_object = yaml.load(fh)

        return yaml_object