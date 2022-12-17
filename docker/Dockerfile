ARG PYTHON_VERSION=3.10-slim-bullseye

# define an alias for the specfic python version used in this file.
FROM python:${PYTHON_VERSION} as python

# Python build stage
FROM python as python-build-stage

ARG APP_HOME=/src
WORKDIR ${APP_HOME}

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt .

# Create Python Dependency and Sub-Dependency Wheels.
RUN pip wheel --wheel-dir /usr/src/app/wheels  \
  -r requirements.txt


# Python 'run' stage
FROM python as python-run-stage

ARG BUILD_ENVIRONMENT=local
ARG APP_HOME=/src
WORKDIR ${APP_HOME}

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
  # psycopg2 dependencies
  libpq-dev \
  # Translations dependencies
  gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# All absolute dir copies ignore workdir instruction. All relative dir copies are wrt to the workdir instruction
# copy python dependency wheels from python-build-stage
COPY --from=python-build-stage /usr/src/app/wheels  /wheels/

# use wheels to install python dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
	&& rm -rf /wheels/

COPY ./docker/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//g' /entrypoint.sh && chmod +x /entrypoint.sh

COPY ./docker/start_scripts/django.sh /start-django.sh
RUN sed -i 's/\r$//g' /start-django.sh && chmod +x /start-django.sh

COPY ./docker/start_scripts/celery_worker.sh /start-celeryworker.sh
RUN sed -i 's/\r$//g' /start-celeryworker.sh && chmod +x /start-celeryworker.sh

COPY ./docker/start_scripts/celery_beat.sh /start-celerybeat.sh
RUN sed -i 's/\r$//g' /start-celerybeat.sh && chmod +x /start-celerybeat.sh

COPY ./docker/start_scripts/celery_flower.sh /start-flower.sh
RUN sed -i 's/\r$//g' /start-flower.sh && chmod +x /start-flower.sh

# copy application code to WORKDIR
COPY . ${APP_HOME}

ENTRYPOINT ["/entrypoint.sh"]
