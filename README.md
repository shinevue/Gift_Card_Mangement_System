<div align="center">
<h1>GCManager💰💸</h1>
<p>
A Gift Card Management System
</p>
<a href="https://www.python.org/">
<img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg">
</a>
<a href="https://lbesson.mit-license.org/">
<img src="https://img.shields.io/badge/License-MIT-blue.svg">
</a>
<a href="https://github.com/psf/black">
<img src="https://img.shields.io/badge/code%20style-black-000000.svg">
</a>
<a href="https://codecov.io/gh/vishaltanwar96/GCManager">
<img src="https://codecov.io/gh/vishaltanwar96/GCManager/branch/main/graph/badge.svg?token=MBJVZ9502A"/>
</a>
<img src="https://github.com/vishaltanwar96/GCManager/actions/workflows/ci.yml/badge.svg"/>
<img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/vishaltanwar96/GCManager">
</div>

## A little about the system
* The system is built with [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) and follows [Test Driven Development](https://rubikscode.net/2021/05/24/test-driven-development-tdd-with-python/).
* It heavily uses design patterns like [Dependency Injection](https://en.wikipedia.org/wiki/Dependency_injection), [Strategy](https://en.wikipedia.org/wiki/Strategy_pattern) and [Command](https://en.wikipedia.org/wiki/Command_pattern).
* We aim for 100% [code coverage](https://www.atlassian.com/continuous-delivery/software-testing/code-coverage).
* Mocks are the preffered way of [mocking](https://microsoft.github.io/code-with-engineering-playbook/automated-testing/unit-testing/mocking/) dependencies in unit tests as we want to test our components in a controlled environment.

## Project Structure
```
.
|-- LICENSE
|-- README.md
|-- codecov.yml
|-- gcmanager
|   |-- __init__.py
|   |-- app.py                 <- Creates the WSGI App with all the settings that's intended to be served.
|   |-- dependencies.py        <- Builds all the dependencies and adds them to the dependency container, ready to be consumed.
|   |-- domain.py              <- All the domain models AKA entities in Clean Architecture are located here.
|   |-- enums.py
|   |-- exceptions.py          <- All the exceptions used within the app are located here.
|   |-- repositories.py        <- All the components that communicate with some sort of external system are located here.
|   |-- routes.py              <- All the API routes defined in the app are present here.
|   |-- serializers.py         <- Models used for (de)serialization of data.
|   |-- settings.py            <- Settings used by the app, all sorts of configuration, secrets and whatnot shall go here.
|   |-- usecases.py            <- The core business logic of the app should be present here.
|   |-- validators.py
|   `-- webapi.py              <- All the Views that map to a URL are located in here.
|-- makefile                   <- Used to run a CI like system locally.
|-- mongo-for-testing.yml      <- MongoDB docker-compose file used for local testing.
|-- poetry.lock
|-- pyproject.toml
`-- tests
    |-- __init__.py
    |-- factories.py
    |-- integration            <- Tests for all the components integrated together.
    |   |-- __init__.py
    |   |-- db_app_test_case.py
    |   |-- test_webapi.py
    |   `-- utils.py
    `-- unit                   <- Tests for a single unit, dependencies are mocked.
        |-- __init__.py
        |-- test_container.py
        |-- test_domain.py
        |-- test_usecases.py
        `-- test_webapi.py
```

## Tests
Run all the quality checks, unit tests and integration tests:
```bash
make
```

Run only unit tests:
```bash
python -m unittest discover tests/unit --verbose
```

Run only integration tests:
```bash
python -m unittest discover tests/integration --verbose
```

## Running the project locally:
Run MongoDB using docker-compose:
```bash
docker-compose -f mongo-for-testing.yml up -d
```

Using gunicorn:
```bash
gunicorn -w 1 --reload "gcmanager.app:create_app()" -e APP_ENV=TEST
```

## Index
* [What is this?](#what-is-this)
* [Why is this needed?](#why-is-this-needed)
* [What does this solve?](#what-does-it-solve)
* [Who is this intended for?](#who-is-this-intended-for)
* [Caveats](#caveats)

## What is this?
This is a gift card management system, made to manage your gift cards in a hassle-free way. Say goodbye to those pesky spreadsheets!

## Why is this needed?
I was having a really hard time managing my gift card collection in a spreadsheet, I always needed to fill in all the information by hand like the date of purchase, denomination, source etc. and honestly it never felt intuitive to me and was becoming a lot of work that was hard to maintain.

## What does it solve?
It aims to provide an intuitive way of adding a gift card to your asset collection & retrieve them as and when needed.

## Who is this intended for?
GCManager can be used by anyone who believe that managing their gift cards is becoming a **PITA**, and they wouldn't want to waste their time anymore.

## Caveats
* This application was made keeping **AMAZON** brand in mind, but can be used for other brands that use **PIN** & **Redeem Code**.
