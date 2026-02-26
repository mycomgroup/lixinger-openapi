#!/bin/bash

# 批量修复所有 data-queries.md 文件中的 API 路径错误
# 将点号格式改为斜杠格式

echo "开始批量修复 API 路径..."
echo ""

# 查找所有 data-queries.md 文件
files=$(find skills -name "data-queries.md")

total=0
fixed=0

for file in $files; do
    total=$((total + 1))
    
    # 检查文件是否包含点号格式的 API 路径
    if grep -q 'suffix "cn/index\.' "$file" || \
       grep -q 'suffix "cn/company\.' "$file" || \
       grep -q 'suffix "hk/index\.' "$file" || \
       grep -q 'suffix "hk/company\.' "$file" || \
       grep -q 'suffix "us/index\.' "$file" || \
       grep -q 'suffix "us/company\.' "$file"; then
        
        echo "修复: $file"
        
        # 创建备份
        cp "$file" "$file.bak"
        
        # 修复常见的点号格式 API 路径
        sed -i '' \
            -e 's|cn/index\.constituent|cn/index/constituents|g' \
            -e 's|cn/index\.k-line|cn/index/k-line|g' \
            -e 's|cn/company\.equity-pledge|cn/company/pledge|g' \
            -e 's|cn/company\.trading-abnormal|cn/company/trading-abnormal|g' \
            -e 's|hk/index\.constituent|hk/index/constituents|g' \
            -e 's|hk/index\.k-line|hk/index/k-line|g' \
            -e 's|us/index\.constituent|us/index/constituents|g' \
            -e 's|us/index\.k-line|us/index/k-line|g' \
            "$file"
        
        fixed=$((fixed + 1))
    fi
done

echo ""
echo "修复完成!"
echo "总文件数: $total"
echo "修复文件数: $fixed"
echo ""
echo "备份文件已保存为 .bak 后缀"
