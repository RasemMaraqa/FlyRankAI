# Task Management CRUD API

A simple to-do list API built with Python and FastAPI for the FlyRank Internship.

## How to Install & Run

1. **Clone the repo and enter the folder:**
   ```bash
   git clone https://github.com/RasemMaraqa/FlyRankAI-A1.git

2. **Create a virtual environment & Activate it:**
   ```bash
   python3 -m venv venv
   .\venv\Scripts\Activate.ps1
3. **install dependencies:**
   ```bash
   pip install -r requirements.txt

4. **Start The Server :**
   ```bash
   uvicorn main:app --reload

## Example :
  ```bash
  curl -i http://localhost:8000/tasks/1
  ```
## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/tasks` | Get all tasks |
| GET | `/tasks/{task_id}` | Get one task |
| POST | `/tasks` | Create a task |
| PUT | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |

# Swagger UI Screenshot :


<img width="1574" height="617" alt="image" src="https://github.com/user-attachments/assets/ce7d246e-bd8d-44a1-a141-054683b3cf41" />




