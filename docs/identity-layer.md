# Identity layer — zero-trust multi-cloud

All cloud access uses **short-lived credentials** from ambient provider chains. No static API keys, passwords, or long-lived tokens in code.

## Detection order

`security/introspection.py` checks signals in priority order:

| Priority | Signal | Manager |
|----------|--------|---------|
| 1 | `OCI_RESOURCE_PRINCIPAL_VERSION` | `OCIResourcePrincipalManager` |
| 2 | `TRUSTED_PROFILE_NAME` | `IBMTrustedProfileManager` |
| 3 | `ALIBABA_CLOUD_ECS_METADATA` | `AlibabaRAMRoleManager` |
| 4 | `VCAP_SERVICES` / `VCAP_APPLICATION` | `PCFCredHubManager` |
| 5 | `AWS_EXECUTION_ENV` / `AWS_REGION` | `AWSCredentialChainManager` |
| 6 | `AZURE_CLIENT_ID` / `IDENTITY_ENDPOINT` | `AzureDefaultCredentialManager` |
| 7 | `GOOGLE_CLOUD_PROJECT` / `K_SERVICE` | `GCPDefaultCredentialManager` |

## Per-cloud reference

| Cloud | Class | Mechanism | Required env / binding |
|-------|-------|-----------|------------------------|
| AWS | `AWSCredentialChainManager` | boto3 default chain | IAM role, IRSA, instance profile |
| Azure | `AzureDefaultCredentialManager` | `DefaultAzureCredential` | Managed identity, workload identity |
| GCP | `GCPDefaultCredentialManager` | Application Default Credentials | GCE/GKE metadata, WIF |
| OCI | `OCIResourcePrincipalManager` | `get_resource_principals_signer()` | `OCI_RESOURCE_PRINCIPAL_VERSION` |
| IBM | `IBMTrustedProfileManager` | `ContainerAuthenticator` | `TRUSTED_PROFILE_NAME` |
| Alibaba | `AlibabaRAMRoleManager` | `ram_role_arn` STS refresh | `ALIBABA_CLOUD_ROLE_ARN` |
| PCF | `PCFCredHubManager` | VCAP or UAA OAuth2 | Platform-injected `VCAP_SERVICES` |

## Usage in code

```python
from security import detect_cloud_environment, get_identity_manager

signal = detect_cloud_environment()
print(signal.environment, signal.signals)

manager = get_identity_manager()
creds = manager.get_credentials()
manager.refresh_if_needed()
```

## Install extras

Install only the SDKs you need:

```bash
pip install -e ".[aws]"
pip install -e ".[azure,gcp,oci,ibm,alibaba]"
```

## OCI Vault

When `OCI_VAULT_ID` is set, `OCIResourcePrincipalManager` connects to OCI Vault using the resource principal signer. Vault OCIDs come from platform config — never hard-coded secrets.

## PCF CredHub

`PCFCredHubManager` parses CredHub bindings from `VCAP_SERVICES` or exchanges UAA client credentials (injected by the platform) for OAuth2 tokens. Client secrets must come from service bindings, not source files.
