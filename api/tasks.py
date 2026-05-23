import time


def process_task(data: str):
    print(f"Processing task: {data}")

    time.sleep(10)

    print(f"Task completed: {data}")

    return {
        "status": "completed",
        "data": data
    }