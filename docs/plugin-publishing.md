# Plugin publishing

Release checklist for **VS Code** and **JetBrains** plugins.

## Pre-release

```bash
make plugin-sync
make validate
python scripts/validate-plugin-manifest.py
```

1. Bump `VERSION`, `pyproject.toml`, `vscode-extension/package.json`, `jetbrains-plugin/gradle.properties`
2. Update `CHANGELOG.md`
3. Run `python scripts/sync-install-manifest.py`

## VS Code

```bash
cd vscode-extension
npm install
npx @vscode/vsce package
# npx @vscode/vsce publish  # with PAT
```

Artifact: `cloud-security-agent-skills-0.2.0.vsix`

## JetBrains

```bash
cd jetbrains-plugin
./gradlew buildPlugin publishPlugin
```

Requires `JETBRAINS_MARKETPLACE_TOKEN` for publish.

## GitHub release

Attach:

- `.vsix` from vscode-extension
- `.zip` from `jetbrains-plugin/build/distributions/`

Tag: `v0.2.0`
