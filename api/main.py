from fastapi import FastAPI
from redis import Redis
from rq import Queue

from tasks import process_task

app = FastAPI()

redis_conn = Redis(host="redis", port=6379)
queue = Queue(connection=redis_conn)


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "vibetask-api"
    }


@app.post("/tasks")
def create_task(payload: dict):
    task_data = payload.get("data")

    job = queue.enqueue(process_task, task_data)

    return {
        "message": "Task added to queue",
        "job_id": job.id
    }