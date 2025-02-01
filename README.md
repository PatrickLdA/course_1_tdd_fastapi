# Test-Driven Development with Docker and FastAPI

Reference code: https://github.com/testdrivenio/fastapi-tdd-docker

## Getting Started
Starlette is the Asynchronous Server Gateway Interface (ASGI)

OpenAPI is a standard of APIs

Swagger is a graphical interface for endpoints

## FastAPI dependencies

Is a way to create and maintain common structures to several parts of code that have dependencies themselves

## Postgres setup

`source env/bin/activate` activates the venv

The file `entrypoint.sh` of a container is the first executable of it

Tortoise ORM is a Object Relational Mapper (ORM) that allows a interaction with databases

`docker-compose down -v` remove all Dockers related to the project

Aerich is a migration tool for TortoiseORM

## Pytest setup
Fixtures are data/object sets common to one or more tests

## Commands

```sh
# normal run
$ docker-compose exec web python -m pytest

# disable warnings
$ docker-compose exec web python -m pytest -p no:warnings

# run only the last failed tests
$ docker-compose exec web python -m pytest --lf

# run only the tests with names that match the string expression
$ docker-compose exec web python -m pytest -k "summary and not test_read_summary"

# stop the test session after the first failure
$ docker-compose exec web python -m pytest -x

# enter PDB after first failure then end the test session
$ docker-compose exec web python -m pytest -x --pdb

# stop the test run after two failures
$ docker-compose exec web python -m pytest --maxfail=2

# show local variables in tracebacks
$ docker-compose exec web python -m pytest -l

# list the 2 slowest tests
$ docker-compose exec web python -m pytest --durations=2
```

## Project files

```
├── .gitignore
├── docker-compose.yml
└── project
    ├── .dockerignore
    ├── Dockerfile
    └── app
        ├── __init__.py
        └── main.py: FastAPI endpoint declaration file
        ├── config.py: Logger configuration file
    │   └── models
    │       ├── __init__.py
    │       └── tortoise.py
    ├── db
    │   ├── Dockerfile
    │   └── create.sql
    ├── entrypoint.sh
    └── requirements.txt
```

## Heroku Deployment

After install Heroku CLI and create an account:

Logs in Heroku Container Registry: `heroku container:login`

Push the image to the registry: `docker push registry.heroku.com/<APP_NAME>/web:latest`

Release the image: `heroku container:release web --app <APP_NAME>`


## Continuous Integration

Build and tag the image: `docker build -f project/Dockerfile.prod -t ghcr.io/<USERNAME>/<REPOSITORY_NAME>/summarizer:latest ./project`

Next, using your personal access token, authenticate to GitHub Packages with Docker: `docker login ghcr.io -u <USERNAME> -p <TOKEN>`

Push the image to the Container registry on GitHub Packages: `docker push ghcr.io/<USERNAME>/<REPOSITORY_NAME>/summarizer:latest`

![Continuous Integration and Delivery](https://github.com/patricklda/course_1_tdd_fastapi/workflows/Continuous%20Integration%20and%20Delivery/badge.svg?branch=main)

## Alias

To save some precious keystrokes, let's create an alias for the docker-compose command -- dc.

Simply add the following line to your .bashrc file:

```bash
alias dc='docker-compose'
```

Save the file, then execute it:

```bash
$ source ~/.bashrc
```

### Common Commands

Build the images: `$ docker-compose build`

Run the containers: `$ docker-compose up -d`

Apply the migrations: `$ docker-compose exec web aerich upgrade`. Prefer just to apply the latest changes to the database, without the migrations?
`$ docker-compose exec web python app/db.py`

Run the tests: `$ docker-compose exec web python -m pytest`

Run the tests with coverage: `$ docker-compose exec web python -m pytest --cov="."`

Lint: `$ docker-compose exec web flake8 .`

Run Black and isort with check options:

```bash
$ docker-compose exec web black . --check
$ docker-compose exec web isort . --check-only
```

Make code changes with Black and isort:

```bash
$ docker-compose exec web black .
$ docker-compose exec web isort .
```

### Other Commands

To stop the containers: `$ docker-compose stop`

To bring down the containers: `$ docker-compose down`

Want to force a build? `$ docker-compose build --no-cache`

Remove images: `$ docker rmi $(docker images -q)`

### Postgres

Want to access the database via psql? `$ docker-compose exec web-db psql -U postgres`

Then, you can connect to the database and run SQL queries. For example:

```bash
# \c web_dev
# select * from textsummary;
```

