from fastapi import FastAPI

app = FastAPI()


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

    return {
        "error": f"Task {task_id} not found",
        "status code": 404
    }
