#!/bin/bash

export DJANGO_SETTINGS_MODULE=inventory.settings
source ./venv/bin/activate
python ./inventory/manage.py ${*}
