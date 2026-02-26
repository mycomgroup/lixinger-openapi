#!/bin/bash

# 为所有 candlestick API 添加 type 参数

echo "为 candlestick API 添加 type 参数..."
echo ""

files=$(find skills -name "data-queries.md")

for file in $files; do
    if grep -q 'cn/index/candlestick\|hk/index/candlestick\|us/index/candlestick\|cn/company/candlestick\|hk/company/candlestick' "$file"; then
        echo "修复: $file"
        
        # 为 candlestick API 添加 type 参数
        # 在 stockCode 后面添加 "type": "normal"
        sed -i '' \
            -e 's|"stockCode": "\([^"]*\)", "startDate"|"stockCode": "\1", "type": "normal", "startDate"|g' \
            -e 's|"stockCode": "\([^"]*\)", "endDate"|"stockCode": "\1", "type": "normal", "endDate"|g' \
            -e 's|"stockCode": "\([^"]*\)", "date"|"stockCode": "\1", "type": "normal", "date"|g' \
            "$file"
    fi
done

echo ""
echo "修复完成!"
