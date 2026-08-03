import sqlite3
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


app = FastAPI()


class Task(BaseModel):
    title: str


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

    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)",
                       ("Learn FastAPI", 1))
        cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)",
                       ("Build API", 0))
        cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)",
                       ("Push to GitHub", 1))

    conn.commit()
    conn.close()


@app.on_event("startup")
def startup():
    init_db()
    seed_db()


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
         
    return [dict(row) for row  in rows]


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
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (title, 0))
    conn.commit()
    new_id = cursor.lastrowid
    new_task = conn.execute("SELECT * FROM tasks WHERE id = ?",
                            (new_id,)).fetchone()
    conn.close()

    return dict(new_task)


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    '''update a single Task'''
    for t in tasks:
        if t["id"] == task_id:
            t["title"] = task.title
            return t

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"task {task_id} not found"
    )


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    '''delete a single Task using id'''
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"task {task_id} not found"
    )
