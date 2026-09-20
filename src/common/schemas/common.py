from typing import Annotated

from ninja import Field
from ninja.errors import ValidationError
from pydantic import AfterValidator

from common.normalizers import normalize_email, normalize_phone
from common.validators import password_validation


def validate_phone(value: str) -> str:
    return normalize_phone(value)


def validate_email(value: str) -> str:
    return normalize_email(value)


def validate_password(value: str) -> str:
    password_validation(value)
    return value


def validate_code(value: str) -> str:
    if not value.isdigit():
        raise ValidationError([{"code": "Code must be an integer"}])
    return value


PhoneNumber = Annotated[
    str,
    Field(examples=["09123456789", "+989123456789"]),
    AfterValidator(validate_phone),
]

Email = Annotated[
    str,
    Field(examples=["example@gmail.com"]),
    AfterValidator(validate_email),
]

Password = Annotated[
    str,
    Field(min_length=8, max_length=32),
    AfterValidator(validate_password),
]

Code = Annotated[
    str,
    Field(min_length=6, max_length=6, examples=["123456"]),
    AfterValidator(validate_code),
]
