<div align="center">
    <img src="./frontend/public/logo.png" height="100px" alt="BarberManager Logo"/>
</div>

# Project Documentation

This project is containerized using **Docker**, **Docker Compose** and **VSCode Dev Containers** for easy setup and cross-platform consistency.

## Table of Contents

- [Project Documentation](#project-documentation)
  - [Table of Contents](#table-of-contents)
  - [Requirements](#requirements)
- [Development Workflow](#development-workflow)
  - [1. Clone the repository:](#1-clone-the-repository)
  - [2. Build and launch development containers](#2-build-and-launch-development-containers)
  - [To reset the environment](#to-reset-the-environment)
  - [Backend Development (Django API)](#backend-development-django-api)
    - [To install new python dependencies](#to-install-new-python-dependencies)
    - [To run migrations](#to-run-migrations)
    - [to create a superuser](#to-create-a-superuser)
    - [To run test cases](#to-run-test-cases)
    - [To check test case coverage](#to-check-test-case-coverage)
    - [To generate model diagram](#to-generate-model-diagram)
  - [Frontend Development (React + Vite)](#frontend-development-react--vite)
    - [To install new npm Packages](#to-install-new-npm-packages)
- [API Endpoint Guide \[TODO\]](#api-endpoint-guide-todo)
  - [Auth Endpoints (`api/auth/`)](#auth-endpoints-apiauth)
  - [Admin Endpoints (`api/admin/`)](#admin-endpoints-apiadmin)
  - [Barber Endpoints (`api/barber/`)](#barber-endpoints-apibarber)
  - [Client Endpoints (`api/client/`)](#client-endpoints-apiclient)
  - [Common Endpoints (`api/public/`)](#common-endpoints-apipublic)
  - [Developer Notes](#developer-notes)
    - [Barber Availability](#barber-availability)
    - [Client Appointments](#client-appointments)
    - [Reviews](#reviews)
- [Production Workflow](#production-workflow)
  - [1 SSH into produciton server](#1-ssh-into-produciton-server)
  - [1. Clone the repository:](#1-clone-the-repository-1)
  - [2. Copy the project's reverse proxy settings](#2-copy-the-projects-reverse-proxy-settings)
  - [3. Pull latest code from GitHub](#3-pull-latest-code-from-github)
  - [4. Build and run production containers](#4-build-and-run-production-containers)
- [Rerun the server's reverse proxy](#rerun-the-servers-reverse-proxy)

## Requirements

Make sure the following are installed on your machine:

- [Docker](https://docs.docker.com/engine/install/) installed
- [Docker Compose](https://docs.docker.com/compose/install/) installed
- [VSCode](https://code.visualstudio.com/) with the [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension installed

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

```bash
git clone https://github.com/CreepyMemes/BarberManager.git
cd BarberManager/Implementazione
```

## 2. Build and launch development containers

```bash
docker-compose -f docker-compose.dev.yml up --build
```

## To reset the environment

```bash
docker-compose -f docker-compose.dev.yml down --volumes --remove-orphans
```

- Frontend available at: [http://localhost:3000](http://localhost:3000)
- Backend available at: [http://localhost:8000](http://localhost:8000)

## Backend Development (Django API)

The Django dev server reloads automatically on code changes.

> [!IMPORTANT]
> Run the following commands _inside_ the container.
> by running the following command:
> `docker-compose -f docker-compose.dev.yml exec -it backend sh`.

### To install new python dependencies

```bash
pip install <package>
pip freeze > requirements.txt
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
> `docker-compose -f docker-compose.dev.yml exec -it frontend sh`.

### To install new npm Packages

```bash
npm install <package>
```

# API Endpoint Guide [TODO]

```
api/
├── auth/
├── admin/
├── barber/
├── client/
└── public/
```

- ✅ Implemented endpoint
- 🧪 Implemented testcases

## Auth Endpoints (`api/auth/`)

| Endpoint                                 | Method | Description                                     | Status |
| ---------------------------------------- | ------ | ----------------------------------------------- | ------ |
| `/auth/register/`                        | POST   | Register a new client.                          | ✅ 🧪  |
| `/auth/register/<uidb64>/<token>/`       | POST   | Register a barber after an invitation email.    | ✅ 🧪  |
| `/auth/verify/<uidb64>/<token>/`         | GET    | Verify a client's email address.                | ✅ 🧪  |
| `/auth/me/`                              | GET    | Get the currently logged-in user's profile.     | ✅ 🧪  |
| `/auth/login/`                           | POST   | Log in a user.                                  | ✅ 🧪  |
| `/auth/logout/`                          | POST   | Log out the current user                        | ✅ 🧪  |
| `/auth/reset-password/`                  | POST   | Send password reset link via email.             | ✅ 🧪  |
| `/auth/reset-password/<uidb64>/<token>/` | POST   | Confirm and apply password reset.               | ✅ 🧪  |
| `/auth/refresh-token/`                   | POST   | Get a new access token using the refresh token. | ✅ 🧪  |

## Admin Endpoints (`api/admin/`)

| Endpoint                           | Method  | Description                                                      | Status |
| ---------------------------------- | ------- | ---------------------------------------------------------------- | ------ |
| `/admin/barber/`                   | POST    | Invite a barber through their email.                             | ✅ 🧪  |
| `/admin/barber/<barber_id>/`       | DELETE  | Remove a barber by ID                                            | ✅     |
| `/admin/availability/<barber_id>/` | POST    | Add or update availability slots for a barber on a specific date |        |
| `/admin/availability/<barber_id>/` | PATCH   | Edit availability slots for a barber on a specific date          |        |
| `/admin/availability/<barber_id>/` | DELELTE | Delete availability slots for a barber on a specific date        |        |
| `/admin/statistics/`               | GET     | Generate general statistics                                      |        |
| `/admin/appointments/`             | GET     | View a list of all past appointments                             |        |

## Barber Endpoints (`api/barber/`)

| Endpoint                         | Method | Description                  | Status |
| -------------------------------- | ------ | ---------------------------- | ------ |
| `/barber/services/`              | GET    | List own services            |        |
| `/barber/services/`              | POST   | Add a service                |        |
| `/barber/services/<service_id>/` | PATCH  | Edit a service               |        |
| `/barber/services/<service_id>/` | DELETE | Remove a service             |        |
| `/barber/reviews/`               | GET    | List reviews of own services |        |
| `/barber/appointments/`          | GET    | View upcoming appointments   |        |

## Client Endpoints (`api/client/`)

| Endpoint                                 | Method | Description                                          | Status |
| ---------------------------------------- | ------ | ---------------------------------------------------- | ------ |
| `/client/appointments/`                  | GET    | List own past appointments                           |        |
| `/client/appointments/`                  | POST   | Create a appointment only if no active one currently |        |
| `/client/appointments/<appointment_id>/` | DELETE | Cancel if still ongoing                              |        |
| `/client/reviews/`                       | GET    | List own reviews                                     |        |
| `/client/reviews/<appointment_id>/`      | POST   | Create review for barber of appointment if competed  |        |
| `/client/reviews/<review_id>/`           | PATCH  | Edit own review                                      |        |
| `/client/reviews/<review_id>/`           | DELETE | Delete own review                                    |        |

## Common Endpoints (`api/public/`)

| Endpoint                                   | Method | Description                           | Status |
| ------------------------------------------ | ------ | ------------------------------------- | ------ |
| `/public/barbers/`                         | GET    | List all barbers                      | ✅     |
| `/public/barber/<barber_id>/services/`     | GET    | List services by selected barber      |        |
| `/public/barber/<barber_id>/availability/` | GET    | Get available time slots              |        |
| `/public/barber/<barber_id>/profile/`      | GET    | Get barber profile, reviews, services |        |

TODO: some way to set reminders (will think of this later)

## Developer Notes

### Barber Availability

Barber availability is defined as a single record per barber per date, listing all 1-hour time slots during which the barber is available. Example:

```json
{
  "barber": 3,
  "date": "2025-05-20",
  "slots": ["09:00", "10:00", "11:00", "14:00", "15:00"]
}
```

**Rules & Constraints:**

- Each time slot represents a fixed 1-hour window.
- Availability data is managed exclusively by admins.
- Only one availability entry is allowed per barber per date.

### Client Appointments

Clients can book a single available slot with a barber on a specific date, along with one or more services offered by that barber. Example:

```json
{
  "client": 12,
  "barber": 3,
  "date": "2025-05-20",
  "slot": "09:00",
  "status": "ONGOING",
  "services": [4, 7]
}
```

**Rules & Constraints:**

- A client may have only **one** appointment with `status = "ONGOING"` at a time.
- The selected `slot` must:

  - Exist in the barber’s availability for the specified date.
  - Not be already booked by another appointment.

### Reviews

Clients can submit a **single** review per barber, but **only** after completing an appointment. Each review is directly associated with both the barber and the related appointment. Example:

```json
{
  "appointment": 101,
  "client": 12,
  "barber": 3,
  "rating": 5,
  "comment": "Great cut, very professional!"
}
```

**Rules & Constraints:**

- One review per client per barber.
- Reviews are allowed **only** after the associated appointment is completed.

# Production Workflow

This section is about deplying the application to the internet in a production environment hosted by a server exposed to the internet.

## 1 SSH into produciton server

```bash
ssh rock@rockpi
```

## 1. Clone the repository:

```bash
cd projects && git clone https://github.com/CreepyMemes/BarberManager.git
cd BarberManager/Implementazione
```

## 2. Copy the project's reverse proxy settings

```bash
cd ~/nginx/conf.d/ && cd cp ~/projects/BarberManager/Implementazione/nginx/nginx.conf ~/nginx/conf.d/barbermanager.conf
```

## 3. Pull latest code from GitHub

```bash
cd ~/projects/BarberManager && git pull
```

## 4. Build and run production containers

```bash
cd ~/projects/BarberManager/Implementazione && docker compose -f docker-compose.prod.yml up -d --build
```

# Rerun the server's reverse proxy

```bash
cd ~/nginx/ && docker exec nginx nginx -s reload
```

- The deployed will be available at: [http://barbermanager.creepymemes.duckdns.org](http://barbermanager.creepymemes.duckdns.org)
