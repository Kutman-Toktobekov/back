from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from database import SessionLocal, engine
import models, schemas

# Создание таблиц: SQLAlchemy проверяет наличие таблиц в БД и создает их, если их нет
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Настройка CORS: позволяет фронтенду взаимодействовать с бэкендом, даже если они на разных доменах
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Функция получения сессии БД: открывает соединение и гарантированно закрывает его после запроса
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ================= AUTH =================

@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Регистрация: сохраняем email и пароль нового пользователя
    new_user = models.User(
        email=user.email,
        password=user.password
    )
    db.add(new_user)
    db.commit()
    return {"message": "User created"}

@app.post("/login")
def login(user: dict, db: Session = Depends(get_db)):
    # Логин: поиск пользователя в базе и простая проверка совпадения пароля
    db_user = db.query(models.User).filter(models.User.email == user.get("email")).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if db_user.password != user.get("password"):
        raise HTTPException(status_code=401, detail="Wrong password")

    return {"message": "Login successful"}

# ================= REPORT =================

@app.post("/report")
def create_report(report: schemas.ReportCreate, db: Session = Depends(get_db)):
    # Создание заявки: записываем координаты и описание, ставим начальный статус "pending"
    new_report = models.Report(
        title=report.title,
        description=report.description,
        lat=report.lat,
        lng=report.lng,
        status="pending"
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    return {
        "message": "Report created",
        "id": new_report.id
    }

@app.get("/reports")
def get_reports(db: Session = Depends(get_db)):
    # Получение списка: возвращает все найденные в базе заявки
    return db.query(models.Report).all()

# ================= UPDATE STATUS =================

@app.put("/report/{report_id}")
def update_status(report_id: int, status_update: schemas.StatusUpdate, db: Session = Depends(get_db)):
    # Обновление: находим заявку по ID и меняем её текущий статус
    report = db.query(models.Report).filter(models.Report.id == report_id).first()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    if status_update.status not in ["pending", "in_progress", "resolved"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    report.status = status_update.status
    db.commit()

    return {"message": f"Status updated to {status_update.status}"}

# ================= DELETE REPORT =================

@app.delete("/report/{report_id}")
def delete_report(report_id: int, db: Session = Depends(get_db)):
    # Удаление: находим запись и полностью стираем её из базы данных
    report = db.query(models.Report).filter(models.Report.id == report_id).first()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    db.delete(report)
    db.commit()

    return {"message": "Report deleted successfully"}

# ================= STATS =================

@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    # Статистика: считаем количество строк в таблице для каждого типа статуса
    total = db.query(models.Report).count()
    pending = db.query(models.Report).filter(models.Report.status == "pending").count()
    in_progress = db.query(models.Report).filter(models.Report.status == "in_progress").count()
    resolved = db.query(models.Report).filter(models.Report.status == "resolved").count()

    return {
        "total": total,
        "pending": pending,
        "in_progress": in_progress,
        "resolved": resolved
    }