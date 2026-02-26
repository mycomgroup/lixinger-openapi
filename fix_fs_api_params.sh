#!/bin/bash

# 修复 fs/non_financial API 的参数错误
# stockCode -> stockCodes (数组格式)

echo "修复 fs/non_financial API 参数..."
echo ""

files=$(find skills -name "data-queries.md")

for file in $files; do
    if grep -q 'cn/company/fs/non_financial\|hk/company/fs/non_financial\|us/company/fs/non_financial' "$file"; then
        if grep -q '"stockCode":' "$file"; then
            echo "修复: $file"
            
            # 将 "stockCode": "xxx" 改为 "stockCodes": ["xxx"]
            sed -i '' \
                -e 's|"stockCode": "\([^"]*\)"|"stockCodes": ["\1"]|g' \
                "$file"
        fi
    fi
done

echo ""
echo "修复完成!"
