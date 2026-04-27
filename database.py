from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# Резервный URL: используется только при локальной разработке
LOCAL_DATABASE_URL = "postgresql://postgres:12345678@localhost:5432/campus"

# Переменная окружения: на Render данные берутся из системы (DATABASE_URL), 
# если её нет — подключается локальная БД. Это делает код универсальным.
DATABASE_URL = os.environ.get("DATABASE_URL", LOCAL_DATABASE_URL)

# Engine: основной объект SQLAlchemy, который отвечает за соединение с PostgreSQL
engine = create_engine(DATABASE_URL)

# SessionLocal: фабрика сессий; каждая сессия — это конкретное «окно» для работы с данными
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: базовый класс, от которого будут наследоваться все модели (таблицы) в проекте
Base = declarative_base()