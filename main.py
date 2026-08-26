import sqlite3
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import os
import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI()


class Task(BaseModel):
    title: str
    

class TaskUpdate(BaseModel):
    title: str
    done: bool


def get_db():
    conn = psycopg.connect(DATABASE_URL, row_factory=dict_row)
    return conn


def init_db():
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    done BOOLEAN DEFAULT FALSE
                );
            """)
            conn.commit()


def seed_db():
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM tasks;")
            count = cursor.fetchone()["count"]

            if count == 0:
                cursor.execute("""
                    INSERT INTO tasks (title, done) VALUES 
                    (%s, %s),
                    (%s, %s),
                    (%s, %s);
                """, ("Learn FastAPI", True, "Build API", False, "Push to GitHub", True))
                conn.commit()


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
