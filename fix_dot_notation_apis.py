#!/usr/bin/env python3
"""
修复所有使用点号格式的 API 路径
"""
import re
from pathlib import Path

# 查找所有 data-queries.md 文件
def find_all_data_queries_files():
    skills_dir = Path("skills")
    files = []
    
    for market in ["China-market", "HK-market", "US-market"]:
        market_dir = skills_dir / market
        if market_dir.exists():
            for skill_dir in market_dir.iterdir():
                if skill_dir.is_dir():
                    data_queries = skill_dir / "references" / "data-queries.md"
                    if data_queries.exists():
                        files.append(data_queries)
    
    return sorted(files)

# 修复点号格式
def fix_dot_notation(content):
    # 匹配 --suffix "xxx.yyy" 格式，但排除已经是斜杠的
    # 匹配模式：--suffix "cn/company.xxx" 或 --suffix "cn.company.xxx"
    pattern = r'--suffix "([^"]+)"'
    
    def replace_dots(match):
        path = match.group(1)
        # 只替换路径中的点号为斜杠
        if '.' in path:
            # 替换所有点号为斜杠
            new_path = path.replace('.', '/')
            return f'--suffix "{new_path}"'
        return match.group(0)
    
    return re.sub(pattern, replace_dots, content)

# 主函数
def main():
    files = find_all_data_queries_files()
    fixed_count = 0
    
    print(f"找到 {len(files)} 个 data-queries.md 文件")
    print()
    
    for file_path in files:
        content = file_path.read_text(encoding='utf-8')
        new_content = fix_dot_notation(content)
        
        if content != new_content:
            file_path.write_text(new_content, encoding='utf-8')
            fixed_count += 1
            print(f"✅ 修复: {file_path}")
    
    print()
    print(f"✅ 总共修复了 {fixed_count} 个文件")

if __name__ == '__main__':
    main()
