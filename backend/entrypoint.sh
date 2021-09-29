#!/bin/sh
python manage.py makemigrations
python manage.py makemigrations api
python manage.py migrate
# echo 'yes' | python manage.py collectstatic
exec "$@"