from typing import Literal

from django.db.models import QuerySet
from django.shortcuts import aget_object_or_404

from finance.models import Wallet, WalletTransaction


async def get_wallet_by_id_for_owner(owner_id: int, wallet_id: int) -> Wallet:
    qs = Wallet.objects.filter(user_id=owner_id, id=wallet_id, is_active=True)

    return await aget_object_or_404(qs)


async def is_wallet_owner(
    owner_id: int,
    wallet_id: int,
    wallet_type: Literal["PERSONAL", "BUSINESS"] = "BUSINESS",
) -> bool:
    qs = Wallet.objects.filter(
        user_id=owner_id, id=wallet_id, is_active=True, type=wallet_type
    )

    return await qs.aexists()


def list_wallet_transactions_for_owner(
    owner_id: int, business_id: int
) -> QuerySet[WalletTransaction]:
    queryset = WalletTransaction.objects.filter(
        wallet__business_id=business_id,
        wallet__user_id=owner_id,
    ).order_by("-created_at")
    return queryset


def list_wallets_for_owner(owner_id: int) -> QuerySet[Wallet]:
    queryset = Wallet.objects.filter(user_id=owner_id, is_active=True).order_by(
        "-balance"
    )
    return queryset
