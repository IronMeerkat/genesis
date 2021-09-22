#!/bin/sh
echo 'yes' | python manage.py collectstatic
python manage.py makemigrations
python manage.py migrate
exec "$@"