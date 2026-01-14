from utils.base import AppException

class PermissionDenied(AppException):
    pass

class NotFoundError(AppException):
    pass

class DatabaseError(AppException):
    pass

class BadRequest(AppException):
    pass

class NotAuthenticatedUser(AppException):
    pass
