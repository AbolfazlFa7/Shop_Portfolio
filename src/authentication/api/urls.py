from ninja.router import Router

from authentication.api.views import otp, user

router = Router(tags=["Authentication"])

router.add_router("/otp", otp.router)
router.add_router("", user.router)
# router.add_router("", social_login.router)
