# 📧 Email Extractor API (FastAPI + Ollama + Mistral)

This project provides a FastAPI-based web service that extracts the latest composed email from a raw thread using `email-reply-parser` and locally hosted open-source LLMs (via Ollama). It's ideal for pulling only the most recent human-composed message from multi-reply email chains.

---

## 🚀 Features

-   Accepts raw email input via plain text (`text/plain`)
-   Uses `email-reply-parser` to isolate the most recent composed message
-   Sends cleaned prompt to an LLM (e.g. Mistral) running locally via Ollama
-   Returns clean body content with greeting, message, and sign-off

---

## 🧱 Project Structure

```
email-extractor/
├── app/
│   └── main.py               # FastAPI app logic
├── .env                      # Environment variables (OLLAMA_HOST, OLLAMA_MODEL)
├── Dockerfile                # Docker build for FastAPI service
├── requirements.txt          # Python dependencies
├── docker-compose.yml        # Runs Ollama + API service
```

---

## 🛠 Makefile Commands

The following commands simplify Docker and API interaction:

| Command           | Description                             |
| ----------------- | --------------------------------------- |
| `make up`         | Start all containers in the background  |
| `make pull-model` | Pull the Mistral model into Ollama      |
| `make rebuild`    | Rebuild containers and restart services |
| `make down`       | Stop all services                       |
| `make logs`       | View real-time logs                     |
| `make curl`       | Send a sample email from `email.txt`    |

> ✅ Recommended first-time setup:
>
> ```bash
> make up
> make pull-model
> ```

---

## ⚙️ Setup Instructions

### 1. Clone & prepare

```bash
git clone <repo>
cd email-extractor
```

### 2. Create `.env` file

```env
OLLAMA_HOST=http://ollama:11434
OLLAMA_MODEL=mistral
```

### 3. Build & start services

```bash
docker compose up --build -d
```

### 4. Pull model into Ollama (first-time only)

```bash
docker exec -it ollama ollama pull mistral
```

---

## 🧪 How to Use

### ▶️ Plain text input

```bash
curl -X POST http://localhost:8000/extract \
     -H "Content-Type: text/plain" \
     --data-binary @email.txt
```

---

## 🧰 Troubleshooting

### ❌ API returns `model not found`

You forgot to pull the model:

```bash
docker exec -it ollama ollama pull mistral
```

### ❌ API returns `Failed to connect to Ollama`

Ensure:

-   `.env` or Docker `environment:` sets `OLLAMA_HOST=http://ollama:11434`
-   `ollama` container is running
-   You’re using Docker Compose, not `localhost` from within the `api` container

### ✅ Verify Ollama is reachable

```bash
docker compose exec api curl http://ollama:11434/api/tags
```

Should return model list.

---

## 📜 License

MIT

---

Let me know if you want to:

-   Add a `Makefile`
-   Bundle `.http` files for REST client testing
-   Extend to support summarization or intent detection
