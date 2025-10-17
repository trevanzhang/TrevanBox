---
title: "Plugins reference"
source: "https://docs.claude.com/en/docs/claude-code/plugins-reference"
author:
  - "[[Claude Docs]]"
published:
created: 2025-10-18
description: "Complete technical reference for Claude Code plugin system, including schemas, CLI commands, and component specifications."
tags:
  - "clippings"
---
For hands-on tutorials and practical usage, see [Plugins](https://docs.claude.com/en/docs/claude-code/plugins). For plugin management across teams and communities, see [Plugin marketplaces](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces).

This reference provides complete technical specifications for the Claude Code plugin system, including component schemas, CLI commands, and development tools.

## Plugin components reference

This section documents the five types of components that plugins can provide.

### Commands

Plugins add custom slash commands that integrate seamlessly with Claude Code’s command system.**Location**: `commands/` directory in plugin root **File format**: Markdown files with frontmatter For complete details on plugin command structure, invocation patterns, and features, see [Plugin commands](https://docs.claude.com/en/docs/claude-code/slash-commands#plugin-commands).

### Agents

Plugins can provide specialized subagents for specific tasks that Claude can invoke automatically when appropriate.**Location**: `agents/` directory in plugin root **File format**: Markdown files describing agent capabilities **Agent structure**:

```
---

description: What this agent specializes in

capabilities: ["task1", "task2", "task3"]

---

# Agent Name

Detailed description of the agent's role, expertise, and when Claude should invoke it.

## Capabilities

- Specific task the agent excels at

- Another specialized capability

- When to use this agent vs others

## Context and examples

Provide examples of when this agent should be used and what kinds of problems it solves.
```

**Integration points**:
- Agents appear in the `/agents` interface
- Claude can invoke agents automatically based on task context
- Agents can be invoked manually by users
- Plugin agents work alongside built-in Claude agents

### Skills

Plugins can provide Agent Skills that extend Claude’s capabilities. Skills are model-invoked—Claude autonomously decides when to use them based on the task context.**Location**: `skills/` directory in plugin root **File format**: Directories containing `SKILL.md` files with frontmatter **Skill structure**:

```
skills/

├── pdf-processor/

│   ├── SKILL.md

│   ├── reference.md (optional)

│   └── scripts/ (optional)

└── code-reviewer/

    └── SKILL.md
```

**Integration behavior**:
- Plugin Skills are automatically discovered when the plugin is installed
- Claude autonomously invokes Skills based on matching task context
- Skills can include supporting files alongside SKILL.md
For SKILL.md format and complete Skill authoring guidance, see:
- [Use Skills in Claude Code](https://docs.claude.com/en/docs/claude-code/skills)
- [Agent Skills overview](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview#skill-structure)

### Hooks

Plugins can provide event handlers that respond to Claude Code events automatically.**Location**: `hooks/hooks.json` in plugin root, or inline in plugin.json **Format**: JSON configuration with event matchers and actions **Hook configuration**:

```
{

  "hooks": {

    "PostToolUse": [

      {

        "matcher": "Write|Edit",

        "hooks": [

          {

            "type": "command",

            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format-code.sh"

          }

        ]

      }

    ]

  }

}
```

**Available events**:
- `PreToolUse`: Before Claude uses any tool
- `PostToolUse`: After Claude uses any tool
- `UserPromptSubmit`: When user submits a prompt
- `Notification`: When Claude Code sends notifications
- `Stop`: When Claude attempts to stop
- `SubagentStop`: When a subagent attempts to stop
- `SessionStart`: At the beginning of sessions
- `SessionEnd`: At the end of sessions
- `PreCompact`: Before conversation history is compacted
**Hook types**:
- `command`: Execute shell commands or scripts
- `validation`: Validate file contents or project state
- `notification`: Send alerts or status updates

### MCP servers

Plugins can bundle Model Context Protocol (MCP) servers to connect Claude Code with external tools and services.**Location**: `.mcp.json` in plugin root, or inline in plugin.json **Format**: Standard MCP server configuration **MCP server configuration**:

```
{

  "mcpServers": {

    "plugin-database": {

      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",

      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],

      "env": {

        "DB_PATH": "${CLAUDE_PLUGIN_ROOT}/data"

      }

    },

    "plugin-api-client": {

      "command": "npx",

      "args": ["@company/mcp-server", "--plugin-mode"],

      "cwd": "${CLAUDE_PLUGIN_ROOT}"

    }

  }

}
```

**Integration behavior**:
- Plugin MCP servers start automatically when the plugin is enabled
- Servers appear as standard MCP tools in Claude’s toolkit
- Server capabilities integrate seamlessly with Claude’s existing tools
- Plugin servers can be configured independently of user MCP servers

---

## Plugin manifest schema

The `plugin.json` file defines your plugin’s metadata and configuration. This section documents all supported fields and options.

### Complete schema

### Required fields

| Field | Type | Description | Example |
| --- | --- | --- | --- |
| `name` | string | Unique identifier (kebab-case, no spaces) | `"deployment-tools"` |

| Field | Type | Description | Example |
| --- | --- | --- | --- |
| `version` | string | Semantic version | `"2.1.0"` |
| `description` | string | Brief explanation of plugin purpose | `"Deployment automation tools"` |
| `author` | object | Author information | `{"name": "Dev Team", "email": "dev@company.com"}` |
| `homepage` | string | Documentation URL | `"https://docs.example.com"` |
| `repository` | string | Source code URL | `"https://github.com/user/plugin"` |
| `license` | string | License identifier | `"MIT"`, `"Apache-2.0"` |
| `keywords` | array | Discovery tags | `["deployment", "ci-cd"]` |

### Component path fields

| Field | Type | Description | Example |
| --- | --- | --- | --- |
| `commands` | string\|array | Additional command files/directories | `"./custom/cmd.md"` or `["./cmd1.md"]` |
| `agents` | string\|array | Additional agent files | `"./custom/agents/"` |
| `hooks` | string\|object | Hook config path or inline config | `"./hooks.json"` |
| `mcpServers` | string\|object | MCP config path or inline config | `"./mcp.json"` |

### Path behavior rules

**Important**: Custom paths supplement default directories - they don’t replace them.
- If `commands/` exists, it’s loaded in addition to custom command paths
- All paths must be relative to plugin root and start with `./`
- Commands from custom paths use the same naming and namespacing rules
- Multiple paths can be specified as arrays for flexibility
**Path examples**:

```
{

  "commands": [

    "./specialized/deploy.md",

    "./utilities/batch-process.md"

  ],

  "agents": [

    "./custom-agents/reviewer.md",

    "./custom-agents/tester.md"

  ]

}
```

### Environment variables

**`${CLAUDE_PLUGIN_ROOT}`**: Contains the absolute path to your plugin directory. Use this in hooks, MCP servers, and scripts to ensure correct paths regardless of installation location.

```
{

  "hooks": {

    "PostToolUse": [

      {

        "hooks": [

          {

            "type": "command",

            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/process.sh"

          }

        ]

      }

    ]

  }

}
```

---

## Plugin directory structure

### Standard plugin layout

A complete plugin follows this structure:

```
enterprise-plugin/

├── .claude-plugin/           # Metadata directory

│   └── plugin.json          # Required: plugin manifest

├── commands/                 # Default command location

│   ├── status.md

│   └──  logs.md

├── agents/                   # Default agent location

│   ├── security-reviewer.md

│   ├── performance-tester.md

│   └── compliance-checker.md

├── skills/                   # Agent Skills

│   ├── code-reviewer/

│   │   └── SKILL.md

│   └── pdf-processor/

│       ├── SKILL.md

│       └── scripts/

├── hooks/                    # Hook configurations

│   ├── hooks.json           # Main hook config

│   └── security-hooks.json  # Additional hooks

├── .mcp.json                # MCP server definitions

├── scripts/                 # Hook and utility scripts

│   ├── security-scan.sh

│   ├── format-code.py

│   └── deploy.js

├── LICENSE                  # License file

└── CHANGELOG.md             # Version history
```

The `.claude-plugin/` directory contains the `plugin.json` file. All other directories (commands/, agents/, skills/, hooks/) must be at the plugin root, not inside `.claude-plugin/`.

### File locations reference

| Component | Default Location | Purpose |
| --- | --- | --- |
| **Manifest** | `.claude-plugin/plugin.json` | Required metadata file |
| **Commands** | `commands/` | Slash command markdown files |
| **Agents** | `agents/` | Subagent markdown files |
| **Skills** | `skills/` | Agent Skills with SKILL.md files |
| **Hooks** | `hooks/hooks.json` | Hook configuration |
| **MCP servers** | `.mcp.json` | MCP server definitions |

---

## Debugging and development tools

### Debugging commands

Use `claude --debug` to see plugin loading details:

```
claude --debug
```

This shows:
- Which plugins are being loaded
- Any errors in plugin manifests
- Command, agent, and hook registration
- MCP server initialization

### Common issues

| Issue | Cause | Solution |
| --- | --- | --- |
| Plugin not loading | Invalid `plugin.json` | Validate JSON syntax |
| Commands not appearing | Wrong directory structure | Ensure `commands/` at root, not in `.claude-plugin/` |
| Hooks not firing | Script not executable | Run `chmod +x script.sh` |
| MCP server fails | Missing `${CLAUDE_PLUGIN_ROOT}` | Use variable for all plugin paths |
| Path errors | Absolute paths used | All paths must be relative and start with `./` |

---

## Distribution and versioning reference

### Version management

Follow semantic versioning for plugin releases:

```
## See also

- [Plugins](/en/docs/claude-code/plugins) - Tutorials and practical usage

- [Plugin marketplaces](/en/docs/claude-code/plugin-marketplaces) - Creating and managing marketplaces

- [Slash commands](/en/docs/claude-code/slash-commands) - Command development details

- [Subagents](/en/docs/claude-code/sub-agents) - Agent configuration and capabilities

- [Agent Skills](/en/docs/claude-code/skills) - Extend Claude's capabilities

- [Hooks](/en/docs/claude-code/hooks) - Event handling and automation

- [MCP](/en/docs/claude-code/mcp) - External tool integration

- [Settings](/en/docs/claude-code/settings) - Configuration options for plugins
```

[Hooks reference](https://docs.claude.com/en/docs/claude-code/hooks) [Legal and compliance](https://docs.claude.com/en/docs/claude-code/legal-and-compliance)