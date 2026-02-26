#!/usr/bin/env python3
"""
Fix macro API calls to include required parameters
"""
import re
from pathlib import Path

def fix_macro_money_supply(content):
    """Fix macro/money-supply API calls"""
    # Pattern 1: with --limit 20
    old_pattern1 = '--suffix "macro/money-supply" \\\n  --params \'{"date": "2026-02-24"}\' \\\n  --columns "date,m0,m1,m2" \\\n  --limit 20'
    new_format1 = '--suffix "macro/money-supply" \\\n  --params \'{"areaCode": "cn", "startDate": "2025-02-01", "endDate": "2026-02-24", "metricsList": ["m.m0.t", "m.m1.t", "m.m2.t"]}\' \\\n  --columns "date,m0,m1,m2" \\\n  --limit 20'
    
    # Pattern 2: without --limit
    old_pattern2 = '--suffix "macro/money-supply" \\\n  --params \'{"date": "2026-02-24"}\' \\\n  --columns "date,m0,m1,m2"'
    new_format2 = '--suffix "macro/money-supply" \\\n  --params \'{"areaCode": "cn", "startDate": "2025-02-01", "endDate": "2026-02-24", "metricsList": ["m.m0.t", "m.m1.t", "m.m2.t"]}\' \\\n  --columns "date,m0,m1,m2"'
    
    fixed = False
    if old_pattern1 in content:
        content = content.replace(old_pattern1, new_format1)
        fixed = True
    elif old_pattern2 in content:
        content = content.replace(old_pattern2, new_format2)
        fixed = True
    
    return content, fixed

def fix_macro_gdp(content):
    """Fix macro/gdp API calls"""
    old_pattern = '--suffix "macro/gdp" \\\n  --params \'{}\''
    new_format = '--suffix "macro/gdp" \\\n  --params \'{"areaCode": "cn", "startDate": "2025-01-01", "endDate": "2026-02-24", "metricsList": ["q.gdp.t", "q.gdp.t_y2y"]}\' \\\n  --limit 20'
    
    if old_pattern in content:
        content = content.replace(old_pattern, new_format)
        return content, True
    
    return content, False

def fix_macro_price_index(content):
    """Fix macro/price-index API calls"""
    old_pattern = '--suffix "macro/price-index" \\\n  --params \'{}\''
    new_format = '--suffix "macro/price-index" \\\n  --params \'{"areaCode": "cn", "startDate": "2025-01-01", "endDate": "2026-02-24", "metricsList": ["m.cpi.t", "m.ppi.t"]}\' \\\n  --limit 20'
    
    if old_pattern in content:
        content = content.replace(old_pattern, new_format)
        return content, True
    
    return content, False

def main():
    print("=" * 80)
    print("Fixing macro API calls")
    print("=" * 80)
    print()
    
    # Find all data-queries.md files
    skills_dir = Path("skills")
    all_files = []
    
    for market in ["China-market", "HK-market", "US-market"]:
        market_dir = skills_dir / market
        if market_dir.exists():
            for skill_dir in market_dir.iterdir():
                if skill_dir.is_dir():
                    data_queries = skill_dir / "references" / "data-queries.md"
                    if data_queries.exists():
                        all_files.append(data_queries)
    
    print(f"Found {len(all_files)} data-queries.md files")
    print()
    
    fixed_count = 0
    for file_path in all_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Try all fixes
        content, fixed1 = fix_macro_money_supply(content)
        content, fixed2 = fix_macro_gdp(content)
        content, fixed3 = fix_macro_price_index(content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            fixes = []
            if fixed1:
                fixes.append("money-supply")
            if fixed2:
                fixes.append("gdp")
            if fixed3:
                fixes.append("price-index")
            print(f"✅ Fixed {', '.join(fixes)}: {file_path}")
            fixed_count += 1
    
    print()
    print("=" * 80)
    print(f"Summary: Fixed {fixed_count} files")
    print("=" * 80)

if __name__ == '__main__':
    main()
