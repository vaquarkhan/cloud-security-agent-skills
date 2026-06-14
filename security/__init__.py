"""Zero-trust multi-cloud identity abstraction layer."""

from security.base import CloudCredentials, IdentityManager, TokenLifecycleError
from security.introspection import CloudEnvironment, detect_cloud_environment, get_identity_manager

__all__ = [
    "CloudCredentials",
    "CloudEnvironment",
    "IdentityManager",
    "TokenLifecycleError",
    "detect_cloud_environment",
    "get_identity_manager",
]
