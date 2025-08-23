# OSINT Microservice: [Service Name]

## 1. Overview

This microservice is responsible for [briefly describe the service's purpose, e.g., "scraping social media profiles based on user identifiers"]. It is part of a larger OSINT application for law enforcement.

This project is built with Python, FastAPI, and Celery, and is containerized using Docker.

## 2. Setup & Installation

### Prerequisites

- Docker
- Docker Compose

### Configuration

1. **API Key:** Open the `docker-compose.yaml` file and change the default `API_KEY` environment variable to a strong, unique secret.

    ```yaml
    environment:
      - API_KEY=your-new-secure-secret-key
    ```

2. **Dependencies:** Add any required Python libraries for this specific service to the `requirements.txt` file.

## 3. How to Run (Local Development)

This project includes simple scripts to manage the Docker Compose environment.

### To start the service

Execute the `start-dev.sh` script. This will build the Docker images (if they don't exist) and start the API, worker, Redis, and PostgreSQL containers in detached mode.

```bash
chmod +x start-dev.sh
./start-dev.sh
