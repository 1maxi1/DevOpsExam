from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import auth, models, schemas
from .database import get_db, init_db
from .schemas import AuthRequest, Token, AppointmentWithDoctor, DoctorBase

app = FastAPI(title="Приложение записи на прием к врачу")
templates = Jinja2Templates(directory="app/templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse, summary="Веб-интерфейс приложения")
def read_root(request: Request) -> HTMLResponse:
    """
    Веб-интерфейс для работы с приложением:
    логин, просмотр расписания и своих записей.
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.post("/auth/login", response_model=Token, summary="Аутентификация пациента")
def login(auth_request: AuthRequest, db: Session = Depends(get_db)) -> Token:
    """
    Аутентификация по паре номер телефона - код из СМС.
    """
    return auth.login(auth_request, db)


@app.get(
    "/doctors/schedule",
    response_model=list[DoctorBase],
    summary="Расписание приема врачей с указанием специализации",
)
def get_doctors_schedule(db: Session = Depends(get_db)) -> list[DoctorBase]:
    """
    Базовая функция №1 + дополнение:
    возвращает список врачей с расписанием приема и специализацией.
    """
    doctors = db.query(models.Doctor).all()
    return [DoctorBase.model_validate(d) for d in doctors]


@app.get(
    "/appointments",
    response_model=list[AppointmentWithDoctor],
    summary="Информация о записях пациента (требует аутентификации)",
)
def get_appointments_for_current_patient(
    current_phone: str = Depends(auth.get_current_phone),
    db: Session = Depends(get_db),
) -> list[AppointmentWithDoctor]:
    """
    Базовая функция №2:
    возвращает записи пациента, прошедшего аутентификацию.
    """
    appointments = (
        db.query(models.Appointment)
        .join(models.Doctor)
        .filter(models.Appointment.phone_number == current_phone)
        .all()
    )
    result: list[AppointmentWithDoctor] = []
    for appt in appointments:
        result.append(
            AppointmentWithDoctor(
                id=appt.id,
                phone_number=appt.phone_number,
                appointment_time=appt.appointment_time,
                doctor=schemas.DoctorBase.model_validate(appt.doctor),
            )
        )
    return result

