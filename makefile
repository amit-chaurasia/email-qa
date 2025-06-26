# Makefile for Email Extractor API (FastAPI + Ollama + Mistral)

.DEFAULT_GOAL := up

ENV_FILE := .env

up:
	@echo "🚀 Starting containers..."
	docker compose up -d

pull-model:
	@echo "📦 Pulling mistral model into Ollama..."
	docker exec -it ollama ollama pull mistral

rebuild:
	@echo "🔧 Rebuilding and restarting containers..."
	docker compose down
	docker compose up --build -d

down:
	@echo "🧹 Stopping containers..."
	docker compose down

logs:
	docker compose logs -f

curl:
	curl -X POST http://localhost:8000/extract \
	     -H "Content-Type: text/plain" \
	     --data-binary @email.txt