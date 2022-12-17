# LEM
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/LemCommunity/lem/main.svg)](https://results.pre-commit.ci/latest/github/LemCommunity/lem/main) [![Coverage Status](https://coveralls.io/repos/github/LemCommunity/lem/badge.svg?branch=main)](https://coveralls.io/github/LemCommunity/lem?branch=main)

Social media for book lovers (similar to Goodreads)

# Getting started
## Installing EditorConfig
To maintain consistent coding style, we settled on [EditorConfig](https://editorconfig.org/). The installation process is different depending on your editor:
* PyCharm has support for EditorConfig out of the box
* VSCode [needs a plugin](https://marketplace.visualstudio.com/items?itemName=EditorConfig.EditorConfig)
* If you use another editor, reference to https://editorconfig.org/#pre-installed and https://editorconfig.org/#download
## Installing Poetry
LEM is using [Poetry](https://python-poetry.org/) as a package manager. Check out [its documentation](https://python-poetry.org/docs/#installation) to learn how to install it. Unless you know what you are doing, we recommend following the installation steps with the official installer.

After the installation process, ensure Poetry is installed correctly by typing
```
poetry --version
```

We are also using the official export plugin for Poetry. You can install it with
```
poetry self add poetry-plugin-export
```

## Installing Docker
To install Docker, head to [the official documentation](https://docs.docker.com/get-docker/). You can find instructions for your Operating System there. With Docker Desktop, you can start Docker conveniently from the tray.
Make sure Docker is up and running:
```
docker --version
```

## Running the project
Clone the repository (make sure you have git installed):
```
git clone https://github.com/LemCommunity/lem.git
cd lem
```
Install the dependencies (Poetry will create a virtual environment automatically for you)
```
poetry install --with dev
```
Enter the virtual environment that Poetry creates for you:
```
poetry shell
```

Now, install [pre-commit](https://pre-commit.com/) hooks by running:
```
pre-commit install
```
**Note:** Be sure you are in the same directory as `.pre-commit-config.yaml` file.

Build images and start containers. No worries, first run will take a lot of time. Docker has to download a lot of data, but it will store it in a cache for later retrieval.
```
docker-compose up --build -d
```
The `-d` flag runs the containers in the background so you can fire other commands from the same terminal.

If everything went smoothly without errors, the application should now be running.
You can access it at
```
http://localhost:8000/
```
If you see the 404 page, then everything is correct.

Consider creating a superuser to access the Django Admin panel
```
docker-compose run django python manage.py createsuperuser
```

## Docker Cheat Sheet
Stopping containers:
```
docker-compose stop
```
See logs for a particular service:
```
docker-compose logs <SERVICE_NAME>
e.g.
docker-compose logs django
```

## How to install packages
We are using Poetry for installing dependencies and then generating with it standard Python requirements.txt file for Docker.

You can install a Python package from PyPI by typing:
```
poetry add <PACKAGE_NAME>
```

Use the command below to generate the requirements file
```
poetry export --with production --with dev -f requirements.txt --output requirements.txt
```
