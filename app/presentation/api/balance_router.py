from fastapi import APIRouter, Header, Depends
from app.application.dtos.balance_dtos import BalanceOut, BalanceTopUpRequest, BalancePayRequest
from app.application.service.balance_service import BalanceService
from app.core.dependencies import get_balance_service, get_auth_client
from app.core.logging import logger
from app.infrastructure.auth.auth_client import AuthClient


router = APIRouter(prefix="/balance", tags=["Balance"])


@router.post("/top-up", response_model=BalanceOut)
async def top_up(
    request: BalanceTopUpRequest,
    authorization: str = Header(...),
    service: BalanceService = Depends(get_balance_service),
    auth_client: AuthClient = Depends(get_auth_client),
):
    token = authorization.replace("Bearer ", "")
    user_id = await auth_client.get_user_id_by_token(token)

    logger.info("Received top-up request: user_id=%s, amount=%s", user_id, request.amount)

    balance_int = await service.top_up(user_id, request.amount)

    logger.info("Returning BalanceOut: user_id=%s, balance=%s", user_id, balance_int)

    return BalanceOut(user_id=user_id, balance=balance_int)


@router.get("/", response_model=BalanceOut)
async def get_balance(
    authorization: str = Header(...),
    service: BalanceService = Depends(get_balance_service),
    auth_client: AuthClient = Depends(get_auth_client),
):
    token = authorization.replace("Bearer ", "")
    user_id = await auth_client.get_user_id_by_token(token)
    balance = await service.get_balance(user_id)
    return BalanceOut(user_id=user_id, balance=balance)


@router.post("/pay", response_model=BalanceOut)
async def pay(
    request: BalancePayRequest,
    authorization: str = Header(...),
    service: BalanceService = Depends(get_balance_service),
    auth_client: AuthClient = Depends(get_auth_client),
):
    token = authorization.replace("Bearer ", "")
    user_id = await auth_client.get_user_id_by_token(token)
    balance = await service.pay(user_id, request.amount)
    return BalanceOut(user_id=user_id, balance=balance)
