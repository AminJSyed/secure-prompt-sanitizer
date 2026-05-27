# Secure Prompt Sanitizer

Secure Prompt Sanitizer is a local-first React and FastAPI application that helps developers sanitize logs, configs, screenshots, errors, and API output before sharing them with public AI tools.

The goal is simple: reduce the risk of accidentally exposing secrets such as tokens, passwords, API keys, database URLs, cookies, private IPs, local file paths, or internal details while debugging with AI.

## Why this project matters

Developers often copy logs, stack traces, screenshots, configuration files, and terminal output into AI tools for troubleshooting.

These inputs can accidentally contain sensitive values.

Secure Prompt Sanitizer helps by detecting and masking sensitive data locally before generating a safer AI-ready query.

## Features

- React frontend built with Vite
- FastAPI backend
- Local secret detection and masking
- Screenshot paste support
- File upload support
- OCR support for screenshots and images
- Manual masking list for custom sensitive values
- Generated safe query for public AI tools
- Dockerized frontend and backend
- Local-first design
- No cloud AI calls by default

## Tech Stack

### Frontend

- React
- Vite
- CSS

### Backend

- Python
- FastAPI
- Uvicorn
- OCR processing
- Custom detection and masking logic

### DevOps

- Docker
- Docker Compose

## What it can detect

The sanitizer can detect and mask examples such as:

- Bearer tokens
- API keys
- Password assignments
- Cookies
- Database URLs
- Private IP addresses
- Local paths
- Secret-like configuration values

Example input:

```text
password=DemoPassword123 Authorization: Bearer abc123

Sanitized output:

<SECRET_ASSIGNMENT> Authorization: Bearer <TOKEN>
Project Structure
secure-prompt-sanitizer/
  backend/
    api.py
    detectors.py
    ocr.py
    prompt_generator.py
    sanitizer.py

  frontend/
    src/
      App.jsx
      App.css
    package.json
    vite.config.js

  Dockerfile.backend
  Dockerfile.frontend
  docker-compose.yml
  requirements.txt
  README.md
Run with Docker

Build and start the full application:

docker compose up --build

Frontend:

http://127.0.0.1:5173

Backend health check:

http://127.0.0.1:8000/health

API docs:

http://127.0.0.1:8000/docs
Run backend manually
source .venv/bin/activate
uvicorn backend.api:app --host 127.0.0.1 --port 8000 --reload

Test health:

curl http://127.0.0.1:8000/health

Test sanitize endpoint:

curl -X POST http://127.0.0.1:8000/sanitize \
  -F "text=password=DemoPassword123 Authorization: Bearer abc123" \
  -F "user_goal=Help me safely share this error" \
  -F "manual_masks="
Run frontend manually
cd frontend
npm install
npm run dev

Open:

http://127.0.0.1:5173
Security Notes

This project is designed as a local-first sanitizer.

It does not call any AI API or send data to cloud services by default.

Users should still manually review sanitized output before sharing it publicly.

Do not commit real secrets, production logs, private keys, .env files, customer data, or internal credentials.

Roadmap
Add more detection rules
Improve OCR accuracy
Add better screenshot preview handling
Add unit tests for detector patterns
Add CI checks for backend and frontend
Add production-ready frontend build using Nginx
Add downloadable sanitized report
Author

Amin Jafar Syed
Principal Engineering Lead, DevSecOps, Cloud, Security, AI-Assisted Engineering and Automation

GitHub: https://github.com/AminJSyed