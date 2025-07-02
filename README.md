<div align="center">
  <img src="./frontend/assets/images/logo.webp" height="100px" alt="BarberManager Logo"/>
  <h1>BarberManager</h1>

[![Deploy to Production](https://github.com/CreepyMemes/barbermanager/actions/workflows/deploy.yml/badge.svg?branch=master)](https://github.com/CreepyMemes/barbermanager/actions/workflows/deploy.yml)
[![BarberManager](https://img.shields.io/badge/BarberManager-Live%20Website-F38020?labelColor=555555&logo=cloudflare&logoColor=white)](https://barbermanager.creepymemes.com/)
[![API Documentation](https://img.shields.io/badge/Swagger%20UI-API%20Documentation-6ec225?labelColor=555555&logo=swagger&logoColor=white)](https://barbermanager.creepymemes.com/api/)

</div>

## Overview

BarberManager is a containerized barber shop management system web application.

It provides an appointment booking system for clients, availability management for barbers, and automated reminders.

The tech stack uses **React** (Vite) frontend, **Django** backend, and relies on **Docker Compose** for easy cross-platform development & deployment.

## Table of Contents

- [Overview](#overview)
- [Table of Contents](#table-of-contents)
- [Features](#features)
- [Architecture](#architecture)
- [API Documentation](#api-documentation)
- [Live Deployment](#live-deployment)
- [Quickstart](#quickstart)
  - [Requirements](#requirements)
  - [Development Workflow](#development-workflow)
    - [Clone the repository](#clone-the-repository)
    - [Build and launch all containers](#build-and-launch-all-containers)
    - [(Optional) Reset dev environment](#optional-reset-dev-environment)
- [Development Guide](#development-guide)
  - [Backend (Django)](#backend-django)
    - [Configuration](#configuration)
    - [Dependencies](#dependencies)
    - [Migrations](#migrations)
    - [SuperUser](#superuser)
    - [Run tests](#run-tests)
    - [Model diagram](#model-diagram)
  - [Frontend (React + Vite)](#frontend-react--vite)
    - [Dependencies](#dependencies-1)
    - [Run tests](#run-tests-1)
- [Production Workflow](#production-workflow)
  - [Deployment](#deployment)
    - [CI/CD Workflow Overview](#cicd-workflow-overview)

## Features

- 💇‍♂️ **Barber Availability**: Admins define 1-hour slot schedules for each barber.
- 📅 **Client Appointments**: Clients can book available slots with their chosen barber & service(s).
- ⏰ **Reminders & Automation**: Email reminders and automatic appointment status updates via Celery tasks.
- 💬 **Client Reviews**: Only permitted after completed appointments; one per client-barber pair.
- 📊 **Dashboard Statistics**: See business insights & feedback.
- 🐳 **Portable Development**: Containerized via Docker and VSCode Dev Containers for zero-conf dev setup.
- ♾️ **DevOps & CI/CD**: GitHub Actions automate testing, linting, and deployment.

## Architecture

```mermaid
flowchart TD
    US([User <br> Browser/Mobile])

    RP[Reverse Proxy: Nginx]

    subgraph FrontendInfra[Frontend Infrastructure]
      subgraph frontend[Container: 'frontend']
        SF[Server: Nginx]
        BL[Builder: Vite]
        FE[Frontend: React SPA]
      end
    end

    subgraph BackendInfra[Backend Infrastructure]
      subgraph backend[Container: 'backend']
        SB[WSGI: Gunicorn]
        BE[Backend: Django REST API]
      end

      subgraph celery[Container: 'celery']
          CW[[Worker: Celery]]
      end

      subgraph celery-beat[Container: 'celery-beat']
          CB[[Beat: Celery]]
      end

      subgraph db[Container: 'db']
        PG[(Datatbase: Postgres)]
      end

      subgraph redis[Container: 'redis']
        RD[(Broker: Redis)]
      end
    end

    %% User
    US -- HTTPS --> RP
    RP -- Routes --> SF
    RP -- Routes --> SB

    %% Frontend Infrastructutre
    SF -- Serves --> BL
    BL -- Builds --> FE

    %% Backend Infrastructutre
    SB -- Serves --> BE
    BE -- ORM Access --> PG
    CW -- ORM Access (for task logic) --> PG
    CW -- Pulls tasks --> RD
    CB -- Enqueues tasks --> RD
    BE .-> CW
    BE .-> CB

    style FrontendInfra fill:#0005
    style BackendInfra fill:#0005

    style frontend fill:#2496ED50
    style backend fill:#2496ED50
    style celery fill:#2496ED50
    style celery-beat fill:#2496ED50
    style db fill:#2496ED50
    style redis fill:#2496ED50

    style SF fill:#009639
    style BL fill:#646CFF
    style FE fill:#61DAFB
    style FE color:#000
    style RP fill:#009639
    style BE fill:#092e20
    style SB fill:#499848
    style RD fill:#FF4438
    style PG fill:#4169E1
    style CW fill:#37814A
    style CB fill:#37814A
```

## API Documentation

BarberManager offers extensive, interactive API documentation using **Swagger UI**.  
You can explore all backend endpoints, models, request/response formats, and try out live requests directly in your browser.

➡️ **[View the API Documentation here.](https://barbermanager.creepymemes.com/api/)**  
Or click the green "Swagger UI" badge at the top of this README.

Typical API documentation features:

- **Visual interface** for exploring all available endpoints and methods.
- **Live "Try it Out"** feature for authenticating and testing API calls.
- **Model schemas** and required/optional field details for each operation.

This documentation is always up-to-date with the deployed backend and is a helpful resource for frontend developers, integrators, and testers.

## Live Deployment

You can try out BarberManager yourself on our live, production website!

➡️ **[Open the Live Website](https://barbermanager.creepymemes.com/)**  
Or click the orange "BarberManager" badge at the top of this README.

The live deployment features:

- The latest available version, always kept up to date through automated CI/CD.
- Full access to the web app's core features as described in this documentation.
- A real working environment for testing, demos, or exploring as a developer, admin, or client.

## Quickstart

### Requirements

- [Docker](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [VSCode](https://code.visualstudio.com/) (+ [Dev Containers Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers))

### Development Workflow

This section is about the development workflow in programming and testing the application on local machine.

> [!TIP]
> If you want to run **VSCode** inside the backend container.
> When you open the project `backend` or `frontend` foldlers in **VSCode**,
> it shoullt automaticaly detect the `.devcontainer` configurations.
>
> If it doesn't detect it or you ignore the notification you can:
> Open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P` on macOS).
> Select `Remote-Containers: Reopen in Container`.

#### Clone the repository

If the repository is public:

```bash
git clone https://github.com/CreepyMemes/barbermanager.git
cd barbermanager/
```

If the repository is private:

> [!IMPORTANT]
> Change **TOKEN** to your github token

```bash
git clone https://CreepyMemes:TOKEN@github.com/CreepyMemes/barbermanager.git
cd barbermanager
```

#### Build and launch all containers

```bash
docker compose -f docker-compose.dev.yml --env-file .env.dev up --build
```

- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend: [http://localhost:8000](http://localhost:8000)

#### (Optional) Reset dev environment

```bash
docker compose -f docker-compose.dev.yml down --volumes --remove-orphans
```

## Development Guide

### Backend (Django)

The Django dev server reloads automatically on code changes.

> [!IMPORTANT]
> Run the following commands _inside_ the container.
> by running the following command:
>
> ```bash
> docker compose -f docker-compose.dev.yml --env-file .env.dev exec -it backend sh
> ```

#### Configuration

Create a new `.env` file in root directory, and enter your credentials there, follow the example at `.env.example`:

```sh
# Django config
SECRET_KEY=your-super-secret-key-here
DJANGO_ALLOWED_HOSTS=*
DJANGO_SETTINGS_MODULE=config.settings.dev # change .dev or .prod

# Database config
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=mydb
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword

# Email config
EMAIL_HOST='smtp.server.com'
EMAIL_PORT=587
EMAIL_HOST_USER='your.stmp@email.com'
EMAIL_HOST_PASSWORD='your stmp pass here'
```

#### Dependencies

To install new dependencies, for either base, prod or dev:

```bash
pip install <package>
pip freeze > requirements/base.txt
pip freeze > requirements/dev.txt
pip freeze > requirements/prod.txt
```

#### Migrations

To migrate database:

```bash
python manage.py migrate
```

#### SuperUser

To create an admin user:

```bash
python manage.py createsuperuser
```

#### Run tests

To simply run all tests:

```bash
python manage.py test api
```

To check test coverage, we use `coverage` package that highlights which part of the codebase are being tested:

```bash
coverage run --source="." manage.py test api
coverage html
```

#### Model diagram

To generate a models diagram, we use `django-extensions` package that includes a diagram generator for all the implemented models found in the project, to use:

```bash
python manage.py graph_models -a -o models_diagram.png
```

### Frontend (React + Vite)

Vite provides automatic hot-reloading when frontend files are modified.

> [!IMPORTANT]
> Run the following commands _inside_ the container.
> by running the following command:
>
> ```bash
> docker compose -f docker-compose.dev.yml --env-file .env.dev exec -it frontend sh
> ```

#### Dependencies

To install new dependencies, for either prod or dev:

```bash
npm install <package> --save-dev
npm install <package>
```

#### Run tests

[TODO]

## Production Workflow

### Deployment

The deployment process is **fully automated** via [GitHub Actions](https://github.com/features/actions). The CI/CD pipeline is triggered by every **Pull Request**:

#### CI/CD Workflow Overview

```mermaid
flowchart TD
    PR(🔀 Pull Request)
    Tests{{🧪 Runs Tests}}
    Passed([✅ Able to Merge])
    Failed([❌ Cannot Merge])
    Deployment(🚀 Runs Deployment)
    PR --> Tests
    Tests -- Passed --> Passed
    Tests -- Failed --> Failed
    Passed -- Merge --> Deployment
```

1. **Build & Test:**  
   All pull requests trigger automated builds and tests in a production-like Docker environment.
2. **Merge & Deploy Automatically:**  
   If tests pass, the pull request can be merged.  
   Once merged, the code is automatically deployed to the server via SSH.

- Environment variables are provided securely with GitHub Secrets.
- Deployments use a custom `deploy.sh` script for zero downtime.
