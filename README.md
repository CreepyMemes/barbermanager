<div align="center">
  <img src="./frontend/public/logo.png" height="100px" alt="BarberManager Logo"/>
  <h1>BarberManager</h1>

  <!-- Badges -->

[![Deploy to Production](https://github.com/CreepyMemes/barbermanager/actions/workflows/deploy.yml/badge.svg?branch=master)](https://github.com/CreepyMemes/barbermanager/actions/workflows/deploy.yml)
[![Website](https://img.shields.io/badge/website-barbermanager.creepymemes.com-31C754?logo=cloudflare&logoColor=white)](https://barbermanager.creepymemes.com/)

</div>

# Project Documentation

This project is containerized using **Docker**, **Docker Compose** and **VSCode Dev Containers** for easy setup and cross-platform consistency.

## Table of Contents

- [Project Documentation](#project-documentation)
  - [Table of Contents](#table-of-contents)
  - [Requirements](#requirements)
- [System Architecture](#system-architecture)
- [Backend API Documentation](#backend-api-documentation)
- [Development Workflow](#development-workflow)
  - [1. Clone the repository:](#1-clone-the-repository)
  - [2. Build and launch development containers](#2-build-and-launch-development-containers)
  - [To reset the environment](#to-reset-the-environment)
  - [Backend Development (Django API)](#backend-development-django-api)
    - [Configuration](#configuration)
    - [To install new python dependencies](#to-install-new-python-dependencies)
    - [To run migrations](#to-run-migrations)
    - [to create a superuser](#to-create-a-superuser)
    - [To run test cases](#to-run-test-cases)
    - [To check test case coverage](#to-check-test-case-coverage)
    - [To generate model diagram](#to-generate-model-diagram)
  - [Frontend Development (React + Vite)](#frontend-development-react--vite)
    - [To install new npm Packages](#to-install-new-npm-packages)
  - [Developer Notes](#developer-notes)
    - [Barber Availability](#barber-availability)
    - [Client Appointments](#client-appointments)
    - [Tasks](#tasks)
    - [Reviews](#reviews)
  - [Statistics](#statistics)
- [Production Workflow](#production-workflow)
  - [Deployment](#deployment)

## Requirements

Make sure the following are installed on your machine:

- [Docker](https://docs.docker.com/engine/install/) installed
- [Docker Compose](https://docs.docker.com/compose/install/) installed
- [VSCode](https://code.visualstudio.com/) with the [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension installed

# System Architecture

```mermaid
flowchart TD
    %% User and Client
    enduser([User<br/>Browser/Mobile])

    %% Frontend
    FE[Frontend: Nginx<br/>Container: frontend]
    subgraph Frontend Container
    FE
    end

    %% Backend
    BE[Backend: Django<br/>Container: backend]

    subgraph Backend Container
        BE
    end

    %% Postgres and Redis
    RD[(Redis Broker<br/>Container: redis)]
    PG[(Postgres DB<br/>Container: db)]

    subgraph Infra Containers
        RD
        PG
    end

    %% Celery
    CW[[Celery Worker<br/>Container: celery]]
    CB[[Celery Beat<br/>Container: celery-beat]]

    subgraph Celery Containers
        CW
        CB
    end


    %% Frontend
    FE -- Serves React SPA --> enduser

    %% Core Request/Response Flow
    enduser -- HTTPS --> FE
    FE -- HTTPS /API --> BE
    BE -- Serves Rest API --> FE

    %% Backend/DB/Cache
    BE -- ORM (SQL) --> PG

    %% Celery Worker process
    CW -- ORM (SQL for task logic) --> PG
    CW -- Pulls tasks --> RD

    %% Celery Beat Schedules
    CB -- Enqueues jobs --> RD

    %% Relationships
    BE -.-> CW
    BE -.-> CB

    %% Show persistent volumes
    classDef volstyle fill:#E0E0E0,stroke:#999

    %% Color / Service Types
    style FE fill:#008000
    style BE fill:#092e20

    style RD fill:#D82C20
    style PG fill:#0064a5
    style CW fill:#64913D
    style CB fill:#64913D
```

# Backend API Documentation

You can find the API `Swagger` documentation here:
https://barbermanager.creepymemes.com/api

# Development Workflow

This section is about the development workflow in programming and testing the application on local machine.

> [!TIP]
> If you want to run **VSCode** inside the backend container.
> When you open the project `backend` or `frontend` foldlers in **VSCode**,
> it shoullt automaticaly detect the `.devcontainer` configurations.
>
> If it doesn't detect it or you ignore the notification you can:
> Open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P` on macOS).
> Select `Remote-Containers: Reopen in Container`.

## 1. Clone the repository:

> [!IMPORTANT]
> Change **TOKEN** to your github token
>
> ```bash
> git clone https://CreepyMemes:TOKEN@github.com/CreepyMemes/BarberManager.git
> cd BarberManager/Implementazione
> ```

## 2. Build and launch development containers

```bash
docker compose -f docker-compose.dev.yml up --build
```

## To reset the environment

```bash
docker compose -f docker-compose.dev.yml down --volumes --remove-orphans
```

- Frontend available at: [http://localhost:3000](http://localhost:3000)
- Backend available at: [http://localhost:8000](http://localhost:8000)

## Backend Development (Django API)

The Django dev server reloads automatically on code changes.

> [!IMPORTANT]
> Run the following commands _inside_ the container.
> by running the following command:
>
> ```bash
> docker compose -f docker-compose.dev.yml exec -it backend sh
> ```

### Configuration

- Create a .env.local file containing your stmp server credentials, follow this example:

```bash
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.server.com'
EMAIL_PORT=587
EMAIL_USE_TLS=1
EMAIL_HOST_USER='your@email.com'
EMAIL_HOST_PASSWORD='your-password'
```

### To install new python dependencies

```bash
pip install <package>

# If for both prod and dev
pip freeze > requirements/base.txt

# If for dev
pip freeze > requirements/dev.txt

# If for prod
pip freeze > requirements/prod.txt
```

### To run migrations

```bash
python manage.py migrate
```

### to create a superuser

```bash
python manage.py createsuperuser
```

### To run test cases

```bash
python manage.py test api
```

### To check test case coverage

This is a useful installed package `coverage` that highlights which part of the codebase are being tested, helps with developing testcases, to use:

```bash
# to run
coverage run --source="." manage.py test api

# To check results, generates htmlconv find index.html
coverage html

# Or just print retults in terminal
coverage report
```

### To generate model diagram

This is a useful installed package `django-extensions` that has many features, of which a diagram generator for all the implemented models found in the project, to use:

```bash
python manage.py graph_models -a -o models_diagram.png
```

## Frontend Development (React + Vite)

Vite provides automatic hot-reloading when frontend files are modified.

> [!IMPORTANT]
> Run the following commands _inside_ the container.
> by running the following command:
>
> ```bash
> docker compose -f docker-compose.dev.yml exec -it frontend sh
> ```

### To install new npm Packages

```bash
npm install <package>
```

## Developer Notes

### Barber Availability

Status: ✅

Barber availability is defined as a single record per barber per date, listing all 1-hour time slots during which the barber is available.

Model Example:

```json
{
  "barber": 3, // Barber ID associated to the availability
  "date": "2025-05-20",
  "slots": ["09:00", "10:00", "11:00", "14:00", "15:00"]
}
```

**Rules & Constraints:**

- Each time slot represents a fixed 1-hour window.
- Availability data is managed exclusively by admins.
- Only one availability entry is allowed per barber per date.

### Client Appointments

Status: ✅

Clients can book a single available slot with a barber on a specific date, along with one or more services offered by that barber.

Model Example:

```json
{
  "client": 12,
  "barber": 3,
  "date": "2025-05-20",
  "slot": "09:00",
  "status": "ONGOING",
  "services": [4, 7] // Service IDs associated to the appointment
}
```

**Rules & Constraints:**

- A client may have only **one** appointment with `status = "ONGOING"` at a time.
- The selected `slot` must:

  - Exist in the barber’s availability for the specified date.
  - Not be already booked by another appointment.

### Tasks

Status: ✅

Used `Celery` to run background tasks to:

- trigger automatic email reminders that trigger a bit before the appointment is due.
- update ONGOING appointment status to COMPLETED when it is due

This was deployed with 3 services, `Celery worker`, `Celery beat` and `Redis broker`.

### Reviews

Status: ✅

Clients can submit a **single** review per barber, but **only** after completing an appointment. Each review is directly associated with both the barber and the related appointment.

Model Example:

```json
{
  "appointment": 101, // Appointment ID associated to the review
  "client": 12,
  "barber": 3,
  "rating": 5, // Rating vote (1 - 5)
  "comment": "Great cut, very professional!"
}
```

**Rules & Constraints:**

- One review per client per barber.
- Reviews are allowed **only** after the associated appointment is completed.

## Statistics

Status: ✅

Generate overall statistics about total revenue, appointments, reviews and average rating

# Production Workflow

The Barber Manager website can be accessed at: [http://barbermanager.creepymemes.com](http://barbermanager.creepymemes.com)

## Deployment

The deployment process is fully automated using `GitHub Actions CI/CD`. Any push to the `master` branch will automatically trigger a redeployment, ensuring the latest changes are always live.
