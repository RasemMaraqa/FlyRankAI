from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


app = FastAPI()


class Task(BaseModel):
    title: str


tasks = [
        {
            "id": 1,
            "title": "Start Journaling",
            "done": True
        },
        {
            "id": 2,
            "title": "Study for The Final",
            "done": False
        },
        {
            "id": 3,
            "title": "Talk with my Therpist ",
            "done": False
        },
        {
            "id": 4,
            "title": "Use HTTPException Next Commit",
            "done": False
        }
    ]


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
    '''get a All Tasks'''
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    '''get a single Task'''
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"task {task_id} not found"
    )


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: Task):
    if task.title.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="task title cannot be empty"
        )
    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "done": False
    }
    tasks.append(new_task)
    return new_task
