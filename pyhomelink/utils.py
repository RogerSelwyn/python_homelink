"""HomeLINK utilities."""
from .exceptions import ApiException, AuthException


def check_status(status):
    """Check status of the call."""
    if status == 401:
        raise AuthException(f"Authorization failed: {status}")
    if status != 200:
        raise ApiException(f"Error request failed: {status}")
