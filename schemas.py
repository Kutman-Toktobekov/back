from pydantic import BaseModel

# Схема для регистрации и логина: проверяет, чтобы email и пароль были строками
class UserCreate(BaseModel):
    email: str
    password: str

# Схема для создания заявки: 
# Гарантирует, что title и description — это текст, 
# а lat и lng — это числа с плавающей точкой (координаты)
class ReportCreate(BaseModel):
    title: str
    description: str
    lat: float
    lng: float

# Схема для обновления статуса администратором:
# Используется в PUT-запросе для изменения состояния заявки
class StatusUpdate(BaseModel):
    status: str