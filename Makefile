.PHONY: help dev-frontend dev-backend dev

help:
	@echo "Available commands:"
	@echo "  make dev-frontend     - Starts frontend dev server (Vite)"
	@echo "  make dev-backend      - Starts backend dev server (LangGraph/FastAPI)"
	@echo "  make dev              - Starts both servers concurrently"

dev-frontend:
	cd frontend && npm run dev

dev-backend:
	cd backend && langgraph dev

# Runs both processes in parallel; both stop on Ctrl+C (POSIX systems)
dev:
	@echo "Starting both frontend and backend dev servers..."
	@$(MAKE) dev-frontend &
	@frontend_pid=$$!; \
	$(MAKE) dev-backend; \
	wait $$frontend_pid

# Optional: If you use npm 'concurrently', this is cross-platform
dev-concurrent:
	cd frontend && npm install --no-save concurrently
	npx concurrently "cd frontend && npm run dev" "cd backend && langgraph dev"
