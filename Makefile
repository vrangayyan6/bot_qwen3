.PHONY: help install install-backend install-frontend dev-frontend dev-backend dev

help:
	@echo "Available commands:"
	@echo "  make install           - Installs all dependencies for Windows"
	@echo "  make dev               - Starts both frontend and backend servers for Windows"
	@echo "  ---"
	@echo "  make install-backend   - Installs backend dependencies"
	@echo "  make install-frontend  - Installs frontend dependencies"
	@echo "  make dev-frontend      - Starts the frontend development server (Vite)"
	@echo "  make dev-backend       - Starts the backend development server (Langgraph)"


install: install-backend install-frontend

install-backend:
	@echo "Checking for backend virtual environment..."
	@if not exist backend\venv (py -m venv backend\venv)
	@echo "Installing backend dependencies..."
	@call backend\venv\Scripts\activate.bat && pip install -e backend

install-frontend:
	@echo "Installing frontend dependencies..."
	@cd frontend && npm install

dev-frontend:
	@echo "Starting frontend development server..."
	@cd frontend && npm run dev

dev-backend:
	@echo "Starting backend development server..."
	@echo "Activating backend environment and starting server..."
	@cd backend && call .\venv\Scripts\activate.bat && langgraph dev

# Run frontend and backend concurrently
dev:
	@echo "Starting both frontend and backend development servers in new windows..."
	@start "Frontend" make dev-frontend
	@start "Backend" make dev-backend