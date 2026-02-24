#!/usr/bin/env python3
"""
Update query_tool.py paths in all skill documentation files.
Make the paths relative and simpler.
"""

import os
import re
from pathlib import Path

def update_file(file_path):
    """Update query paths in a single file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Replace absolute paths with relative paths
    # Pattern 1: python3 skills/lixinger-data-query/scripts/query_tool.py
    # Keep as is - this is already good
    
    # Pattern 2: python3 /Users/.../query_tool.py -> python3 skills/lixinger-data-query/scripts/query_tool.py
    content = re.sub(
        r'python3 /[^\s]+/skills/lixinger-data-query/scripts/query_tool\.py',
        'python3 skills/lixinger-data-query/scripts/query_tool.py',
        content
    )
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Update all skill documentation files."""
    base_dir = Path('skills')
    updated_files = []
    
    # Find all data-queries.md files
    for md_file in base_dir.rglob('data-queries.md'):
        if update_file(md_file):
            updated_files.append(str(md_file))
    
    # Find all SKILL.md files
    for md_file in base_dir.rglob('SKILL.md'):
        if update_file(md_file):
            updated_files.append(str(md_file))
    
    print(f"Updated {len(updated_files)} files:")
    for f in updated_files:
        print(f"  - {f}")

if __name__ == '__main__':
    main()
