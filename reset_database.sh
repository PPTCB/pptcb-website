#!/bin/bash
rm db.sqlite3
rm content/migrations/0001_initial.py
rm members/migrations/0001_initial.py
rm music/migrations/0001_initial.py
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser