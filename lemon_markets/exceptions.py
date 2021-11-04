"""Exceptions raised by the SDK."""


class LemonException(Exception):
    """Baseclass for exceptions raised by the SDK."""

    pass


class LemonConnectionException(LemonException):
    """Raised when there is a problem with the network connection."""

    pass


class LemonTokenException(LemonException):
    """Raised when the account token is of the wrong type."""

    pass
