#!/bin/bash
# Fix macro/money-supply API calls to include required areaCode and metricsList parameters

echo "Fixing macro/money-supply API calls..."

# Find all data-queries.md files with macro/money-supply
files=$(grep -l "macro/money-supply" skills/*/references/data-queries.md 2>/dev/null)

for file in $files; do
    echo "Processing: $file"
    
    # Check if file contains the old pattern
    if grep -q '"macro/money-supply".*--params.*"date".*"2026-02-24"' "$file"; then
        # Replace the old pattern with the new one
        # Old: --params '{"date": "2026-02-24"}' --columns "date,m0,m1,m2"
        # New: --params '{"areaCode": "cn", "startDate": "2025-02-01", "endDate": "2026-02-24", "metricsList": ["m.m0.t", "m.m1.t", "m.m2.t"]}' --columns "date,m0,m1,m2"
        
        sed -i '' 's|--suffix "macro/money-supply" \\\
  --params '\''{"date": "2026-02-24"}'\'' \\\
  --columns "date,m0,m1,m2"|--suffix "macro/money-supply" \\\
  --params '\''{"areaCode": "cn", "startDate": "2025-02-01", "endDate": "2026-02-24", "metricsList": ["m.m0.t", "m.m1.t", "m.m2.t"]}'\'' \\\
  --columns "date,m0,m1,m2"|g' "$file"
        
        echo "  ✅ Fixed"
    else
        echo "  ⏭️  Skipped (pattern not found)"
    fi
done

echo ""
echo "Done! Fixed macro/money-supply API calls."
