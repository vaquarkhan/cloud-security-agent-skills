"""IBM Cloud trusted profile identity via ContainerAuthenticator."""

from __future__ import annotations

import os

from security.base import CloudCredentials, IdentityManager, TokenLifecycleError


class IBMTrustedProfileManager(IdentityManager):
    """
    Authenticates using ibm_cloud_sdk_core ContainerAuthenticator.

    Requires ONLY the TRUSTED_PROFILE_NAME environment variable — no API keys.
    """

    def provider_name(self) -> str:
        return "ibm"

    def _fetch_credentials(self) -> CloudCredentials:
        profile_name = os.getenv("TRUSTED_PROFILE_NAME")
        if not profile_name:
            raise TokenLifecycleError(
                "TRUSTED_PROFILE_NAME environment variable is required for IBM Cloud identity"
            )

        try:
            from ibm_cloud_sdk_core.authenticators import ContainerAuthenticator
        except ImportError as exc:
            raise TokenLifecycleError(
                "ibm-cloud-sdk-core is required. Install with: pip install cloud-security-agent-skills[ibm]"
            ) from exc

        authenticator = ContainerAuthenticator(
            profile_name=profile_name,
            url=os.getenv("IBM_AUTH_URL"),
        )
        authenticator.validate()

        headers = authenticator.authenticate({})
        authorization = headers.get("Authorization", "")
        if not authorization.startswith("Bearer "):
            raise TokenLifecycleError("IBM ContainerAuthenticator did not return a Bearer token")

        token = authorization.removeprefix("Bearer ").strip()
        return CloudCredentials(
            provider=self.provider_name(),
            access_token=token,
            metadata={"trusted_profile": profile_name},
        )
