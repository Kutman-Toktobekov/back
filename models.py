from sqlalchemy import Column, Integer, String, Float
from database import Base

# Класс User: описывает таблицу "users" для хранения данных пользователей
class User(Base):
    __tablename__ = "users"

    # primary_key=True: уникальный идентификатор пользователя
    # index=True: ускоряет поиск по этому полю
    id = Column(Integer, primary_key=True, index=True)
    
    # unique=True: гарантирует, что в базе не будет двух одинаковых email
    email = Column(String, unique=True)
    
    # password: хранит пароль в виде строки
    password = Column(String)


# Класс Report: описывает таблицу "reports" для хранения заявок о проблемах
class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    
    # title: краткий заголовок проблемы
    title = Column(String)
    
    # description: подробное описание проблемы
    description = Column(String)
    
    # status: состояние заявки (по умолчанию — "pending")
    status = Column(String, default="pending")
    
    # lat и lng: координаты места происшествия (числа с плавающей точкой)
    lat = Column(Float)
    lng = Column(Float)