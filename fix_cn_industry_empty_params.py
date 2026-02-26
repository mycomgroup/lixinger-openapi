#!/usr/bin/env python3
"""
Fix cn/industry API calls with empty params in US market files
"""
import re
from pathlib import Path

files_to_fix = [
    "skills/US-market/us-dividend-aristocrat-calculator/references/data-queries.md",
    "skills/US-market/us-etf-allocator/references/data-queries.md",
    "skills/US-market/us-event-driven-detector/references/data-queries.md",
    "skills/US-market/us-macro-liquidity-monitor/references/data-queries.md",
    "skills/US-market/us-policy-sensitivity-brief/references/data-queries.md",
    "skills/US-market/us-portfolio-health-check/references/data-queries.md",
    "skills/US-market/us-quant-factor-screener/references/data-queries.md",
    "skills/US-market/us-risk-adjusted-return-optimizer/references/data-queries.md",
    "skills/US-market/us-sentiment-reality-gap/references/data-queries.md",
    "skills/US-market/us-small-cap-growth-identifier/references/data-queries.md",
    "skills/US-market/us-tech-hype-vs-fundamentals/references/data-queries.md",
    "skills/US-market/us-valuation-regime-detector/references/data-queries.md",
]

# Pattern to match cn/industry with empty params (with newlines)
pattern = r'(--suffix "cn/industry"\s+\\\s+--params) \'\{\}\''
replacement = r'\1 \'{"source": "sw", "level": "one"}\' \\\n  --limit 20'

fixed_count = 0
for file_path in files_to_fix:
    path = Path(file_path)
    if not path.exists():
        print(f"⚠️  File not found: {file_path}")
        continue
    
    content = path.read_text(encoding='utf-8')
    
    # Check if pattern exists
    if re.search(pattern, content):
        new_content = re.sub(pattern, replacement, content)
        path.write_text(new_content, encoding='utf-8')
        fixed_count += 1
        print(f"✅ Fixed: {file_path}")
    else:
        print(f"⏭️  No match: {file_path}")

print(f"\n✅ Total files fixed: {fixed_count}")
