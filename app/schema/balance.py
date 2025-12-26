from pydantic import BaseModel


class BalanceOut(BaseModel):
    user_id: str
    balance: int

class BalanceTopUpRequest(BaseModel):
    amount: int