#!/bin/bash

export DJANGO_SETTINGS_MODULE=inventory.settings
cd /home/opsadmin/inventory.owensboro.kyschools.us
source ./venv/bin/activate
python ./inventory/manage.py ${*}
