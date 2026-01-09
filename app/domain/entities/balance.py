from dataclasses import dataclass


@dataclass(frozen=True)
class Balance:
    user_id: str
    balance: int
