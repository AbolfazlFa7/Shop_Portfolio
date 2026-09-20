from ninja import Field, Schema


class GoogleLoginCallback_Schema(Schema):
    """
    Query parameters received by the Google OAuth callback view.
    """

    code: str | None = Field(
        None,
        description="Authorization code for the token exchange (successful response)",
    )

    state: str = Field(
        ...,
        description="CSRF protection token - MUST match the state sent in initial request",
    )

    scope: str | None = Field(
        None, description="Space-separated list of scopes the user granted"
    )

    error: str | None = Field(
        None, description="Error code if authentication failed (access_denied, etc.)"
    )

    error_description: str | None = Field(
        None, description="Human-readable error description for debugging"
    )

    error_uri: str | None = Field(
        None, description="URI with additional error information"
    )
