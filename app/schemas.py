from pydantic import BaseModel


class DoctorBase(BaseModel):
    id: int
    full_name: str
    reception_time: str
    specialization: str

    class Config:
        from_attributes = True


class AppointmentBase(BaseModel):
    id: int
    phone_number: str
    appointment_time: str
    doctor_id: int

    class Config:
        from_attributes = True


class AppointmentWithDoctor(BaseModel):
    id: int
    phone_number: str
    appointment_time: str
    doctor: DoctorBase

    class Config:
        from_attributes = True


class AuthRequest(BaseModel):
    phone_number: str
    sms_code: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

