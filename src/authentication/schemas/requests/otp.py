from ninja import Schema

from common.schemas.common import PhoneNumber


class SendOTP_SMS_Schema(Schema):
    phone_number: PhoneNumber
