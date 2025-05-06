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
  - [Frontend Development (React + Vite)](#frontend-development-react--vite)
    - [Install npm Packages](#install-npm-packages)
  - [Troubleshooting](#troubleshooting)
  - [Resetting the Environment](#resetting-the-environment)

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

This command removes all volumes and rebuilds everything from scratch, ensuring a clean development state.
