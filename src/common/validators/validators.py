from ninja.errors import ValidationError


def password_validation(value: str):
    SPECIAL_CHARS = frozenset("!@#$%^&*()-_=+")
    has_lower = False
    has_upper = False
    has_digit = False
    has_special = False

    for char in value:
        if char.isspace():
            raise ValidationError(
                [{"password": "Password must not contain whitespace."}]
            )

        if char.islower():
            has_lower = True
        elif char.isupper():
            has_upper = True
        elif char.isdigit():
            has_digit = True
        elif char in SPECIAL_CHARS:
            has_special = True
        else:
            raise ValidationError([{"password": f"Unsupported character: {char}"}])

    if not has_lower:
        raise ValidationError(
            [{"password": "Password must contain at least one lowercase letter."}]
        )

    if not has_upper:
        raise ValidationError(
            [{"password": "Password must contain at least one uppercase letter."}]
        )

    if not has_digit:
        raise ValidationError(
            [{"password": "Password must contain at least one digit."}]
        )

    if not has_special:
        raise ValidationError(
            [{"password": "Password must contain at least one special character."}]
        )
