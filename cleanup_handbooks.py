#!/usr/bin/env python3
"""
Remove specific sections from alert handbooks:
1. "责任团队: XXX团队负责处理此类告警。" line
2. Entire "Grafana 仪表板参考" section
"""

import re
from pathlib import Path

def cleanup_handbook(filepath):
    """Remove specified sections from a handbook file."""

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Remove "**责任团队:** XXX团队负责处理此类告警。" line
    # Pattern matches the line with any team name
    content = re.sub(
        r'\n\*\*责任团队:\*\* .+?负责处理此类告警。\n',
        '\n',
        content
    )

    # Remove the entire "## Grafana 仪表板参考" section
    # This section goes from "## Grafana 仪表板参考" to the next "---" or end of file
    content = re.sub(
        r'## Grafana 仪表板参考\n\n.*?(?=\n---|\Z)',
        '',
        content,
        flags=re.DOTALL
    )

    # Clean up any resulting double blank lines or trailing "---"
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = re.sub(r'\n---\s*$', '\n', content)
    content = content.rstrip() + '\n'

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    handbook_dir = Path("/app/luckin-alerts-repo/alert-handbooks")
    modified_count = 0

    print("Cleaning up alert handbooks...")
    print("-" * 50)

    for filepath in sorted(handbook_dir.glob("ALR-*.md")):
        if cleanup_handbook(filepath):
            print(f"Cleaned: {filepath.name}")
            modified_count += 1

    print("-" * 50)
    print(f"Modified {modified_count} files")

if __name__ == "__main__":
    main()
