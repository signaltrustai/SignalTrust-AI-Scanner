.PHONY: help build up down logs test setup clean

help: ## Show this help message
	@echo "SignalTrust EU Multi-Agent System - Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

setup: ## Initial setup - create .env from example
	@echo "Setting up environment..."
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "✅ Created .env file"; \
		echo "⚠️  Please edit .env and add your API keys"; \
	else \
		echo "⚠️  .env file already exists"; \
	fi

build: ## Build all Docker images
	@echo "Building all agents..."
	docker compose build

up: ## Start all agents
	@echo "Starting all agents..."
	docker compose up -d
	@echo "Waiting for services to be ready..."
	@sleep 5
	@docker compose ps

down: ## Stop all agents
	@echo "Stopping all agents..."
	docker compose down

logs: ## Show logs from all agents
	docker compose logs -f

logs-coordinator: ## Show coordinator logs
	docker compose logs -f coordinator

logs-crypto: ## Show crypto agent logs
	docker compose logs -f crypto_agent

logs-stock: ## Show stock agent logs
	docker compose logs -f stock_agent

logs-whale: ## Show whale agent logs
	docker compose logs -f whale_agent

logs-news: ## Show news agent logs
	docker compose logs -f news_agent

logs-supervisor: ## Show supervisor logs
	docker compose logs -f supervisor

test: ## Run all tests
	@echo "Running tests..."
	./test_agents.sh

test-quick: ## Quick health check of all agents
	@echo "Quick health check..."
	@for port in 8000 8001 8002 8003 8004; do \
		echo -n "Port $$port: "; \
		curl -s http://localhost:$$port/health | grep -q "healthy" && echo "✅" || echo "❌"; \
	done

restart: ## Restart all agents
	@echo "Restarting all agents..."
	docker compose restart

restart-coordinator: ## Restart coordinator
	docker compose restart coordinator

restart-crypto: ## Restart crypto agent
	docker compose restart crypto_agent

restart-stock: ## Restart stock agent
	docker compose restart stock_agent

restart-whale: ## Restart whale agent
	docker compose restart whale_agent

restart-news: ## Restart news agent
	docker compose restart news_agent

ps: ## Show status of all containers
	docker compose ps

clean: ## Remove all containers and volumes
	@echo "Cleaning up..."
	docker compose down -v
	@echo "✅ Cleaned up"

rebuild: clean build up ## Clean, rebuild, and start all agents

workflow: ## Run a test workflow
	@echo "Running test workflow..."
	@curl -X POST http://localhost:8000/run-workflow \
		-H "Content-Type: application/json" \
		-d '{"symbol":"BTC/USDT","ticker":"AAPL","network":"btc","topics":["crypto","stocks"]}' \
		| python3 -m json.tool

agents: ## List all available agents
	@curl -s http://localhost:8000/agents | python3 -m json.tool

docs: ## Open API documentation in browser
	@echo "Opening API documentation..."
	@echo "Coordinator: http://localhost:8000/docs"
	@which open > /dev/null && open http://localhost:8000/docs || xdg-open http://localhost:8000/docs || echo "Please open http://localhost:8000/docs in your browser"

install-deps: ## Install Python dependencies locally (for development)
	pip install -r requirements.txt
	cd agents/crypto_agent && pip install -r requirements.txt
	cd agents/stock_agent && pip install -r requirements.txt
	cd agents/whale_agent && pip install -r requirements.txt
	cd agents/news_agent && pip install -r requirements.txt
	cd agents/supervisor && pip install -r requirements.txt
	cd agents/coordinator && pip install -r requirements.txt

dev: ## Start in development mode with hot reload
	@if [ ! -f docker-compose.override.yml ]; then \
		cp docker-compose.override.yml.example docker-compose.override.yml; \
		echo "✅ Created docker-compose.override.yml for development"; \
	fi
	docker compose up

shell-coordinator: ## Open shell in coordinator container
	docker compose exec coordinator /bin/bash

shell-crypto: ## Open shell in crypto agent container
	docker compose exec crypto_agent /bin/bash

shell-stock: ## Open shell in stock agent container
	docker compose exec stock_agent /bin/bash

shell-whale: ## Open shell in whale agent container
	docker compose exec whale_agent /bin/bash

shell-news: ## Open shell in news agent container
	docker compose exec news_agent /bin/bash
