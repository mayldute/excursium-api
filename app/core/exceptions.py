class ApplicationError(Exception):
    """Base exception for expected application failures."""

    status_code = 400

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class NotFoundError(ApplicationError):
    status_code = 404


class ConflictError(ApplicationError):
    status_code = 409


class PermissionDeniedError(ApplicationError):
    status_code = 403


class AuthenticationError(ApplicationError):
    status_code = 401
