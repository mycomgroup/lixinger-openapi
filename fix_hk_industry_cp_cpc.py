#!/usr/bin/env python3
"""
Fix HK industry fundamental API - remove cp and cpc metrics
"""
import re

file_path = "skills/HK-market/hk-sector-rotation/references/data-queries.md"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern 1: Remove cp and cpc from metricsList in hk/industry/fundamental/hsi queries
# Match: "metricsList": ["cp", "cpc", "ta", "mc", ...] 
# Replace: "metricsList": ["ta", "mc", ...]

# Remove "cp", "cpc", from metricsList
content = re.sub(
    r'("metricsList":\s*\[)"cp",\s*"cpc",\s*',
    r'\1',
    content
)

# Remove "cpc", "ta" -> "ta"
content = re.sub(
    r'("metricsList":\s*\[)"cpc",\s*"ta"',
    r'\1"ta"',
    content
)

# Remove standalone "cpc" in metricsList
content = re.sub(
    r'("metricsList":\s*\[)"cpc"(\])',
    r'\1\2',
    content
)

# Remove "cp", "cpc" from metricsList
content = re.sub(
    r'("metricsList":\s*\[.*?)"cp",\s*"cpc",\s*',
    r'\1',
    content
)

# Remove cp, cpc from columns parameter
content = re.sub(
    r'(--columns\s+"[^"]*?)cp,cpc,',
    r'\1',
    content
)

content = re.sub(
    r'(--columns\s+"[^"]*?)cp,',
    r'\1',
    content
)

content = re.sub(
    r'(--columns\s+"[^"]*?)cpc,',
    r'\1',
    content
)

content = re.sub(
    r'(--columns\s+"[^"]*?),cpc"',
    r'\1"',
    content
)

# Update descriptions to remove cp/cpc references
content = re.sub(
    r'- `cp`: 收盘点位\n',
    '',
    content
)

content = re.sub(
    r'- `cpc`: 涨跌幅（%）\n',
    '',
    content
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ Fixed {file_path}")
print("Removed cp and cpc metrics from hk/industry/fundamental/hsi queries")
