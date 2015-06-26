#!/bin/bash
rm db.sqlite
rm content/migrations/0001_initial.py
rm members/migrations/0001_initial.py
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser