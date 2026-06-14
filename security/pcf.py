"""VMware Tanzu PCF CredHub identity via VCAP_SERVICES or UAA OAuth2."""

from __future__ import annotations

import json
import os
from typing import Any
from urllib.parse import urljoin

import httpx

from security.base import CloudCredentials, IdentityManager, TokenLifecycleError


class PCFCredHubManager(IdentityManager):
    """
    Resolves CredHub credentials from VCAP_SERVICES or authenticates to CredHub via UAA.

    No static passwords are embedded; UAA client credentials come from bound services.
    """

    def provider_name(self) -> str:
        return "pcf"

    def _fetch_credentials(self) -> CloudCredentials:
        vcap = os.getenv("VCAP_SERVICES")
        if vcap:
            return self._credentials_from_vcap(vcap)
        return self._credentials_from_uaa()

    def _credentials_from_vcap(self, vcap_json: str) -> CloudCredentials:
        try:
            services: dict[str, list[dict[str, Any]]] = json.loads(vcap_json)
        except json.JSONDecodeError as exc:
            raise TokenLifecycleError("VCAP_SERVICES payload is not valid JSON") from exc

        credhub_binding = self._find_credhub_binding(services)
        if credhub_binding is None:
            raise TokenLifecycleError("No CredHub service binding found in VCAP_SERVICES")

        credentials = credhub_binding.get("credentials", {})
        access_token = credentials.get("access_token") or credentials.get("uaa_access_token")
        if access_token:
            return CloudCredentials(
                provider=self.provider_name(),
                access_token=access_token,
                metadata={"source": "vcap_services", "label": credhub_binding.get("label", "")},
            )

        return self._uaa_token_from_binding(credentials)

    def _find_credhub_binding(
        self, services: dict[str, list[dict[str, Any]]]
    ) -> dict[str, Any] | None:
        for instances in services.values():
            for instance in instances:
                label = (instance.get("label") or "").lower()
                name = (instance.get("name") or "").lower()
                if "credhub" in label or "credhub" in name:
                    return instance
        return None

    def _uaa_token_from_binding(self, credentials: dict[str, Any]) -> CloudCredentials:
        uaa_url = credentials.get("uaa_url") or credentials.get("url")
        client_id = credentials.get("client_id") or credentials.get("clientid")
        client_secret = credentials.get("client_secret") or credentials.get("clientsecret")

        if not all([uaa_url, client_id, client_secret]):
            raise TokenLifecycleError(
                "CredHub binding missing UAA client credentials for OAuth2 token exchange"
            )

        token_url = urljoin(uaa_url.rstrip("/") + "/", "oauth/token")
        response = httpx.post(
            token_url,
            data={
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
            },
            headers={"Accept": "application/json"},
            timeout=30.0,
        )
        response.raise_for_status()
        payload = response.json()
        access_token = payload.get("access_token")
        if not access_token:
            raise TokenLifecycleError("UAA OAuth2 response did not include access_token")

        expires_in = payload.get("expires_in")
        expires_at = None
        if isinstance(expires_in, (int, float)):
            from datetime import datetime, timedelta, timezone

            expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)

        return CloudCredentials(
            provider=self.provider_name(),
            access_token=access_token,
            expires_at=expires_at,
            metadata={"source": "uaa_oauth2", "token_type": payload.get("token_type", "bearer")},
        )

    def _credentials_from_uaa(self) -> CloudCredentials:
        uaa_url = os.getenv("UAA_URL") or os.getenv("CF_UAA_URL")
        client_id = os.getenv("UAA_CLIENT_ID")
        client_secret = os.getenv("UAA_CLIENT_SECRET")

        if not all([uaa_url, client_id, client_secret]):
            raise TokenLifecycleError(
                "PCF identity requires VCAP_SERVICES or UAA_URL + UAA_CLIENT_ID + UAA_CLIENT_SECRET "
                "(injected by platform, not hard-coded)"
            )

        return self._uaa_token_from_binding(
            {"uaa_url": uaa_url, "client_id": client_id, "client_secret": client_secret}
        )
