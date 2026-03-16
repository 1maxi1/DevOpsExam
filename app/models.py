from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from .database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    reception_time: Mapped[str] = mapped_column(String, nullable=False)
    specialization: Mapped[str] = mapped_column(String, nullable=False)

    appointments: Mapped[list["Appointment"]] = relationship(
        "Appointment", back_populates="doctor"
    )


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    phone_number: Mapped[str] = mapped_column(String, nullable=False, index=True)
    sms_code: Mapped[str] = mapped_column(String, nullable=False)
    doctor_id: Mapped[int] = mapped_column(Integer, ForeignKey("doctors.id"))
    appointment_time: Mapped[str] = mapped_column(String, nullable=False)

    doctor: Mapped[Doctor] = relationship("Doctor", back_populates="appointments")


def seed_initial_data(engine: Engine) -> None:
    """
    Seed the database with the exam ticket data if tables are empty.
    """
    with Session(engine) as session:
        has_doctors = session.query(Doctor).first() is not None
        has_appointments = session.query(Appointment).first() is not None

        if has_doctors and has_appointments:
            return

        if not has_doctors:
            doctors = [
                Doctor(
                    id=1,
                    full_name="Ходяков Иван Валерьевич",
                    reception_time="08:00-15:00",
                    specialization="Стоматолог",
                ),
                Doctor(
                    id=2,
                    full_name="Чечевский Андрей Сергеевич",
                    reception_time="09:00-18:00",
                    specialization="Участковый врач",
                ),
                Doctor(
                    id=3,
                    full_name="Ерулина Жанна Аркадьевна",
                    reception_time="12:00-16:00",
                    specialization="Психолог",
                ),
                Doctor(
                    id=4,
                    full_name="Пастух Ольга Михайловна",
                    reception_time="07:00-10:00",
                    specialization="Лаборант",
                ),
            ]
            session.add_all(doctors)

        if not has_appointments:
            appointments = [
                Appointment(
                    id=1,
                    phone_number="+78986664502",
                    sms_code="5500",
                    doctor_id=2,
                    appointment_time="12:15",
                ),
                Appointment(
                    id=2,
                    phone_number="+79196663409",
                    sms_code="0208",
                    doctor_id=1,
                    appointment_time="13:00",
                ),
                Appointment(
                    id=3,
                    phone_number="+79265340071",
                    sms_code="3648",
                    doctor_id=4,
                    appointment_time="07:25",
                ),
            ]
            session.add_all(appointments)

        session.commit()
