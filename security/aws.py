"""AWS identity via default credential provider chain (no static keys)."""

from __future__ import annotations

from datetime import datetime, timezone

from security.base import CloudCredentials, IdentityManager, TokenLifecycleError


class AWSCredentialChainManager(IdentityManager):
    """
    Uses boto3's default credential provider chain:
    env vars (ephemeral), instance/profile/SSO/WebIdentity, etc.
    """

    def provider_name(self) -> str:
        return "aws"

    def _fetch_credentials(self) -> CloudCredentials:
        try:
            import boto3
            from botocore.exceptions import BotoCoreError, NoCredentialsError
        except ImportError as exc:
            raise TokenLifecycleError(
                "boto3 is required for AWS identity. Install with: pip install cloud-security-agent-skills[aws]"
            ) from exc

        session = boto3.Session()
        try:
            frozen = session.get_credentials().get_frozen_credentials()
        except (NoCredentialsError, BotoCoreError) as exc:
            raise TokenLifecycleError("AWS default credential chain returned no credentials") from exc

        if not frozen or not frozen.access_key:
            raise TokenLifecycleError("AWS credential chain did not yield an access key")

        expires_at: datetime | None = None
        if frozen.token:
            # STS session tokens are short-lived; refresh aggressively via parent lifecycle.
            expires_at = datetime.now(timezone.utc).replace(microsecond=0)

        return CloudCredentials(
            provider=self.provider_name(),
            access_token=frozen.token or frozen.access_key,
            expires_at=expires_at,
            metadata={
                "access_key_id": frozen.access_key,
                "secret_access_key_present": bool(frozen.secret_key),
            },
        )
