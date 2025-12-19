# -----------------------------
# Makefile for News Platform
# Dev + Production Orchestration
# -----------------------------

# File paths
DEV_COMPOSE = docker-compose.dev.yml
PROD_COMPOSE = docker-compose.prod.yml

# -----------------------------
# Development Commands
# -----------------------------

dev:
	docker compose -f $(DEV_COMPOSE) up --build

dev-down:
	docker compose -f $(DEV_COMPOSE) down

dev-rebuild:
	docker compose -f $(DEV_COMPOSE) up --build --force-recreate

dev-logs:
	docker compose -f $(DEV_COMPOSE) logs -f

dev-backend-shell:
	docker exec -it news-backend sh

dev-db-shell:
	docker exec -it news-db sh

# -----------------------------
# Production Commands
# -----------------------------

prod:
	docker compose -f $(PROD_COMPOSE) up --build -d

prod-down:
	docker compose -f $(PROD_COMPOSE) down

prod-rebuild:
	docker compose -f $(PROD_COMPOSE) up --build --force-recreate -d

prod-logs:
	docker compose -f $(PROD_COMPOSE) logs -f

prod-backend-shell:
	docker exec -it news-backend sh

prod-db-shell:
	docker exec -it news-db sh

# -----------------------------
# Shared Utilities
# -----------------------------

clean:
	docker compose -f $(DEV_COMPOSE) down -v
	docker compose -f $(PROD_COMPOSE) down -v

prune:
	docker system prune -af --volumes

ps:
	docker ps

logs:
	docker compose -f $(DEV_COMPOSE) logs -f

restart:
	docker compose -f $(DEV_COMPOSE) restart