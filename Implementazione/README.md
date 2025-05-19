<div align="center">
    <img src="./frontend/public/logo.png" height="100px" alt="BarberManager Logo"/>
</div>

# Project Documentation

This project is containerized using **Docker**, **Docker Compose** and **VSCode Dev Containers** for easy setup and cross-platform consistency.

## Table of Contents

- [Project Documentation](#project-documentation)
  - [Table of Contents](#table-of-contents)
  - [Requirements](#requirements)
  - [Installation \& Startup](#installation--startup)
    - [1. Clone the repository:](#1-clone-the-repository)
    - [2. Build and Launch Services](#2-build-and-launch-services)
  - [Using VSCode Dev Containers](#using-vscode-dev-containers)
    - [To Start:](#to-start)
  - [Backend Development (Django API)](#backend-development-django-api)
    - [Install Python Dependencies](#install-python-dependencies)
    - [Run Migrations](#run-migrations)
    - [Create SuperUser](#create-superuser)
    - [Run test cases](#run-test-cases)
    - [Check test case coverage](#check-test-case-coverage)
    - [Generate model diagram](#generate-model-diagram)
  - [Frontend Development (React + Vite)](#frontend-development-react--vite)
    - [Install npm Packages](#install-npm-packages)
  - [Troubleshooting](#troubleshooting)
  - [Resetting the Environment](#resetting-the-environment)
  - [Entering the container shell from host machine](#entering-the-container-shell-from-host-machine)
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

## Requirements

Make sure the following are installed on your machine:

- [Docker](https://www.docker.com/) installed
- [Docker Compose](https://docs.docker.com/compose/) installed
- [VSCode](https://code.visualstudio.com/) with the [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension installed

## Installation & Startup

### 1. Clone the repository:

```bash
git clone https://github.com/CreepyMemes/BarberManager.git
cd BarberManager/Implementazione
```

### 2. Build and Launch Services

```bash
docker-compose up --build
```

- Frontend available at: [http://localhost:3000](http://localhost:3000)
- Backend available at: [http://localhost:8000](http://localhost:8000)

## Using VSCode Dev Containers

When you open the project in VSCode, it detects the `.devcontainer` configurations for both frontend and backend:

- **Backend (Django)**: Uses container-based Python environment.
- **Frontend (React + Vite)**: Preconfigured with Prettier, ESLint, and other useful extensions.

### To Start:

1. Open VSCode.
2. Open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P` on macOS).
3. Select `Remote-Containers: Reopen in Container`.

## Backend Development (Django API)

The Django server reloads automatically on code changes.

> [!TIP]
> Run the following commands _inside_ the container.
> If using from the host, prefix commands with:
>
> `docker-compose exec backend`.

### Install Python Dependencies

```bash
pip install <package>
pip freeze > requirements.txt
```

### Run Migrations

```bash
python manage.py migrate
```

### Create SuperUser

```bash
python manage.py createsuperuser
```

### Run test cases

```bash
python manage.py test api
```

### Check test case coverage

This is a useful installed package `coverage` that highlights which part of the codebase are being tested, helps with developing testcases, to use:

```bash
# to run
coverage run --source="." manage.py test api

# To check results, generates htmlconv find index.html
coverage html

# Or just print retults in terminal
coverage report
```

### Generate model diagram

This is a useful installed package `django-extensions` that has many features, of which a diagram generator for all the implemented models found in the project, to use:

```bash
python manage.py graph_models -a -o models_diagram.png
```

## Frontend Development (React + Vite)

Vite provides automatic hot-reloading when frontend files are modified.

> [!TIP]
> Run the following commands _inside_ the container.
> If using from the host, prefix commands with:
>
> `docker-compose exec frontend`.

### Install npm Packages

```bash
npm install <package>
```

## Troubleshooting

- **Port Conflicts**: Ensure ports `3000` and `8000` are free or modify them in `docker-compose.yml`.
- **Dev Container Not Opening**: Use `Remote-Containers: Reopen in Container` from the Command Palette.
- **Python Interpreter Issues**: Use `Python: Select Interpreter` in the Command Palette to choose the correct environment.

## Resetting the Environment

To fully reset and rebuild the environment:

```bash
docker-compose down --volumes --remove-orphans
docker-compose up --build
```

## Entering the container shell from host machine

```bash
# For the frontend docker container
docker-compose exec -it frontend sh

# Or for the backend one
docker-compos exec -it backend sh
```

## API Endpoint Guide [TODO]

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

### Auth Endpoints (`api/auth/`)

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

### Admin Endpoints (`api/admin/`)

| Endpoint                           | Method  | Description                                                      | Status |
| ---------------------------------- | ------- | ---------------------------------------------------------------- | ------ |
| `/admin/barber/`                   | POST    | Invite a barber through their email.                             | ✅ 🧪  |
| `/admin/barber/<barber_id>/`       | DELETE  | Remove a barber by ID                                            | ✅     |
| `/admin/availability/<barber_id>/` | POST    | Add or update availability slots for a barber on a specific date |        |
| `/admin/availability/<barber_id>/` | PATCH   | Edit availability slots for a barber on a specific date          |        |
| `/admin/availability/<barber_id>/` | DELELTE | Delete availability slots for a barber on a specific date        |        |
| `/admin/statistics/`               | GET     | Generate general statistics                                      |        |
| `/admin/appointments/`             | GET     | View a list of all past appointments                             |        |

### Barber Endpoints (`api/barber/`)

| Endpoint                         | Method | Description                  | Status |
| -------------------------------- | ------ | ---------------------------- | ------ |
| `/barber/services/`              | GET    | List own services            |        |
| `/barber/services/`              | POST   | Add a service                |        |
| `/barber/services/<service_id>/` | PATCH  | Edit a service               |        |
| `/barber/services/<service_id>/` | DELETE | Remove a service             |        |
| `/barber/reviews/`               | GET    | List reviews of own services |        |
| `/barber/appointments/`          | GET    | View upcoming appointments   |        |

### Client Endpoints (`api/client/`)

| Endpoint                                 | Method | Description                                          | Status |
| ---------------------------------------- | ------ | ---------------------------------------------------- | ------ |
| `/client/appointments/`                  | GET    | List own past appointments                           |        |
| `/client/appointments/`                  | POST   | Create a appointment only if no active one currently |        |
| `/client/appointments/<appointment_id>/` | DELETE | Cancel if still ongoing                              |        |
| `/client/reviews/`                       | GET    | List own reviews                                     |        |
| `/client/reviews/<appointment_id>/`      | POST   | Create review for barber of appointment if competed  |        |
| `/client/reviews/<review_id>/`           | PATCH  | Edit own review                                      |        |
| `/client/reviews/<review_id>/`           | DELETE | Delete own review                                    |        |

### Common Endpoints (`api/public/`)

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
