# FlyRank Backend Track - Task Manager API

A FastAPI RESTful service for task management, upgraded from an in-memory setup to persistent PostgreSQL storage and containerized using Docker Compose. Built for the FlyRank Internship.

---

## Features

* CRUD Operations: Complete endpoints for creating, retrieving, updating, and deleting tasks.
* PostgreSQL Integration: Data persistence using PostgreSQL and native psycopg parameterized queries (%s placeholders).
* Automated Documentation: Interactive Swagger UI and ReDoc pages available out of the box.
* Dockerized Infrastructure: Multi-container setup orchestrating the FastAPI application and PostgreSQL database using Docker Compose.

---

## Project Structure

* main.py - Core FastAPI routes, database connectivity, table initialization, and auto-seeding logic.
* compose.yaml - Docker Compose configuration managing both api and db services.
* Dockerfile - Container specification for the Python FastAPI application environment.
* .env.example - Template file for environment variable setups.
* requirements.txt - Project dependencies.

---

## Environment Configuration

Create a .env file in your project root (used for local runs outside of Docker Compose):

`DATABASE_URL=postgresql://postgres:dev@localhost:5432/tasks`

(Note: Docker Compose automatically overrides this to postgresql://postgres:dev@db:5432/tasks to connect across internal container networks).

---

## Running with Docker Compose

1. Clone the repository:
   ```
   git clone https://github.com/RasemMaraqa/FlyRankAI.git
   cd FlyRankAI
   ```

3. Spin up the multi-container stack:
   ```
   docker compose up --build
   ```
4. Access the service:
   * Root Metadata: http://localhost:8000/
   * Health Check: http://localhost:8000/health
   * Swagger UI Docs: http://localhost:8000/docs
   * ReDoc Docs: http://localhost:8000/redoc

---

## API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| GET | `/` | API metadata |
| GET | `/health `| Application health check |
| GET |` /tasks `| Retrieve all tasks |
| GET | `/tasks/{task_id}` | Retrieve a single task by ID |
| POST | `/tasks` | Create a new task |
| PUT | `/tasks/{task_id}` | Update a task by ID |
| DELETE | `/tasks/{task_id}` | Delete a task by ID |

---

## Testing via PowerShell

# Get all tasks
```Invoke-RestMethod -Uri "http://localhost:8000/tasks" -Method Get```

# Create a task`
```Invoke-RestMethod -Uri "http://localhost:8000/tasks" -Method Post -ContentType "application/json" -Body '{"title": "Complete Stage 5", "done": false}'```

# Update a task
```Invoke-RestMethod -Uri "http://localhost:8000/tasks/1" -Method Put -ContentType "application/json" -Body '{"title": "Learn FastAPI & Docker", "done": true}'```

# Delete a task
```Invoke-RestMethod -Uri "http://localhost:8000/tasks/1" -Method Delete```

---

## Screenshots & Visuals

### Manual Database Verification
<img width="584" height="373" alt="Manual SQL Exploration" src="https://github.com/user-attachments/assets/c62cfb2b-5933-4411-add3-92837a942649" />

### Interactive Swagger UI Documentation
<img width="1574" height="617" alt="Swagger UI" src="https://github.com/user-attachments/assets/25cd5ce3-912b-450f-a47c-1b9b3011ed83" />
