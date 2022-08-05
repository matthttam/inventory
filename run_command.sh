#!/bin/bash

export DJANGO_SETTINGS_MODULE=inventory.settings
./inventory/manage.py ${*}
