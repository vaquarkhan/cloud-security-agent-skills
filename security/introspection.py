"""Cloud environment introspection and identity manager routing."""

from __future__ import annotations

import os
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Type

from security.base import IdentityManager


class CloudEnvironment(str, Enum):
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
    OCI = "oci"
    IBM = "ibm"
    ALIBABA = "alibaba"
    PCF = "pcf"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class EnvironmentSignal:
    """Detected environment with confidence metadata."""

    environment: CloudEnvironment
    signals: tuple[str, ...]


def detect_cloud_environment() -> EnvironmentSignal:
    """
    Dynamically detect the active cloud runtime from ambient signals.

    Checks provider-specific environment variables and metadata endpoints
    in priority order. No static credentials are read or required.
    """
    signals: list[str] = []

    if os.getenv("OCI_RESOURCE_PRINCIPAL_VERSION"):
        signals.append("OCI_RESOURCE_PRINCIPAL_VERSION")
        return EnvironmentSignal(CloudEnvironment.OCI, tuple(signals))

    if os.getenv("TRUSTED_PROFILE_NAME"):
        signals.append("TRUSTED_PROFILE_NAME")
        return EnvironmentSignal(CloudEnvironment.IBM, tuple(signals))

    if os.getenv("ALIBABA_CLOUD_ECS_METADATA"):
        signals.append("ALIBABA_CLOUD_ECS_METADATA")
        return EnvironmentSignal(CloudEnvironment.ALIBABA, tuple(signals))

    if os.getenv("VCAP_SERVICES") or os.getenv("VCAP_APPLICATION"):
        signals.append("VCAP_SERVICES" if os.getenv("VCAP_SERVICES") else "VCAP_APPLICATION")
        return EnvironmentSignal(CloudEnvironment.PCF, tuple(signals))

    if os.getenv("AWS_EXECUTION_ENV") or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"):
        for key in ("AWS_EXECUTION_ENV", "AWS_REGION", "AWS_DEFAULT_REGION"):
            if os.getenv(key):
                signals.append(key)
        return EnvironmentSignal(CloudEnvironment.AWS, tuple(signals))

    if os.getenv("AZURE_CLIENT_ID") or os.getenv("IDENTITY_ENDPOINT") or os.getenv("MSI_ENDPOINT"):
        for key in ("AZURE_CLIENT_ID", "IDENTITY_ENDPOINT", "MSI_ENDPOINT"):
            if os.getenv(key):
                signals.append(key)
        return EnvironmentSignal(CloudEnvironment.AZURE, tuple(signals))

    if os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT") or os.getenv("K_SERVICE"):
        for key in ("GOOGLE_CLOUD_PROJECT", "GCP_PROJECT", "K_SERVICE"):
            if os.getenv(key):
                signals.append(key)
        return EnvironmentSignal(CloudEnvironment.GCP, tuple(signals))

    return EnvironmentSignal(CloudEnvironment.UNKNOWN, tuple(signals))


def get_identity_manager(
    environment: Optional[CloudEnvironment] = None,
) -> IdentityManager:
    """Instantiate the IdentityManager matching the detected or specified environment."""
    detected = detect_cloud_environment() if environment is None else None
    target = environment or (detected.environment if detected else CloudEnvironment.UNKNOWN)

    registry: dict[CloudEnvironment, Type[IdentityManager]] = {
        CloudEnvironment.AWS: _lazy_import("security.aws", "AWSCredentialChainManager"),
        CloudEnvironment.AZURE: _lazy_import("security.azure", "AzureDefaultCredentialManager"),
        CloudEnvironment.GCP: _lazy_import("security.gcp", "GCPDefaultCredentialManager"),
        CloudEnvironment.OCI: _lazy_import("security.oci", "OCIResourcePrincipalManager"),
        CloudEnvironment.IBM: _lazy_import("security.ibm", "IBMTrustedProfileManager"),
        CloudEnvironment.ALIBABA: _lazy_import("security.alibaba", "AlibabaRAMRoleManager"),
        CloudEnvironment.PCF: _lazy_import("security.pcf", "PCFCredHubManager"),
    }

    if target not in registry:
        raise RuntimeError(
            f"No IdentityManager available for environment '{target.value}'. "
            "Ensure the agent runs on a supported cloud with workload identity configured."
        )

    manager_cls = registry[target]
    return manager_cls()


def _lazy_import(module: str, class_name: str) -> Type[IdentityManager]:
    import importlib

    mod = importlib.import_module(module)
    return getattr(mod, class_name)
