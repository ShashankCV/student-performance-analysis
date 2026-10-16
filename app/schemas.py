from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


class StudentFields(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    date_of_birth: date
    email: EmailStr | None = None
    phone: str | None = Field(default=None, min_length=5, max_length=30)
    course: str | None = Field(default=None, max_length=120)
    address: str | None = Field(default=None, max_length=300)
    enrollment_date: date | None = None

    @model_validator(mode="before")
    @classmethod
    def strip_text_fields(cls, values):
        if isinstance(values, dict):
            for field in ("name", "phone", "course", "address"):
                if isinstance(values.get(field), str):
                    values[field] = values[field].strip() or None
        return values

    @model_validator(mode="after")
    def require_contact_information(self):
        if not self.email and not self.phone:
            raise ValueError("At least one of email or phone is required")
        return self


class StudentCreate(StudentFields):
    pass


class StudentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    date_of_birth: date | None = None
    email: EmailStr | None = None
    phone: str | None = Field(default=None, min_length=5, max_length=30)
    course: str | None = Field(default=None, max_length=120)
    address: str | None = Field(default=None, max_length=300)
    enrollment_date: date | None = None

    @model_validator(mode="before")
    @classmethod
    def strip_text_fields(cls, values):
        if isinstance(values, dict):
            for field in ("name", "phone", "course", "address"):
                if isinstance(values.get(field), str):
                    values[field] = values[field].strip() or None
        return values


class StudentRead(StudentFields):
    model_config = ConfigDict(from_attributes=True)
    student_id: int