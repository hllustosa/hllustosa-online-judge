#!/bin/bash
python users/manage.py makemigrations
python users/manage.py migrate
python users/manage.py createsuperuser --noinput
python users/manage.py runserver 0.0.0.0:8000