from fastapi import APIRouter, Header, Depends
from app.application.dtos.balance_dtos import BalanceOut, BalanceTopUpRequest, BalancePayRequest
from app.application.service.auth_service import get_user_id_by_token
from app.application.service.balance_service import BalanceService
from app.core.dependencies import get_balance_service


router = APIRouter(prefix="/balance", tags=["Balance"])


@router.post("/top-up", response_model=BalanceOut)
async def top_up(
    request: BalanceTopUpRequest,
    authorization: str = Header(...),
    service: BalanceService = Depends(get_balance_service),
):
    token = authorization.replace("Bearer ", "")
    user_id = await get_user_id_by_token(token)
    balance = await service.top_up(user_id, request.amount)
    return BalanceOut(user_id=user_id, balance=balance)


@router.get("/", response_model=BalanceOut)
async def get_balance(
    authorization: str = Header(...),
    service: BalanceService = Depends(get_balance_service),
):
    token = authorization.replace("Bearer ", "")
    user_id = await get_user_id_by_token(token)
    balance = await service.get_balance(user_id)
    return BalanceOut(user_id=user_id, balance=balance)


@router.post("/pay", response_model=BalanceOut)
async def pay(
    request: BalancePayRequest,
    authorization: str = Header(...),
    service: BalanceService = Depends(get_balance_service),
):
    token = authorization.replace("Bearer ", "")
    user_id = await get_user_id_by_token(token)
    balance = await service.pay(user_id, request.amount)
    return BalanceOut(user_id=user_id, balance=balance)
