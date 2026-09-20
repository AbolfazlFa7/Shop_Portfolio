from collections.abc import Callable
from functools import wraps
from http import HTTPStatus
from inspect import iscoroutinefunction

from ninja.errors import HttpError


def permissions(*permissions: Callable):
    def decorator(func):

        if iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(request, *args, **kwargs):
                for permission in permissions:
                    if iscoroutinefunction(permission):
                        await permission(request, *args, **kwargs)
                    else:
                        permission(request)

                return await func(request, *args, **kwargs)

            return async_wrapper

        else:

            @wraps(func)
            def sync_wrapper(request, *args, **kwargs):
                for permission in permissions:
                    permission(request)

                return func(request, *args, **kwargs)

            return sync_wrapper

    return decorator


def IsAnonymous(request, *args, **kwargs):
    token = request.headers.get("Authorization")

    authenticated = False

    if token:
        parts = token.split()
        authenticated = len(parts) == 2

    if authenticated:
        raise HttpError(HTTPStatus.FORBIDDEN, "You are already authenticated.")


def IsAdmin(request, *args, **kwargs):
    user = request.user

    if not user.is_superuser:
        raise HttpError(HTTPStatus.FORBIDDEN, "You are not an admin.")
