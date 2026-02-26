#!/usr/bin/env python3
"""
Fix HK company candlestick API - add missing type parameter
"""
import re
import glob

files = glob.glob("skills/HK-market/*/references/data-queries.md")

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Pattern: hk/company/candlestick with stockCode parameter but missing type
    # Add "type": "normal" to params
    
    # Match: --params '{"stockCode": "00700", "startDate": ...}'
    # Replace: --params '{"stockCode": "00700", "type": "normal", "startDate": ...}'
    content = re.sub(
        r'(--suffix "hk/company/candlestick"[^\n]*\n[^\n]*--params \'\{"stockCode": "[^"]+"),\s*("startDate")',
        r'\1, "type": "normal", \2',
        content
    )
    
    # Match: --params '{"stockCodes": ["00005"], "startDate": ...}'
    # Replace: --params '{"stockCodes": ["00005"], "type": "normal", "startDate": ...}'
    content = re.sub(
        r'(--suffix "hk/company/candlestick"[^\n]*\n[^\n]*--params \'\{"stockCodes": \[[^\]]+\]),\s*("startDate")',
        r'\1, "type": "normal", \2',
        content
    )
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Fixed {file_path}")

print("Done!")
