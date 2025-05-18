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
  - [Frontend Development (React + Vite)](#frontend-development-react--vite)
    - [Install npm Packages](#install-npm-packages)
  - [Troubleshooting](#troubleshooting)
  - [Resetting the Environment](#resetting-the-environment)
  - [API Endpoint Guide \[TODO\]](#api-endpoint-guide-todo)
    - [Auth Endpoints (`api/auth/`)](#auth-endpoints-apiauth)
    - [Admin Endpoints (`api/admin/`)](#admin-endpoints-apiadmin)
    - [Barber Endpoints (`api/barber/`)](#barber-endpoints-apibarber)
    - [Client Endpoints (`api/client/`)](#client-endpoints-apiclient)
    - [Common Endpoints (`api/public/`)](#common-endpoints-apipublic)

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

To quickly enter the container shell from host machine

```bash
docker-compose exec -it frontend sh
#or
docker-compos exec -it backend sh
```

This command removes all volumes and rebuilds everything from scratch, ensuring a clean development state.

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

| Endpoint                           | Method | Description                          | Status |
| ---------------------------------- | ------ | ------------------------------------ | ------ |
| `/admin/barber/`                   | POST   | Invite a barber through their email. | ✅ 🧪  |
| `/admin/barber/<barber_id>/`       | DELETE | Remove a barber by ID                | ✅     |
| `/admin/availability/<barber_id>/` | POST   | Manage barber's availability slots   |        |
| `/admin/stats/`                    | GET    | Generate general statistics          |        |

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

| Endpoint                             | Method | Description                                    | Status |
| ------------------------------------ | ------ | ---------------------------------------------- | ------ |
| `/client/appointments/`              | GET    | List own past appointments                     |        |
| `/client/appointments/`              | POST   | Create a booking                               |        |
| `/client/appointments/<booking_id>/` | DELETE | Cancel if still ongoing                        |        |
| `/client/reviews/`                   | GET    | List own reviews                               |        |
| `/client/reviews/<booking_id>/`      | POST   | Create a review for barber of this appointment |        |
| `/client/reviews/<review_id>/`       | PATCH  | Edit own review                                |        |
| `/client/reviews/<review_id>/`       | DELETE | Delete own review                              |        |

### Common Endpoints (`api/public/`)

| Endpoint                                   | Method | Description                           | Status |
| ------------------------------------------ | ------ | ------------------------------------- | ------ |
| `/public/barbers/`                         | GET    | List all barbers                      | ✅     |
| `/public/barber/<barber_id>/services/`     | GET    | List services by selected barber      |        |
| `/public/barber/<barber_id>/availability/` | GET    | Get available time slots              |        |
| `/public/barber/<barber_id>/profile/`      | GET    | Get barber profile, reviews, services |        |

TODO: some way to set reminders (will think of this later)
