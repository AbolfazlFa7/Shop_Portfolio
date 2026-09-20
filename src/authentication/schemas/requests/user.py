from ninja import Schema

from common.schemas.common import Code, PhoneNumber


class Login_Schema(Schema):
    phone_number: PhoneNumber
    code: Code


class Register_Schema(Schema):
    phone_number: PhoneNumber
    code: Code


class RefreshToken_Schema(Schema):
    refresh_token: str
