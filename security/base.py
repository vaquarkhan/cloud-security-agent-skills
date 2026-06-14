"""Abstract identity manager and shared credential types."""

from __future__ import annotations

import threading
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Optional


class TokenLifecycleError(RuntimeError):
    """Raised when short-lived credentials cannot be obtained or refreshed."""


@dataclass(frozen=True)
class CloudCredentials:
    """Provider-agnostic view of ephemeral cloud credentials."""

    provider: str
    access_token: str
    expires_at: Optional[datetime] = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return datetime.now(timezone.utc) >= self.expires_at

    @property
    def seconds_until_expiry(self) -> Optional[float]:
        if self.expires_at is None:
            return None
        delta = self.expires_at - datetime.now(timezone.utc)
        return max(delta.total_seconds(), 0.0)


class IdentityManager(ABC):
    """
    Autonomous token lifecycle manager.

    Implementations MUST NOT accept static passwords, API keys, or long-lived secrets.
    All credentials are obtained from ambient provider chains or workload identity.
    """

    _REFRESH_SKEW_SECONDS = 300

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._cached: Optional[CloudCredentials] = None

    @abstractmethod
    def provider_name(self) -> str:
        """Return the cloud provider identifier (aws, azure, gcp, ...)."""

    @abstractmethod
    def _fetch_credentials(self) -> CloudCredentials:
        """Fetch fresh credentials from the provider chain."""

    def get_credentials(self) -> CloudCredentials:
        """Return valid credentials, refreshing automatically when near expiry."""
        with self._lock:
            if self._cached is None or self._should_refresh(self._cached):
                self._cached = self._fetch_credentials()
            return self._cached

    def refresh_if_needed(self) -> CloudCredentials:
        """Force refresh when credentials are expired or within the refresh skew window."""
        with self._lock:
            if self._cached is None or self._should_refresh(self._cached):
                self._cached = self._fetch_credentials()
            return self._cached

    def invalidate(self) -> None:
        """Drop cached credentials (e.g., after auth failure)."""
        with self._lock:
            self._cached = None

    def _should_refresh(self, credentials: CloudCredentials) -> bool:
        if credentials.is_expired:
            return True
        remaining = credentials.seconds_until_expiry
        if remaining is None:
            return False
        return remaining <= self._REFRESH_SKEW_SECONDS

    @staticmethod
    def _epoch_to_datetime(epoch: Optional[float]) -> Optional[datetime]:
        if epoch is None:
            return None
        return datetime.fromtimestamp(epoch, tz=timezone.utc)

    @staticmethod
    def _sleep_backoff(attempt: int, base: float = 0.5, cap: float = 8.0) -> None:
        delay = min(base * (2**attempt), cap)
        time.sleep(delay)
