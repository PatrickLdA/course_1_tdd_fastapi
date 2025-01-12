# Test-Driven Development with Docker and FastAPI

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