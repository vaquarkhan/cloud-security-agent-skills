# VS Code setup

Install for **VS Code**, **Cursor**, **Windsurf**, and **GitHub Copilot**.

## Extension (recommended)

```bash
cd vscode-extension
npm install
npx @vscode/vsce package
code --install-extension cloud-security-agent-skills-*.vsix
```

## Bootstrap

```bash
./bootstrap.sh --target vscode
```

Installs `.github/copilot-instructions.md` and core skills.

## Commands (Command Palette)

- **Cloud Security Agent Skills: Install Full Toolkit**
- **Cloud Security Agent Skills: Install Starter Pack** — AWS / Azure / GCP / Multi-Cloud
- **Cloud Security Agent Skills: Install Cloud Preset**
- **Cloud Security Agent Skills: Install MCP Bastion Templates**

## Copilot

[.github/copilot-instructions.md](../.github/copilot-instructions.md) enforces zero-trust routing and Bastion MCP.

## Workspace settings (optional)

```json
{
  "python.defaultInterpreterPath": ".venv/Scripts/python",
  "files.associations": { "*.mdc": "markdown" }
}
```

## Validate

```bash
make validate
pytest tests/unit/ -v
```

See [vscode-extension/README.md](../vscode-extension/README.md).
