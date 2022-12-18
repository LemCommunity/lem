#!/bin/bash

set -o errexit
set -o nounset


rm -f './celerybeat.pid'
celery -A backend.config.celery beat -l INFO
