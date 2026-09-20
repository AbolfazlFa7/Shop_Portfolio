from ninja import Schema


class DetailResponse(Schema):
    detail: str


class TokenResponse(Schema):
    access_token: str
    refresh_token: str
