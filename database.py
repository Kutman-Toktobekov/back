from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# На Render используем переменную окружения DATABASE_URL
# Локально - твоя БД
LOCAL_DATABASE_URL = "postgresql://postgres:12345678@localhost:5432/campus"

DATABASE_URL = os.environ.get("DATABASE_URL", LOCAL_DATABASE_URL)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()