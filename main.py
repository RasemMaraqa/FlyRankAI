import sqlite3
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


app = FastAPI()


class Task(BaseModel):
    title: str
    

class TaskUpdate(BaseModel):
    title: str
    done: bool


def get_db():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            done INTEGER
            )
        """)

    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()
    cursor = conn.cursor()
    next_id = get_next_available_id()
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute("INSERT INTO tasks (id, title, done) VALUES (?,?, ?)",
                       (next_id, "Learn FastAPI", 1))
        next_id += 1
        cursor.execute("INSERT INTO tasks (id, title, done) VALUES (?,?, ?)",
                       (next_id, "Build API", 0))
        next_id += 1
        cursor.execute("INSERT INTO tasks (id, title, done) VALUES (?,?, ?)",
                       (next_id, "Push to GitHub", 1))

    conn.commit()
    conn.close()


@app.on_event("startup")
def startup():
    init_db()
    seed_db()


def get_next_available_id():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM tasks ORDER BY id ASC")
    existing_ids = [row[0] for row in cursor.fetchall()]
    conn.close()

    candidate_id = 1
    for current_id in existing_ids:
        if current_id == candidate_id:
            candidate_id += 1
        elif current_id > candidate_id:
            break

    return candidate_id


@app.get("/")
def read_root():
    '''Root endpoint describing the API'''
    return {"name": "Task API",
            "version": "1.0",
            "endpoints": ["/tasks"]}


@app.get("/health")
def health_check():
    '''health check endpoint'''
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks():
    conn = get_db()
    rows = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()

    return [dict(row) for row in rows]


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    conn = get_db()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?",
                       (task_id,)).fetchone()
    conn.close()

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found "
        )

    return dict(row)


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(body: Task):
    '''create a new Task'''
    title = body.title.strip()
    if not title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title cannot be empty"
        )

    next_id = get_next_available_id()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (id, title, done) VALUES (?,?, ?)",
                   (next_id, title, 0))
    conn.commit()

    new_task = conn.execute("SELECT * FROM tasks WHERE id = ?",
                            (next_id,)).fetchone()
    conn.close()

    return dict(new_task)


@app.put("/tasks/{task_id}")
def update_task(task_id: int, body: TaskUpdate):
    title = body.title.strip()
    if not title:
        raise HTTPException(
            status_code=status.HTTP_404_BAD_REQUEST,
            detail="title cannot be empty"
        )
    conn = get_db()
    cursor = conn.cursor()
    isexist = cursor.execute(
        "SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if isexist is None:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"task {task_id} not found"
        )

    cursor.execute("UPDATE tasks SET title = ?, done = ? WHERE id = ?",
                   (title, int(body.done), task_id))
    conn.commit()
    updated_task = cursor.execute("SELECT * FROM tasks WHERE id = ?",
                                  (task_id,)).fetchone()
    conn.close()

    return dict(updated_task)


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    conn = get_db()
    cursor = conn.cursor()

    isexist = cursor.execute("SELECT * FROM tasks WHERE id = ?",
                             (task_id,)).fetchone()
    if isexist is None:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="task not found"
        )

    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    return {"msg": "deleted"}
