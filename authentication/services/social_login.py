from http import HTTPStatus

import httpx
from django.conf import settings
from ninja.errors import HttpError

from authentication.models import User
from common.normalizers import normalize_email
from common.services.jwt import AsyncJWTService


class GoogleLoginService:
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

    def __init__(self, code: str):
        self.code = code
        self.token_data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }

    async def get_user_info(self):
        """
        1. Exchanges the OAuth2 code for Google tokens.
        2. Validates the access token.
        3. Fetches user info from Google using the access token.
        4. Validates the email and its verification status.
        5. Logs the user in or returns an error.
        """

        async with httpx.AsyncClient(timeout=5) as client:
            try:
                token_response = await client.post(
                    url=self.TOKEN_URL,
                    data=self.token_data,
                )
                token_response.raise_for_status()
            except httpx.HTTPError as e:
                raise HttpError(
                    HTTPStatus.BAD_GATEWAY,
                    {
                        "error": "Failed to exchange code for tokens",
                        "details": str(e),
                    },
                )

            tokens = token_response.json()

            access_token = tokens.get("access_token")
            if not access_token:
                raise HttpError(HTTPStatus.BAD_REQUEST, "Missing access token")

            try:
                userinfo_response = await client.get(
                    self.USERINFO_URL,
                    headers={
                        "Authorization": f"Bearer {access_token}",
                    },
                )
                userinfo_response.raise_for_status()
            except httpx.HTTPError as e:
                raise HttpError(
                    HTTPStatus.BAD_GATEWAY,
                    {
                        "error": "Failed to fetch user info",
                        "details": str(e),
                    },
                )

        userinfo = userinfo_response.json()

        email = userinfo.get("email")
        email_verified = userinfo.get("email_verified", False)

        if not email:
            raise HttpError(HTTPStatus.BAD_REQUEST, "Email not provided by Google")

        if not email_verified:
            raise HttpError(HTTPStatus.BAD_REQUEST, "Email not verified by Google")

        return await self._login(email)

    @staticmethod
    async def _login(email: str):
        """
        1. Normalizes the email address.
        2. Validates the email format.
        3. Checks if a user with the email exists.
        4. Generates a JWT token for the user if found.
        5. Returns the token.
        """
        email = normalize_email(email)

        user = await User.objects.filter(email=email).afirst()

        if not user:
            raise HttpError(HTTPStatus.NOT_FOUND, "User not found")

        jwt = AsyncJWTService()
        token = await jwt.create_pair(user)

        return token, HTTPStatus.OK
