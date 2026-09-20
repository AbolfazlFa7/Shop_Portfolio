from django.contrib.auth.base_user import BaseUserManager

from common.services.otp import TimeBased_OTP


class UserManager(BaseUserManager):
    def create_user(
        self,
        phone_number: str,
        password: str | None = None,
        **extra_fields,
    ):
        user = self.model(
            phone_number=phone_number,
            **extra_fields,
        )

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)

        return user

    def create_superuser(
        self,
        phone_number: str,
        password: str,
        **extra_fields,
    ):
        extra_fields.setdefault("is_superuser", True)

        user = self.create_user(
            phone_number=phone_number,
            password=password,
            **extra_fields,
        )

        from authentication.models import UserTOTP

        secret = TimeBased_OTP.generate_secret()
        UserTOTP.objects.create(user=user, secret_key=secret)

        print("\n" + "=" * 70)
        print("IMPORTANT: Save this secret in Google Authenticator")
        print(f"   Secret Key: {TimeBased_OTP.create_2FA_secret(secret)}")
        print(f"   Account: {user.email or user.phone_number}")
        print("=" * 70 + "\n")

        return user

    async def acreate_user(
        self,
        phone_number: str,
        password: str | None = None,
        **extra_fields,
    ):
        user = self.model(
            phone_number=phone_number,
            **extra_fields,
        )

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        await user.asave(using=self._db)

        return user

    async def acreate_superuser(
        self,
        phone_number: str,
        password: str,
        **extra_fields,
    ):
        extra_fields.setdefault("is_superuser", True)

        user = await self.acreate_user(
            phone_number=phone_number,
            password=password,
            **extra_fields,
        )

        from authentication.models import UserTOTP

        secret = TimeBased_OTP.generate_secret()
        await UserTOTP.objects.acreate(user=user, secret_key=secret)

        print("\n" + "=" * 70)
        print("IMPORTANT: Save this secret in Google Authenticator")
        print(f"   Secret Key: {TimeBased_OTP.create_2FA_secret(secret)}")
        print(f"   Account: {user.email or user.phone_number}")
        print("=" * 70 + "\n")

        return user
