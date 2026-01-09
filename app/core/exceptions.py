from fastapi import HTTPException, status
from app.domain import errors as domain_errors


ERROR_MAPPING = {
    domain_errors.InvalidTokenError: (
        status.HTTP_401_UNAUTHORIZED,
        "Неверный токен",
    ),
    domain_errors.UserNotFoundError: (
        status.HTTP_404_NOT_FOUND,
        "Пользователь не найден",
    ),
    domain_errors.AuthTimeoutError: (
        status.HTTP_504_GATEWAY_TIMEOUT,
        "Превышено время ожидания авторизации",
    ),
    domain_errors.BalanceNotFoundError: (
        status.HTTP_404_NOT_FOUND,
        "Баланс пользователя не найден",
    ),
    domain_errors.InsufficientFundsError: (
        status.HTTP_400_BAD_REQUEST,
        "Недостаточно средств",
    ),
    domain_errors.InvalidAmountError: (
        status.HTTP_400_BAD_REQUEST,
        "Некорректная сумма операции",
    ),
}

def map_exception(exc: Exception) -> HTTPException:
    for exc_type, (status_code, detail) in ERROR_MAPPING.items():
        if isinstance(exc, exc_type):
            return HTTPException(
                status_code=status_code,
                detail=detail,
            )

    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Внутренняя ошибка сервиса",
    )
