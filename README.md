# cyberswiss

Suite avanzada de ciberseguridad self-hosted para pentesting / red team / hacking ético: gestión de engagements y hallazgos, orquestación de herramientas reales de recon/escaneo (nmap, subfinder, httpx, nuclei, etc.) en contenedores aislados, y biblioteca de conocimiento buscable con foco en OWASP Top 10.

Pensada para uso personal, desplegada en infraestructura propia vía Docker Compose.

## Stack

- Backend: Python 3.12 + FastAPI + SQLAlchemy (async) + PostgreSQL 16
- Cola de jobs: Redis 7 + Dramatiq, con streaming de logs en vivo vía WebSocket
- Aislamiento de ejecución: cada herramienta corre en un contenedor Docker efímero con límites de recursos
- Frontend: React + TypeScript + Vite + Tailwind (tema dark hacker/terminal)
- Búsqueda: PostgreSQL full-text search

## Desarrollo local

```bash
cp .env.example .env   # ajustar secrets
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

- Backend: http://localhost:8000/health
- Frontend: http://localhost:5173

## Producción / despliegue propio

```bash
cp .env.example .env   # ajustar secrets, AUTH_DISABLED=false
docker compose up --build -d
```

El worker necesita acceso al socket Docker del host (`/var/run/docker.sock`) para lanzar contenedores efímeros por cada herramienta ejecutada — mismo patrón usado por herramientas como Portainer o Drone CI. Es un trade-off aceptado para self-hosting personal.

## Estructura

```
backend/app/
  core/          configuración, seguridad, docker_runner (aislamiento por job)
  models/        modelos SQLAlchemy
  api/routes/    endpoints FastAPI
  tools/         adapters por herramienta (subfinder, httpx, nuclei, nmap, ...)
  pipelines/     motor de encadenamiento de jobs
  workers/       actors de Dramatiq
  knowledge/     ingesta y búsqueda de la biblioteca de conocimiento
  reports/       export de reportes (Markdown/PDF)
frontend/src/    UI en React
tool-images/     imágenes Docker con las herramientas de pentesting preinstaladas
```

## Roadmap

1. ~~Fase 0 — Bootstrap~~
2. ~~Fase 1 — Auth + Engagements~~
3. ~~Fase 2 — Motor de ejecución de herramientas (subfinder, httpx, nuclei)~~
4. ~~Fase 3 — Pipelines encadenados + más herramientas (nmap, gobuster, whatweb)~~
5. Fase 4 — Findings + Biblioteca de conocimiento (foco OWASP Top 10)
6. Fase 5 — Reportes (post-MVP)
