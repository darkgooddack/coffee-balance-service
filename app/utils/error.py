from fastapi import HTTPException, status


class AppBaseError(Exception):
    status_code: int = status.HTTP_400_BAD_REQUEST
    detail: str = "Сервисная ошибка"

    def http(self) -> HTTPException:
        return HTTPException(
            status_code=self.status_code,
            detail=self.detail
        )


class InvalidTokenError(AppBaseError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный токен"

class UserNotFoundError(AppBaseError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Пользователь не найден"

class InternalServiceError(AppBaseError):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Внутренняя ошибка сервиса"

class AuthTimeoutError(AppBaseError):
    status_code = status.HTTP_504_GATEWAY_TIMEOUT
    detail = "Превышено время ожидания авторизации"

