import os
import yaml

from django.conf import settings
from django.core.management import BaseCommand

from members.models import User


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
        self.seed_users(base_directory)

    @classmethod
    def seed_users(cls, base_directory):
        users = cls._load_yaml_file(base_directory, 'user')
        for user in users:
            if 'superuser' in user and user['superuser']:
                User.objects.create_superuser(user['first_name'], user['last_name'], user['email'], user['password'])
            else:
                User.objects.create_user(user['first_name'], user['last_name'], user['email'], user['password'])

    @staticmethod
    def _load_yaml_file(base_directory, file_name):
        file_path = os.path.join(base_directory, file_name + '.yaml')

        with open(file_path, 'r') as fh:
            yaml_object = yaml.load(fh)

        return yaml_object