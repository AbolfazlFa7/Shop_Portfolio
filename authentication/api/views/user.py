import logging

from ninja import Router, Status

from authentication.schemas.requests.user import (
    Login_Schema,
    RefreshToken_Schema,
    Register_Schema,
)
from authentication.services.auth_user import AuthUser
from authentication.services.otp import OTP
from common.permissions import IsAnonymous, permissions
from common.schemas.responses import DetailResponse, TokenResponse
from common.services.jwt import JWTAuth

logger = logging.getLogger(__name__)

router = Router()


@router.post("/login", response=TokenResponse)
@permissions(IsAnonymous)
async def login(request, payload: Login_Schema):
    logger.info(f"Login attempt for phone: {payload.phone_number}")
    await OTP.verify_otp(payload.phone_number, payload.code)

    data = await AuthUser.login(payload.phone_number)
    return Status(200, data)


@router.post("/register", response={201: TokenResponse})
@permissions(IsAnonymous)
async def register(request, payload: Register_Schema):
    logger.info(f"Registration attempt for phone: {payload.phone_number}")
    await OTP.verify_otp(payload.phone_number, payload.code)

    data = await AuthUser.register(payload.phone_number)
    return Status(201, data)


@router.post("/token/refresh", response=TokenResponse)
async def refresh_token(request, payload: RefreshToken_Schema):
    logger.info("Token refresh attempt")
    data = await AuthUser.refresh_token(payload.refresh_token)
    return Status(200, data)


@router.post("/logout", auth=JWTAuth(), response=DetailResponse)
async def logout(request, payload: RefreshToken_Schema):
    logger.info(f"Logout attempt for user {request.user.id}")
    data = await AuthUser.logout(payload.refresh_token, request.user.id)
    return Status(200, data)
