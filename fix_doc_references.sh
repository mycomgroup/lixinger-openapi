#!/bin/bash

# 修复文档中的路径引用，将 `skills/lixinger-data-query` 改为相对路径

echo "开始修复文档引用路径..."

# 修复 .claude/skills/ 目录下的文件（使用相对路径 ../../lixinger-data-query 或 ../../../lixinger-data-query）
find .claude/skills -name "*.md" -type f | while read file; do
    # 跳过 lixinger-data-query 目录本身
    if [[ "$file" == *"/lixinger-data-query/"* ]]; then
        continue
    fi
    
    # 检查文件是否包含 `skills/lixinger-data-query
    if grep -q '`skills/lixinger-data-query' "$file"; then
        echo "修复: $file"
        
        # 根据文件深度确定相对路径
        # 如果在 references/ 子目录，使用 ../../lixinger-data-query
        # 否则使用 ../lixinger-data-query
        if [[ "$file" == *"/references/"* ]]; then
            sed -i '' 's|`skills/lixinger-data-query|`../../lixinger-data-query|g' "$file"
        else
            sed -i '' 's|`skills/lixinger-data-query|`../lixinger-data-query|g' "$file"
        fi
    fi
done

# 修复根目录的 README 文件（使用 .claude/skills/lixinger-data-query）
for file in README.md README_NEW.md; do
    if [ -f "$file" ] && grep -q '`skills/lixinger-data-query' "$file"; then
        echo "修复: $file"
        sed -i '' 's|`skills/lixinger-data-query|`.claude/skills/lixinger-data-query|g' "$file"
    fi
done

# 修复 docs/ 目录（使用 ../.claude/skills/lixinger-data-query）
find docs -name "*.md" -type f 2>/dev/null | while read file; do
    if grep -q '`skills/lixinger-data-query' "$file"; then
        echo "修复: $file"
        sed -i '' 's|`skills/lixinger-data-query|`../.claude/skills/lixinger-data-query|g' "$file"
    fi
done

# 修复 regression_tests/ 目录（使用 ../.claude/skills/lixinger-data-query）
find regression_tests -name "*.md" -type f 2>/dev/null | while read file; do
    if grep -q '`skills/lixinger-data-query' "$file"; then
        echo "修复: $file"
        sed -i '' 's|`skills/lixinger-data-query|`../.claude/skills/lixinger-data-query|g' "$file"
    fi
done

echo "完成！"
