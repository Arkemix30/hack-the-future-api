<h1 align="center">fastapi-boilerplate</h1>

A well structured codebase written with FastAPI trying to follow the Clean Architecture principles.

*For more information about Clean Architecture, you can check the [documentation](https://prog.world/clean-architecture-through-the-eyes-of-a-python-developer/)*

*P.D: This is a modified version of the [FastAPI Clean Architecture](https://github.com/0xTheProDev/fastapi-clean-example) project, but with some changes to fit the needs of every developer*

## Table of Content 📑
---
- [Project Folder Structure](#project-folder-structure)
- [How to run the code](#how-to-run-the-code)
    - [Installation](#installation)
- [Installing project's dependencies](#installing-projects-dependencies)
- [How to run locally](#how-to-run-locally)
- [How to run migrations](#how-to-run-migrations)
    - [Alembic](#alembic)
- [Development Configuration](#development-configuration)
    - [Pre-commit](#pre-commit)
    - [Convetional Commits (Commitizen)](#conventional-commits-commitizen)
- [Built with](#built-with)

<br>

## Project Folder Structure

```
.
├── alembic             # Migration tool.
│   └── versions        # Migrations made (Like `make migrations` in Django).
├── app                 # Main app folder.
│   ├── api             # Api related folder (routes, deps, versioning, etc.).
│   │   └── v1
│   │       └── routes  # Route folder where are all routes located for current version.
│   ├── core            # Core where locate all app configs,
│   │   └── settings    # like app settings, logging, etc.
│   │
│   ├── infrastructure  # Infrastructure related configs like databases, external resources, etc.
│   ├── entities        # Database models representation as python classes.
│   ├── repositories    # Collection of classes responsible of databases operations (CRUD).
│   ├── schemas         # Pydantic schemas for validating data input/output (like `serializers` in Django).
│   ├── services        # Classes with the business logic, like use cases.
│   └── utils           # Utils used in the app.
├── tests               # Test cases for the app.
└── main.py             # Entry point where uvicorn runs to start application.
```


## How to run the code

### Installation

You will need to install [Poetry](https://python-poetry.org/) to install project's dependencies

```bash
$ curl -sSL https://install.python-poetry.org | python3 -
```

*Note: On some systems, python may still refer to Python 2 instead of Python 3. We always suggest the python3 binary to avoid ambiguity.*

Locate where Poetry is installed

```bash
$ whereis poetry
```

Copy and replace poetry's path to this line and added it at the end of the `.bashrc` file

```bash
$ export PATH="$HOME/.poetry/bin:$PATH"
```

<br>

## Installing project's dependencies


Clone the repository

  ```bash
  $ git clone https://github.com/Arkemix30/fastapi-boilerplate
  ```

Enter into project's root folder and run:

```bash
$ poetry install
```

It should create a `.venv` folder, generating a virtual enviroment with all project's dependencies

<br>

## How to run locally


* To run the project, you need to activate the virtual environment.
  For that, you can run this command:

  ```bash
  $ poetry shell
  ```

* And finally, to run the server:

  ```bash
  $ uvicorn main:app --reload
  ```

<br>

## How to run migrations


### Alembic

* To create a new migration, run:

  ```bash
  $ alembic revision --autogenerate -m "Migration name"
  ```
  This will create a new migration file in `alembic/versions` folder.

* To apply the migrations made, run:

  ```bash
  $ alembic upgrade head
  ```
  This will apply all migrations to the database.

* To downgrade the migrations, run:

  ```bash
  $ alembic downgrade -1
  ```
  This will downgrade the last migration applied to the database.

* To downgrade all migrations, run:

  ```bash
  $ alembic downgrade base
  ```
  This will downgrade all migrations applied to the database.

* To check the history of migrations applied, run:

  ```bash
  $ alembic history
  ```
  This will show the history of migrations applied to the database.

*For more information about Alembic, you can check the [documentation](https://alembic.sqlalchemy.org/en/latest/)*

<br>

## Development Configuration


### Pre-commit

This project uses [pre-commit](https://pre-commit.com/) to run some checks before commiting the code.

To install it, run:

```bash
$ pre-commit install
```

This will install the hooks in the `.git/hooks` folder.

To run the checks manually, run:

```bash
$ pre-commit run --all-files
```

In case you want to skip the checks, you can use the `--no-verify` flag:

```bash
$ git commit -m "Commit message" --no-verify
```

In every commit, the following checks will be run:

* [black]( https://black.readthedocs.io/en/stable/) - The uncompromising code formatter.
* [flake8](https://flake8.pycqa.org/en/latest/) - The tool for style guide enforcement.
* [isort](https://pycqa.github.io/isort/) - A Python utility / library to sort imports.
* [bandit](https://bandit.readthedocs.io/en/latest/) - Security linter from OpenStack Security.
* [pre-commit-hooks](https://pre-commit.com/) - Some useful hooks for pre-commit.

<br>

### Conventional Commits (Commitizen)

This project uses [commitizen](https://commitizen-tools.github.io/commitizen/) to standardize the commit messages.

To install it, run:

```bash
$ pip install commitizen
```

To run it, run:

```bash
$ cz commit
```
*or the short version:*
```bash
$ cz c
```

This will open a prompt to write the commit message.

<br>

## Built with

* [FastAPI](https://fastapi.tiangolo.com/) - The framework used.
* [Uvicorn](https://www.uvicorn.org/) - The light-fast ASGI server.
* [Pydantic](https://docs.pydantic.dev/) - Data Validator using Python type annotations.
* [SQLModel](https://sqlmodel.tiangolo.com/) - Database ORM based in SQLAlchemy and Pydantic.
* [GeoAlchemy2](https://geoalchemy-2.readthedocs.io/en/latest/index.html) - Provides extensions to SQLAlchemy for working with spatial databases.
* [Alembic](https://alembic.sqlalchemy.org/en/latest/front.html) - Database migration tool to manage changes to the database schema over time.
* [SqlAdmin](https://aminalaee.dev/sqladmin/) - Admin interface for SQLAlchemy/SQLModel models.

---

README ⌨️ with ❤️ by [Enmanuel Silva](https://github.com/Arkemix30) 😊
