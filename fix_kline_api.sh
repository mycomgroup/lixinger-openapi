#!/bin/bash

# 修复所有 k-line API 路径错误
# cn/index/k-line -> cn/index/candlestick
# hk/index/k-line -> hk/index/candlestick  
# us/index/k-line -> us/index/candlestick

echo "修复 K线 API 路径..."
echo ""

files=$(find skills -name "data-queries.md")

for file in $files; do
    if grep -q 'k-line' "$file"; then
        echo "修复: $file"
        
        # 修复 API 路径
        sed -i '' \
            -e 's|cn/index/k-line|cn/index/candlestick|g' \
            -e 's|hk/index/k-line|hk/index/candlestick|g' \
            -e 's|us/index/k-line|us/index/candlestick|g' \
            -e 's|cn/company/k-line|cn/company/candlestick|g' \
            -e 's|hk/company/k-line|hk/company/candlestick|g' \
            "$file"
        
        # 修复参数：indexCode -> stockCode, 添加 type 参数
        sed -i '' \
            -e 's|"indexCode":|"stockCode":|g' \
            "$file"
    fi
done

echo ""
echo "修复完成!"
