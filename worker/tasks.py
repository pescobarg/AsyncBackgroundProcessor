import time


def process_task(data: str):
    print(f"[WORKER] Processing task: {data}")

    time.sleep(10)

    print(f"[WORKER] Task completed: {data}")