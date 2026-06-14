"""Alibaba Cloud RAM role ARN identity with background STS refresh."""

from __future__ import annotations

import os
import threading
from typing import Optional

from security.base import CloudCredentials, IdentityManager, TokenLifecycleError


class AlibabaRAMRoleManager(IdentityManager):
    """
    Uses alibabacloud_credentials with type='ram_role_arn' for STS temporary credentials.

    Background refresh is handled by the credentials provider; this manager surfaces
    the latest ephemeral session token to the agent.
    """

    _provider_lock = threading.Lock()
    _shared_provider: Optional[object] = None

    def provider_name(self) -> str:
        return "alibaba"

    def _fetch_credentials(self) -> CloudCredentials:
        provider = self._get_or_create_provider()
        creds = provider.get_credential()  # type: ignore[union-attr]

        access_key = getattr(creds, "access_key_id", None) or getattr(creds, "accessKeyId", None)
        secret_key = getattr(creds, "access_key_secret", None) or getattr(creds, "accessKeySecret", None)
        token = getattr(creds, "security_token", None) or getattr(creds, "securityToken", None)
        expiration = getattr(creds, "expiration", None)

        if not access_key or not secret_key:
            raise TokenLifecycleError("Alibaba RAM role provider did not return STS credentials")

        expires_at = None
        if expiration is not None:
            expires_at = self._epoch_to_datetime(expiration.timestamp())

        return CloudCredentials(
            provider=self.provider_name(),
            access_token=token or access_key,
            expires_at=expires_at,
            metadata={
                "access_key_id": access_key,
                "sts_token_present": bool(token),
            },
        )

    def _get_or_create_provider(self) -> object:
        with self._provider_lock:
            if self._shared_provider is not None:
                return self._shared_provider

            try:
                from alibabacloud_credentials.client import Client as CredClient
                from alibabacloud_credentials.models import Config as CredConfig
            except ImportError as exc:
                raise TokenLifecycleError(
                    "alibabacloud_credentials is required. "
                    "Install with: pip install cloud-security-agent-skills[alibaba]"
                ) from exc

            role_arn = os.getenv("ALIBABA_CLOUD_ROLE_ARN") or os.getenv("ALIBABA_CLOUD_ROLE_NAME")
            if not role_arn:
                raise TokenLifecycleError(
                    "Set ALIBABA_CLOUD_ROLE_ARN (or ALIBABA_CLOUD_ROLE_NAME) for RAM role authentication"
                )

            config = CredConfig(
                type="ram_role_arn",
                role_arn=role_arn,
                role_session_name=os.getenv("ALIBABA_CLOUD_ROLE_SESSION_NAME", "cloud-de-agent"),
            )
            self._shared_provider = CredClient(config)
            return self._shared_provider
