<div align="center"><img src="./frontend/public/logo.png" height="100px" alt="BarberManager Logo"/></div>

## 🚀 Overview

BarberManager is a modern web-based management system for barber shops, featuring a Django REST API backend and a Vite + React frontend.

The entire project is containerized using **Docker** and **VSCode Dev Containers** for easy setup and consistent development environments across teams.

## 🐳 Getting Started with Docker

### Requirements

- [Docker](https://www.docker.com/) installed
- [Docker Compose](https://docs.docker.com/compose/) installed
- [VSCode](https://code.visualstudio.com/) with the [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension installed

### Installation & Startup

1. Clone the repository:

```bash
git clone https://github.com/CreepyMemes/BarberManager.git
cd BarberManager/Implementazione
```

2. Build and run all services:

```bash
docker-compose up --build
```

- Frontend (React App) will be available at: [http://localhost:3000](http://localhost:3000)
- Backend (Django API) will be available at: [http://localhost:8000](http://localhost:8000)

## ⚙️ Development Workflow with VSCode

### 1. Open the Project in VSCode

When you open the project, VSCode will automatically detect the `.devcontainer` configuration for both the **frontend** and **backend** folders. The following configurations are set:

- **Backend (Django API)**: Automatically uses the Python environment inside the container.
- **Frontend (React App)**: Includes necessary extensions like Prettier and ESLint for code formatting and linting.

To open the project in the containerized environment:

- Open VSCode.
- Open the **Command Palette** (`Ctrl+Shift+P` or `Cmd+Shift+P` on macOS).
- Search for **Remote-Containers: Reopen in Container**.

This will connect VSCode to the running Docker container, allowing you to work inside the containerized development environment.

### 2. Using the Backend Dev Container (Django API)

Any changes you make to the Python code will trigger automatic reloading due to Django's development server.

- If you add new dependencies to the backend:

```bash
pip install <package>
pip freeze > requirements.txt
```

Or from the host machine (in the backend directory):

```bash
docker-compose exec backend pip install <package>
docker-compose exec backend pip freeze > requirements.txt
```

- You can also run Django management commands, for example:

```bash
python manage.py migrate
python manage.py createsuperuser
```

Or from the host machine (in the backend directory):

```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```

### 3. Using the Frontend Dev Container (React + Vite)

Vite will automatically hot-reload on file changes.

- If you need to install a new npm package for the frontend:

```bash
npm install <package>
```

Or from the host machine (inside the frontend directory):

```bash
docker-compose exec frontend npm install <package>
```

### 4. Code Formatting & Linting

Both the frontend and backend containers are configured with useful extensions in VSCode:

- **Backend**: Python, Pylance for IntelliSense, and auto-imports.
- **Frontend**: Prettier for formatting and ESLint for linting.

Formatting happens automatically on save, and linting will give you feedback as you type.

## ⚠️ Troubleshooting

- **Port conflicts**: If ports like `3000` or `8000` are already in use, stop any other services or change the ports in `docker-compose.yml`.
- **Container not opening automatically in VSCode**: If VSCode doesn’t automatically switch to the container, manually open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`) and select **Remote-Containers: Reopen in Container**.
- **If you face issues with Python interpreter**: You can manually select the correct Python interpreter by opening the Command Palette and selecting **Python: Select Interpreter**.

## 🔄 Resetting the Environment

To reset everything and rebuild from scratch:

```bash
docker-compose down --volumes --remove-orphans
docker-compose up --build
```

This will remove all volumes (including any data stored in your containers) and rebuild everything from the ground up.
