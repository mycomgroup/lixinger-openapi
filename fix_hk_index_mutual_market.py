#!/usr/bin/env python3
"""
批量修复 hk/index.mutual-market API 调用
1. 修复路径格式：hk/index.mutual-market → hk/index/mutual-market
2. 修复参数：indexCode → stockCode
3. 添加 metricsList 参数
"""
import re
from pathlib import Path

def fix_hk_index_mutual_market(file_path):
    """修复单个文件中的 hk/index.mutual-market API 调用"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes = []
    
    # 修复 API 路径格式和参数
    # 匹配模式：--suffix "hk/index.mutual-market" --params '{"indexCode": ...}'
    pattern = r'--suffix "hk/index\.mutual-market"\s+--params \'(\{[^}]+\})\''
    
    def fix_params(match):
        params_str = match.group(1)
        # 替换 indexCode 为 stockCode
        params_str = params_str.replace('"indexCode":', '"stockCode":')
        # 添加 metricsList 如果不存在
        if '"metricsList"' not in params_str:
            params_str = params_str.rstrip('}') + ', "metricsList": ["shareholdingsMoney"]}'
        return f'--suffix "hk/index/mutual-market" --params \'{params_str}\''
    
    if re.search(pattern, content):
        content = re.sub(pattern, fix_params, content)
        changes.append("hk/index.mutual-market: 修复路径格式、参数名称并添加 metricsList")
    
    # 修复 API 列表中的路径
    content = content.replace('hk/index.mutual-market', 'hk/index/mutual-market')
    
    # 如果有修改，写回文件
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, changes
    
    return False, []

def main():
    """主函数"""
    print("=" * 80)
    print("批量修复 hk/index.mutual-market API 调用")
    print("=" * 80)
    print()
    
    # 查找所有 data-queries.md 文件
    skills_dir = Path("skills")
    files = list(skills_dir.glob("*/*/references/data-queries.md"))
    
    print(f"找到 {len(files)} 个 data-queries.md 文件")
    print()
    
    fixed_count = 0
    for file_path in files:
        modified, changes = fix_hk_index_mutual_market(file_path)
        if modified:
            fixed_count += 1
            print(f"✅ 修复: {file_path}")
            for change in changes:
                print(f"   - {change}")
    
    print()
    print("=" * 80)
    print(f"修复完成: {fixed_count} 个文件")
    print("=" * 80)

if __name__ == '__main__':
    main()
