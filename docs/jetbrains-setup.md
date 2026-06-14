# JetBrains setup

Install for **IntelliJ IDEA**, **PyCharm**, **WebStorm**, **DataGrip**, **GoLand**, **PhpStorm**.

## Build plugin

```bash
cd jetbrains-plugin
./gradlew buildPlugin    # Windows: gradlew.bat buildPlugin
```

Install ZIP: **Settings → Plugins → ⚙ → Install Plugin from Disk**

## Menu

**Tools → Cloud Security Agent Skills**

- Install Full Toolkit
- Install Core Pack
- Install Agent Adapters
- Install Starter Pack
- Install MCP Bastion Templates
- Scaffold Mock Posture Example

## Local development

```bash
./gradlew runIde
```

## Bootstrap alternative

```bash
./bootstrap.sh --target all
```

Copies skills and adapters into the current project without the plugin.

See [jetbrains-plugin/README.md](../jetbrains-plugin/README.md).
