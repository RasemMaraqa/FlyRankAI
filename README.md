
# FlyRank Backend Track - Assignment 2

This project upgrades the FastAPI Task Manager from Assignment 1 by replacing the temporary in-memory Python list with a persistent **SQLite** database (`tasks.db`). All API endpoints remain identical, but task data now survives server restarts.

---
## How to Install & Run

1. **Clone the repo and enter the folder:**
   ```bash
   git clone https://github.com/RasemMaraqa/FlyRankAI.git

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


---
## 🚀 Why SQLite?
- **Persistence:** All updates are saved directly to `tasks.db` on disk, preserving data when the server restarts.
- **Zero Configuration:** Uses Python's native `sqlite3` standard library, eliminating the need for an external server setup.
- **Single-File Storage:** Lightweight and portable, allowing easy local database management.

---
## 📁 Database Details & Rules
- **Database File:** `tasks.db` lives in the project root folder.
- **Git Ignored:** Included inside `.gitignore` so fresh clones create their own clean database.
- **Auto-Initialization & Seeding:** Tables are created automatically on launch. If `tasks.db` does not exist, 3 default tasks are automatically inserted.

---


# Manual SQL Exploration (Stage 4):
<img width="584" height="373" alt="image" src="https://github.com/user-attachments/assets/c62cfb2b-5933-4411-add3-92837a942649" />

# FlyRank Backend Track - Assignment 1

A simple to-do list API built with Python and FastAPI for the FlyRank Internship.

# Swagger UI Screenshot :


<img width="1574" height="617" alt="Screenshot 2026-07-25 132807" src="https://github.com/user-attachments/assets/25cd5ce3-912b-450f-a47c-1b9b3011ed83" />






