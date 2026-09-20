import re

from django.core.validators import EmailValidator
from ninja.errors import ValidationError


def normalize_email(email: str) -> str:
    """Normalize email

    Args:
        email (str): user

    Raises:
        ValidationError: if user add dot trick after @ sign

    Returns:
        str: Normalize email to lower case and remove whitespaces, and also check for dot trick, and normailze it to normal email
    """

    email = email.lower().strip()
    dj_email_validator = EmailValidator()
    dj_email_validator(email)
    reversed_email = email[::-1]
    suffix, prefix = re.findall(r"(.*?\..*?@)(.*)", reversed_email)[0]
    prefix = prefix.replace(".", "")
    normalized_email = prefix[::-1] + suffix[::-1]

    if normalized_email.count(".") > 1:
        raise ValidationError(
            [{"email": "Your email is not in the correct format"}])

    return normalized_email


def normalize_phone(phone: str) -> str:
    """Normalize Phone
    Args:
        phone (str):
            example: +989123456789
            or: 09123456789
            or: 9123456789

    Raises:
        ValidationError: if phone number is not valid, and not in correct format

    Returns:
        str: if phone number has country code, turn it to 0, and return it
        example:
            +989123456789 -> 09123456789
            09123456789 -> 09123456789
    """
    match = re.findall(r"^(\+98|0)?(9\d{9})$", phone)
    if match:
        return "0" + match[0][1]
    raise ValidationError([{"phone": "Invalid Phone Number"}])
