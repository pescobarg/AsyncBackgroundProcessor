import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import OperationalError

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

MAX_RETRIES = 10

for attempt in range(MAX_RETRIES):
    try:
        with engine.connect() as connection:
            print("PostgreSQL connected successfully!")
            break

    except OperationalError as e:
        print(f"Database connection failed: {e}")

        if attempt == MAX_RETRIES - 1:
            raise

        print("Retrying in 5 seconds...")
        time.sleep(5)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()