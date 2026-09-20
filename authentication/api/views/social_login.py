from http import HTTPStatus

from ninja import Query, Router, Status
from ninja.errors import HttpError

from authentication.schemas.requests.social_login import GoogleLoginCallback_Schema
from authentication.services.social_login import GoogleLoginService
from common.permissions import IsAnonymous, permissions
from common.schemas.responses import TokenResponse

router = Router()


@router.get("/social/google/callback", response=TokenResponse)
@permissions(IsAnonymous)
async def google_login_callback(request, query: Query[GoogleLoginCallback_Schema]):
    if query.error:
        error_response = {
            "error": "google_oauth_error",
            "error_code": query.error,
            "error_description": query.error_description,
            "error_uri": query.error_uri,
        }
        raise HttpError(HTTPStatus.BAD_REQUEST, error_response)

    if not query.code:
        raise HttpError(HTTPStatus.BAD_REQUEST, "Authorization code not provided")

    # if query.scope:
    #     logger.info(f"User granted scopes: {query.scope}")

    service = GoogleLoginService(query.code)
    data, status_code = await service.get_user_info()

    return Status(status_code, data)
