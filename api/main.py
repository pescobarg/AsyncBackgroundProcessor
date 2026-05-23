from fastapi import FastAPI
from redis import Redis
from rq import Queue

from database import Base
from database import engine
from database import SessionLocal

from models import Task

from tasks import process_task

app = FastAPI()

Base.metadata.create_all(bind=engine)

redis_conn = Redis(host="redis", port=6379)
queue = Queue(connection=redis_conn)


@app.get("/")
def health_check():
    return {
        "status": "ok"
    }


@app.post("/tasks")
def create_task(payload: dict):
    db = SessionLocal()

    task = Task(
        data=payload.get("data"),
        status="PENDING"
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    job = queue.enqueue(process_task, task.id)

    return {
        "message": "Task added",
        "task_id": task.id,
        "job_id": job.id,
        "status": task.status
    }


@app.get("/tasks")
def get_tasks():
    db = SessionLocal()

    tasks = db.query(Task).all()

    return tasks