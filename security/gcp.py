"""GCP identity via google.auth default credential chain."""

from __future__ import annotations

from security.base import CloudCredentials, IdentityManager, TokenLifecycleError


class GCPDefaultCredentialManager(IdentityManager):
    """Uses google.auth.default() — ADC from metadata, workload identity, or gcloud."""

    def provider_name(self) -> str:
        return "gcp"

    def _fetch_credentials(self) -> CloudCredentials:
        try:
            import google.auth
            from google.auth.transport.requests import Request
        except ImportError as exc:
            raise TokenLifecycleError(
                "google-auth is required. Install with: pip install cloud-security-agent-skills[gcp]"
            ) from exc

        credentials, project = google.auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        credentials.refresh(Request())

        if not credentials.token:
            raise TokenLifecycleError("GCP default credentials did not yield an access token")

        return CloudCredentials(
            provider=self.provider_name(),
            access_token=credentials.token,
            expires_at=self._epoch_to_datetime(credentials.expiry.timestamp() if credentials.expiry else None),
            metadata={"project": project},
        )
