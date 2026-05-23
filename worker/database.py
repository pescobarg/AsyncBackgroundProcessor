import os
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

MAX_RETRIES = 10

for attempt in range(MAX_RETRIES):
    try:
        engine = create_engine(DATABASE_URL)

        connection = engine.connect()

        print("PostgreSQL connected successfully!")

        connection.close()

        break

    except Exception as e:
        print(f"Database connection failed: {e}")

        if attempt == MAX_RETRIES - 1:
            raise e

        print("Retrying in 5 seconds...")

        time.sleep(5)

SessionLocal = sessionmaker(
autocommit=False,
autoflush=False,
bind=engine
)

Base = declarative_base()
