class DomainError(Exception):
    """Базовая ошибка домена"""
    pass


class InvalidTokenError(DomainError):
    pass


class UserNotFoundError(DomainError):
    pass


class InternalServiceError(DomainError):
    pass


class AuthTimeoutError(DomainError):
    pass


class BalanceNotFoundError(DomainError):
    pass


class InsufficientFundsError(DomainError):
    pass


class InvalidAmountError(DomainError):
    pass


class TokenExpiredError(DomainError):
    pass
