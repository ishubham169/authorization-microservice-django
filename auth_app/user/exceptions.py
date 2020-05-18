
class CustomException:
    class NotFoundException(Exception):
        pass

    class NotFoundExceptionWithSuccess(Exception):
        pass

    class ForbiddenException(Exception):
        pass

    class UnAuthorizeException(Exception):
        pass

    class UserNotVerified(Exception):
        pass

    class InvalidException(Exception):
        pass

    class ValidationError(Exception):
        pass