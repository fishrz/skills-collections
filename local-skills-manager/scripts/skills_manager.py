#!/usr/bin/env python3
"""
Local Skills Manager - Manage locally installed agent skills
"""

import os
import sys
import json
import argparse
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Agent directories relative to home
AGENT_DIRS = {
    'cursor': '.cursor/skills',
    'claude': '.claude/skills',
    'codex': '.codex/skills',
}

# Source directory
SOURCE_DIR = '.agents/skills'


def get_home() -> Path:
    """Get user home directory."""
    return Path.home()


def get_source_dir() -> Path:
    """Get the source skills directory."""
    return get_home() / SOURCE_DIR


def get_agent_dir(agent: str) -> Path:
    """Get the skills directory for a specific agent."""
    if agent not in AGENT_DIRS:
        raise ValueError(f"Unknown agent: {agent}")
    return get_home() / AGENT_DIRS[agent]


def parse_skill_frontmatter(skill_path: Path) -> Dict:
    """Parse SKILL.md frontmatter to extract metadata."""
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return {'name': skill_path.name, 'description': '(no SKILL.md found)'}
    
    content = skill_md.read_text(encoding='utf-8', errors='ignore')
    
    # Parse YAML frontmatter
    frontmatter = {}
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            yaml_content = parts[1].strip()
            for line in yaml_content.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip()
    
    return {
        'name': frontmatter.get('name', skill_path.name),
        'description': frontmatter.get('description', '(no description)'),
        'version': frontmatter.get('version', ''),
        'author': frontmatter.get('author', ''),
    }


def get_all_skills() -> List[Dict]:
    """Get all skills from the source directory."""
    source_dir = get_source_dir()
    if not source_dir.exists():
        return []
    
    skills = []
    for item in sorted(source_dir.iterdir()):
        if item.is_dir() and not item.name.startswith('.'):
            metadata = parse_skill_frontmatter(item)
            metadata['path'] = str(item)
            metadata['files'] = list_skill_files(item)
            skills.append(metadata)
    
    return skills


def list_skill_files(skill_path: Path) -> List[str]:
    """List files in a skill directory."""
    files = []
    for item in skill_path.rglob('*'):
        if item.is_file():
            files.append(str(item.relative_to(skill_path)))
    return files


def get_skill_size(skill_path: Path) -> str:
    """Get total size of a skill directory."""
    total = sum(f.stat().st_size for f in skill_path.rglob('*') if f.is_file())
    if total < 1024:
        return f"{total} B"
    elif total < 1024 * 1024:
        return f"{total / 1024:.1f} KB"
    else:
        return f"{total / (1024 * 1024):.1f} MB"


def is_synced(skill_name: str, agent: str) -> Tuple[bool, str]:
    """Check if a skill is synced to an agent directory."""
    agent_dir = get_agent_dir(agent)
    skill_link = agent_dir / skill_name
    
    if not skill_link.exists():
        return False, 'not synced'
    
    # Check if it's a junction/symlink
    if skill_link.is_symlink():
        return True, 'symlink'
    
    # On Windows, check for junction
    if os.name == 'nt':
        try:
            # Check if it's a junction point
            import ctypes
            FILE_ATTRIBUTE_REPARSE_POINT = 0x400
            attrs = ctypes.windll.kernel32.GetFileAttributesW(str(skill_link))
            if attrs != -1 and attrs & FILE_ATTRIBUTE_REPARSE_POINT:
                return True, 'junction'
        except:
            pass
    
    # It's a regular directory (copied, not linked)
    return True, 'copy'


def create_junction(source: Path, target: Path) -> bool:
    """Create a junction/symlink from source to target."""
    if target.exists():
        return False
    
    # Ensure parent directory exists
    target.parent.mkdir(parents=True, exist_ok=True)
    
    if os.name == 'nt':
        # Windows: use mklink /J for junction
        try:
            result = subprocess.run(
                ['cmd', '/c', 'mklink', '/J', str(target), str(source)],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except Exception as e:
            print(f"Error creating junction: {e}", file=sys.stderr)
            return False
    else:
        # Unix: use symlink
        try:
            target.symlink_to(source)
            return True
        except Exception as e:
            print(f"Error creating symlink: {e}", file=sys.stderr)
            return False


def remove_link(target: Path) -> bool:
    """Remove a junction/symlink."""
    if not target.exists():
        return False
    
    if os.name == 'nt':
        # Windows: junctions are removed with rmdir
        try:
            import shutil
            if target.is_dir():
                # Check if it's a junction
                import ctypes
                FILE_ATTRIBUTE_REPARSE_POINT = 0x400
                attrs = ctypes.windll.kernel32.GetFileAttributesW(str(target))
                if attrs != -1 and attrs & FILE_ATTRIBUTE_REPARSE_POINT:
                    # It's a junction, use rmdir
                    os.rmdir(target)
                else:
                    # Regular directory - don't remove
                    print(f"Warning: {target} is not a junction, skipping", file=sys.stderr)
                    return False
            return True
        except Exception as e:
            print(f"Error removing junction: {e}", file=sys.stderr)
            return False
    else:
        # Unix: unlink symlink
        try:
            if target.is_symlink():
                target.unlink()
                return True
            else:
                print(f"Warning: {target} is not a symlink, skipping", file=sys.stderr)
                return False
        except Exception as e:
            print(f"Error removing symlink: {e}", file=sys.stderr)
            return False


# ============== Commands ==============

def cmd_list(args):
    """List all installed skills."""
    skills = get_all_skills()
    
    if args.search:
        search_lower = args.search.lower()
        skills = [s for s in skills if 
                  search_lower in s['name'].lower() or 
                  search_lower in s['description'].lower()]
    
    if args.format == 'json':
        print(json.dumps(skills, indent=2))
        return
    
    if not skills:
        print("No skills found in ~/.agents/skills/")
        return
    
    # Table format
    name_width = max(len(s['name']) for s in skills)
    name_width = max(name_width, 20)
    name_width = min(name_width, 30)
    desc_width = 50
    
    print(f"{'Skill Name':<{name_width}} | Description")
    print(f"{'-' * name_width}-+-{'-' * desc_width}")
    
    for skill in skills:
        name = skill['name'][:name_width]
        desc = skill['description'][:desc_width]
        if len(skill['description']) > desc_width:
            desc = desc[:desc_width-3] + '...'
        print(f"{name:<{name_width}} | {desc}")
    
    print(f"\nTotal: {len(skills)} skills installed")


def cmd_status(args):
    """Show sync status of all skills."""
    skills = get_all_skills()
    
    if not skills:
        print("No skills found in ~/.agents/skills/")
        return
    
    agents = ['cursor', 'claude', 'codex']
    name_width = max(len(s['name']) for s in skills)
    name_width = max(name_width, 20)
    name_width = min(name_width, 30)
    
    # Header
    print(f"{'Skill':<{name_width}} | Cursor | Claude | Codex")
    print(f"{'-' * name_width}-+--------+--------+--------")
    
    for skill in skills:
        name = skill['name'][:name_width]
        statuses = []
        for agent in agents:
            synced, link_type = is_synced(skill['name'], agent)
            if synced:
                statuses.append('  [x]  ')
            else:
                statuses.append('  [ ]  ')
        
        print(f"{name:<{name_width}} |{statuses[0]}|{statuses[1]}|{statuses[2]}")
    
    print(f"\nTotal: {len(skills)} skills")


def cmd_sync(args):
    """Sync skills to agent directories."""
    skills = get_all_skills()
    source_dir = get_source_dir()
    
    if not skills:
        print("No skills found in ~/.agents/skills/")
        return
    
    agents = ['cursor', 'claude', 'codex']
    if args.target:
        if args.target not in agents:
            print(f"Unknown agent: {args.target}")
            return
        agents = [args.target]
    
    created = 0
    skipped = 0
    
    print(f"Syncing skills from {source_dir}...")
    print()
    
    for skill in skills:
        skill_source = Path(skill['path'])
        synced_to = []
        newly_synced = []
        
        for agent in agents:
            agent_dir = get_agent_dir(agent)
            skill_target = agent_dir / skill['name']
            
            is_linked, link_type = is_synced(skill['name'], agent)
            
            if is_linked:
                synced_to.append(agent)
            else:
                if args.dry_run:
                    newly_synced.append(agent)
                else:
                    if create_junction(skill_source, skill_target):
                        newly_synced.append(agent)
                        created += 1
                    else:
                        skipped += 1
        
        # Output status
        if newly_synced:
            print(f"[+] {skill['name']} -> {', '.join(newly_synced)} (newly synced)")
        elif synced_to:
            print(f"[ok] {skill['name']} -> {', '.join(synced_to)}")
    
    print()
    if args.dry_run:
        print(f"[DRY RUN] Would create {created} new links")
    else:
        print(f"Sync complete: {len(skills)} skills, {created} new links created")


def cmd_info(args):
    """Show detailed info about a skill."""
    skill_name = args.skill_name
    source_dir = get_source_dir()
    skill_path = source_dir / skill_name
    
    if not skill_path.exists():
        print(f"Skill not found: {skill_name}")
        print(f"Available skills: {', '.join(s.name for s in source_dir.iterdir() if s.is_dir())}")
        return
    
    metadata = parse_skill_frontmatter(skill_path)
    files = list_skill_files(skill_path)
    size = get_skill_size(skill_path)
    
    print(f"+{'=' * 60}+")
    print(f"| Skill: {metadata['name']:<51}|")
    print(f"+{'=' * 60}+")
    
    # Description (word wrap)
    desc = metadata['description']
    desc_lines = [desc[i:i+56] for i in range(0, len(desc), 56)]
    for i, line in enumerate(desc_lines[:3]):
        if i == 0:
            print(f"| Description: {line:<46}|")
        else:
            print(f"|              {line:<46}|")
    
    print(f"+{'=' * 60}+")
    print(f"| Location: {str(skill_path):<49}|")
    print(f"| Files: {len(files)} file(s)".ljust(61) + "|")
    print(f"| Size: {size:<53}|")
    
    if metadata.get('version'):
        print(f"| Version: {metadata['version']:<50}|")
    if metadata.get('author'):
        print(f"| Author: {metadata['author']:<51}|")
    
    print(f"+{'=' * 60}+")
    print(f"| Sync Status:".ljust(62) + "|")
    
    for agent in ['cursor', 'claude', 'codex']:
        synced, link_type = is_synced(skill_name, agent)
        status = f"[x] synced ({link_type})" if synced else "[ ] not synced"
        print(f"|   {agent.capitalize()}: {status:<50}|")
    
    print(f"+{'=' * 60}+")


def cmd_enable(args):
    """Enable a skill for a specific agent."""
    skill_name = args.skill_name
    agent = args.target
    
    source_dir = get_source_dir()
    skill_source = source_dir / skill_name
    
    if not skill_source.exists():
        print(f"Skill not found: {skill_name}")
        return
    
    if agent not in AGENT_DIRS:
        print(f"Unknown agent: {agent}. Choose from: cursor, claude, codex")
        return
    
    agent_dir = get_agent_dir(agent)
    skill_target = agent_dir / skill_name
    
    is_linked, link_type = is_synced(skill_name, agent)
    if is_linked:
        print(f"Skill {skill_name} is already enabled for {agent} ({link_type})")
        return
    
    if create_junction(skill_source, skill_target):
        print(f"[ok] Enabled {skill_name} for {agent}")
    else:
        print(f"[FAIL] Failed to enable {skill_name} for {agent}")


def cmd_disable(args):
    """Disable a skill for a specific agent."""
    skill_name = args.skill_name
    agent = args.target
    
    if agent not in AGENT_DIRS:
        print(f"Unknown agent: {agent}. Choose from: cursor, claude, codex")
        return
    
    agent_dir = get_agent_dir(agent)
    skill_target = agent_dir / skill_name
    
    is_linked, link_type = is_synced(skill_name, agent)
    if not is_linked:
        print(f"Skill {skill_name} is not enabled for {agent}")
        return
    
    if link_type == 'copy':
        print(f"Warning: {skill_name} is a copy, not a link. Manual removal required.")
        return
    
    if remove_link(skill_target):
        print(f"[ok] Disabled {skill_name} for {agent}")
    else:
        print(f"[FAIL] Failed to disable {skill_name} for {agent}")


def main():
    parser = argparse.ArgumentParser(
        description='Manage locally installed agent skills',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # list command
    list_parser = subparsers.add_parser('list', help='List all installed skills')
    list_parser.add_argument('--format', choices=['table', 'json'], default='table',
                            help='Output format')
    list_parser.add_argument('--search', '-s', help='Filter by keyword')
    
    # status command
    status_parser = subparsers.add_parser('status', help='Show sync status')
    
    # sync command
    sync_parser = subparsers.add_parser('sync', help='Sync skills to agent directories')
    sync_parser.add_argument('--dry-run', '-n', action='store_true',
                            help='Preview changes without applying')
    sync_parser.add_argument('--target', '-t', choices=['cursor', 'claude', 'codex'],
                            help='Sync to specific agent only')
    
    # info command
    info_parser = subparsers.add_parser('info', help='Show skill details')
    info_parser.add_argument('skill_name', help='Name of the skill')
    
    # enable command
    enable_parser = subparsers.add_parser('enable', help='Enable a skill for an agent')
    enable_parser.add_argument('skill_name', help='Name of the skill')
    enable_parser.add_argument('--target', '-t', required=True,
                              choices=['cursor', 'claude', 'codex'],
                              help='Target agent')
    
    # disable command
    disable_parser = subparsers.add_parser('disable', help='Disable a skill for an agent')
    disable_parser.add_argument('skill_name', help='Name of the skill')
    disable_parser.add_argument('--target', '-t', required=True,
                               choices=['cursor', 'claude', 'codex'],
                               help='Target agent')
    
    args = parser.parse_args()
    
    if args.command == 'list':
        cmd_list(args)
    elif args.command == 'status':
        cmd_status(args)
    elif args.command == 'sync':
        cmd_sync(args)
    elif args.command == 'info':
        cmd_info(args)
    elif args.command == 'enable':
        cmd_enable(args)
    elif args.command == 'disable':
        cmd_disable(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
