import time

from database import SessionLocal
from models import Task



def process_task(task_id: int):
    db = SessionLocal()

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        return

    try:
        task.status = "PROCESSING"
        db.commit()

        print(f"Processing task {task.id}")

        time.sleep(10)

        task.status = "COMPLETED"
        db.commit()

        print(f"Task {task.id} completed")

    except Exception as e:
        task.status = "FAILED"
        db.commit()

        print(str(e))