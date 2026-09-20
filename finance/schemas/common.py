from typing import Annotated

from ninja import Field

Money_Amount = Annotated[
    int,
    Field(
        ge=1000,
        le=500000000,
        description="Amount in Tooman)",
    ),
]

Bank_Account_Number = Annotated[
    str,
    Field(
        pattern=r"^IR[0-9]{24}$",
        min_length=26,
        max_length=26,
        description="Sheba number format: IR followed by 24 digits",
        examples=["IR540560004120002717448001"],
    ),
]
