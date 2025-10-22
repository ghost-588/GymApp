class AppError(Exception):
    """Base class for all custom errors."""

    def __init__(self, message: str):
        self.message = message


class NotFoundError(AppError):
    """Raised when a resource is not found."""

    pass


class AlreadyExistsError(AppError):
    """Raised when trying to create a resource that already exists."""

    pass


class ValidationError(AppError):
    """Raised for invalid input data."""

    pass


class BusinessRuleError(AppError):
    """Raised when logical rule violation"""

    pass


class NotAuthorizedError(AppError):
    """Raised when not authorized"""

    pass


class InvalidToken(AppError):
    """Raised when invalid token"""

    pass


class InvalidCredentials(AppError):
    """Raised when invalid credentials"""

    pass
