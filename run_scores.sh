#!/bin/bash
python scores/manage.py makemigrations
python scores/manage.py migrate
python scores/manage.py runserver 0.0.0.0:8000