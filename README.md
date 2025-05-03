<div align="center"><img src="./frontend/public/logo.png" height="100px" alt="BarberManager Logo"/></div>

## 🚀 Overview

BarberManager is a modern web-based management system for barber shops, featuring a Django REST API backend and a Vite + React frontend.

The entire project is containerized using Docker for easy setup and development across teams.

## 🐳 Getting Started with Docker

### ✅ Requirements

- [Docker](https://www.docker.com/) installed
- [Docker Compose](https://docs.docker.com/compose/) installed

### 🔧 Installation & Startup

1. Clone the repository:

```bash
git clone <repo-url>
cd <project-folder>
```

2. Build and run all services:

```bash
docker-compose up --build
```

- Frontend (React App) will be available at: [http://localhost:3000](http://localhost:3000)
- Backend (Django API) will be available at: [http://localhost:8000](http://localhost:8000)

## ⚙️ Development Tips

### 🔄 Apply Backend Changes

If you make changes to backend Python code, Django will auto-reload. If you add new dependencies:

```bash
# Inside the backend container:
docker-compose exec backend pip install <package>
docker-compose exec backend pip freeze > requirements.txt
```

### 💄 Apply Frontend Changes

React (Vite) supports hot reload by default. If you add a new npm package:

```bash
# Inside the frontend container:
docker-compose exec frontend npm install <package>
```

## ⚠️ Troubleshooting

- If ports like `3000` or `8000` are already in use, stop any other services or change the ports in `docker-compose.yml`.
- To reset everything:

```bash
docker-compose down --volumes --remove-orphans
docker-compose up --build
```
