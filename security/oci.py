"""Oracle Cloud Infrastructure resource principal identity."""

from __future__ import annotations

import os

from security.base import CloudCredentials, IdentityManager, TokenLifecycleError


class OCIResourcePrincipalManager(IdentityManager):
    """
    Authenticates via OCI resource principals and connects to OCI Vault.

    Uses oci.auth.signers.get_resource_principals_signer() for short-lived tokens.
    Requires OCI_RESOURCE_PRINCIPAL_VERSION in the runtime environment.
    """

    def provider_name(self) -> str:
        return "oci"

    def _fetch_credentials(self) -> CloudCredentials:
        if not os.getenv("OCI_RESOURCE_PRINCIPAL_VERSION"):
            raise TokenLifecycleError(
                "OCI resource principal environment not detected (OCI_RESOURCE_PRINCIPAL_VERSION missing)"
            )

        try:
            import oci
            from oci.auth.signers import get_resource_principals_signer
        except ImportError as exc:
            raise TokenLifecycleError(
                "oci SDK is required. Install with: pip install cloud-security-agent-skills[oci]"
            ) from exc

        signer = get_resource_principals_signer()
        security_token = getattr(signer, "security_token", None) or getattr(signer, "token", None)
        if not security_token:
            raise TokenLifecycleError("OCI resource principal signer did not provide a security token")

        vault_client = self._build_vault_client(signer)

        return CloudCredentials(
            provider=self.provider_name(),
            access_token=security_token,
            metadata={
                "tenancy_id": os.getenv("OCI_TENANCY_ID", ""),
                "resource_id": os.getenv("OCI_RESOURCE_ID", ""),
                "vault_reachable": vault_client is not None,
            },
        )

    def _build_vault_client(self, signer: object) -> object | None:
        """Connect to OCI Vault using the resource principal signer."""
        vault_ocid = os.getenv("OCI_VAULT_ID")
        if not vault_ocid:
            return None

        try:
            import oci

            region = os.getenv("OCI_REGION") or signer.region  # type: ignore[attr-defined]
            config = {"region": region}
            return oci.vault.VaultsClient(config, signer=signer)
        except Exception:
            return None
