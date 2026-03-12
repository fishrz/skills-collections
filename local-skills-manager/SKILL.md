---
name: local-skills-manager
description: Manage locally installed agent skills. Use when user asks to list installed skills, sync skills across agents, check skill status, enable/disable skills, or manage their local skill library. Triggers include "list my skills", "what skills do I have", "sync skills", "show installed skills", "enable/disable skill", or any request about managing local skills.
version: 1.0.0
author: local
---

# Local Skills Manager

Manage your locally installed agent skills across Cursor, Claude, and Codex environments.

## When to Use

Use this skill when you need to:
- List all installed skills with their descriptions
- Sync skills from `.agents/skills/` to other agent directories
- Get detailed info about a specific skill
- Enable or disable skills for specific agents
- Check which skills are available where

## Core Commands

### List All Installed Skills

```bash
python scripts/skills_manager.py list
```

Options:
- `--format json` - Output as JSON
- `--format table` - Output as formatted table (default)
- `--search <keyword>` - Filter by name/description

### Sync Skills Across Agents

```bash
python scripts/skills_manager.py sync
```

Syncs all skills from `~/.agents/skills/` to:
- `~/.cursor/skills/`
- `~/.claude/skills/`
- `~/.codex/skills/`

Options:
- `--dry-run` - Preview changes without applying
- `--target cursor|claude|codex` - Sync to specific agent only

### Show Skill Info

```bash
python scripts/skills_manager.py info <skill-name>
```

Displays:
- Name and description
- Version and author
- File structure
- Installation locations
- Sync status across agents

### Enable/Disable Skills

```bash
python scripts/skills_manager.py enable <skill-name> --target cursor
python scripts/skills_manager.py disable <skill-name> --target claude
```

Enable creates a junction/symlink, disable removes it.

### Check Sync Status

```bash
python scripts/skills_manager.py status
```

Shows which skills are synced to which agents in a matrix view.

## Directory Structure

```
~/.agents/skills/           # Central skill repository (source of truth)
├── skill-a/
├── skill-b/
└── ...

~/.cursor/skills/           # Cursor-specific (junctions to .agents)
~/.claude/skills/           # Claude-specific (junctions to .agents)
~/.codex/skills/            # Codex-specific (junctions to .agents)
```

## Usage Examples

### Example 1: List all skills

```
User: What skills do I have installed?
Assistant: [Runs python scripts/skills_manager.py list]

╔═══════════════════════════╤════════════════════════════════════════════════════╗
║ Skill Name                │ Description                                        ║
╠═══════════════════════════╪════════════════════════════════════════════════════╣
║ product-strategist        │ Visionary AI Product Strategist for discovering... ║
║ ai-feature-evaluator      │ AI Product Architect for evaluating feature...     ║
║ ai-ux-designer            │ Senior AI Product Designer specializing in...      ║
║ stock-analysis            │ Analyze stocks and cryptocurrencies using...       ║
╚═══════════════════════════╧════════════════════════════════════════════════════╝

Total: 35 skills installed
```

### Example 2: Check sync status

```
User: Which skills are synced where?
Assistant: [Runs python scripts/skills_manager.py status]

╔═══════════════════════════╤════════╤════════╤════════╗
║ Skill                     │ Cursor │ Claude │ Codex  ║
╠═══════════════════════════╪════════╪════════╪════════╣
║ product-strategist        │   ✓    │   ✓    │   ✓    ║
║ ai-feature-evaluator      │   ✓    │   ✓    │   ✓    ║
║ ai-ux-designer            │   ✓    │   ✓    │   ✓    ║
║ stock-analysis            │   ✓    │   ✗    │   ✓    ║
╚═══════════════════════════╧════════╧════════╧════════╝
```

### Example 3: Sync all skills

```
User: Sync all my skills to all agents
Assistant: [Runs python scripts/skills_manager.py sync]

Syncing skills from ~/.agents/skills/...

✓ product-strategist → cursor, claude, codex
✓ ai-feature-evaluator → cursor, claude, codex
✓ ai-ux-designer → cursor, claude, codex
⊕ stock-analysis → claude (newly synced)

Sync complete: 35 skills, 3 new links created
```

### Example 4: Get skill info

```
User: Tell me about the product-strategist skill
Assistant: [Runs python scripts/skills_manager.py info product-strategist]

╔══════════════════════════════════════════════════════════════════╗
║ Skill: product-strategist                                        ║
╠══════════════════════════════════════════════════════════════════╣
║ Description: Visionary AI Product Strategist for discovering     ║
║              high-impact "Killer Features" through trend         ║
║              analysis and First Principles thinking.             ║
╠══════════════════════════════════════════════════════════════════╣
║ Location: ~/.agents/skills/product-strategist/                   ║
║ Files: SKILL.md                                                  ║
║ Size: 8.2 KB                                                     ║
╠══════════════════════════════════════════════════════════════════╣
║ Sync Status:                                                     ║
║   Cursor: ✓ synced (junction)                                    ║
║   Claude: ✓ synced (junction)                                    ║
║   Codex:  ✓ synced (junction)                                    ║
╚══════════════════════════════════════════════════════════════════╝
```

## Notes

- On Windows, junctions (`mklink /J`) are used instead of symlinks (no admin required)
- The `.agents/skills/` directory is the source of truth
- Skills installed via `npx skills add` may need manual sync
- Restart your agent after syncing to pick up new skills
