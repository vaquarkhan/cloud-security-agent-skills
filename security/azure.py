"""Azure identity via DefaultAzureCredential (managed identity, workload, CLI chain)."""

from __future__ import annotations

from security.base import CloudCredentials, IdentityManager, TokenLifecycleError


class AzureDefaultCredentialManager(IdentityManager):
    """Relies strictly on azure.identity.DefaultAzureCredential — no client secrets in code."""

    def provider_name(self) -> str:
        return "azure"

    def _fetch_credentials(self) -> CloudCredentials:
        try:
            from azure.identity import DefaultAzureCredential
        except ImportError as exc:
            raise TokenLifecycleError(
                "azure-identity is required. Install with: pip install cloud-security-agent-skills[azure]"
            ) from exc

        credential = DefaultAzureCredential(exclude_interactive_browser_credential=True)
        token = credential.get_token("https://management.azure.com/.default")

        return CloudCredentials(
            provider=self.provider_name(),
            access_token=token.token,
            expires_at=self._epoch_to_datetime(token.expires_on),
            metadata={"token_type": "Bearer"},
        )
