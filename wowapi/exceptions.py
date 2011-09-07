class APIError(Exception):
    """
    This is raised on all other http errors only with the error code, this will change in the future and
    include the error message
    """
    pass

class NotModified(APIError):
    """
    This is raised when using the last modified option and nothing changed, since last request
    """
    pass

class NotFound(APIError):
    """
    This is raised on 404 Errors
    """
    pass