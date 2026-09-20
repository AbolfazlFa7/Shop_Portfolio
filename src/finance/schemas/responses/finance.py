from ninja import ModelSchema, Schema

from finance.models import Wallet, WalletTransaction


class WalletResponseSchema(ModelSchema):
    class Meta:
        model = Wallet
        fields = [
            "id",
            "user",
            "is_active",
            "balance",
            "card_number",
            "shaba_number",
            "account_number",
        ]


class WalletTransactionResponseSchema(ModelSchema):
    class Meta:
        model = WalletTransaction
        fields = [
            "id",
            "wallet",
            "amount",
            "balance_before",
            "balance_after",
            "type",
            "status",
            "transaction_group_id",
            "reference_id",
            "created_at",
        ]


class DepositToWalletResponseSchema(Schema):
    payment_url: str
