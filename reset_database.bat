@ECHO off

del "db.sqlite3"
del "content\migrations\0001_initial.py"
del "members\migrations\0001_initial.py"
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser