#!/bin/bash
python problems/manage.py makemigrations
python problems/manage.py migrate
python problems/manage.py runserver 0.0.0.0:8000