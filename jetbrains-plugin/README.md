# Cloud Security Agent Skills — JetBrains Plugin

Install **14 multi-cloud security skills**, Bastion MCP templates, presets, and zero-trust adapters into IntelliJ-based IDEs:

- IntelliJ IDEA · PyCharm · WebStorm · DataGrip · GoLand · PhpStorm

## Menu

**Tools → Cloud Security Agent Skills**

| Action | Description |
|--------|-------------|
| Install Full Toolkit | Skills, presets, hooks, MCP, adapters |
| Install Core Pack | AGENTS.md, 14 skills, bastion.yaml |
| Install Agent Adapters | Cursor, Claude, Copilot, Gemini, Kiro |
| Install Starter Pack | AWS / Azure / GCP / Multi-Cloud |
| Install MCP Bastion Templates | Bastion-wrapped MCP client |
| Scaffold Mock Posture Example | Runnable posture demo |

## Build

```bash
cd jetbrains-plugin
./gradlew buildPlugin    # Windows: gradlew.bat buildPlugin
```

Output: `build/distributions/cloud-security-agent-skills-jetbrains-0.2.0.zip`

Install via **Settings → Plugins → ⚙ → Install from Disk**.

## Local run

```bash
./gradlew runIde
```

See [docs/jetbrains-setup.md](../docs/jetbrains-setup.md).
