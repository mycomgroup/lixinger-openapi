#!/usr/bin/env python3
"""
测试所有 data-queries.md 文件中的示例命令
"""
import os
import re
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Tuple

def find_all_data_queries_files() -> List[Path]:
    """查找所有 data-queries.md 文件"""
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

def extract_examples_from_file(file_path: Path) -> List[Dict]:
    """从 data-queries.md 文件中提取示例命令"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    examples = []
    
    # 匹配代码块中的 python3 命令
    # 匹配 ```bash 或 ```sh 代码块
    code_blocks = re.findall(r'```(?:bash|sh)\n(.*?)```', content, re.DOTALL)
    
    for block in code_blocks:
        # 查找 python3 query_tool.py 命令
        lines = block.strip().split('\n')
        command_lines = []
        in_command = False
        skip_block = False
        
        # 检查是否包含循环语句、变量替换或输出重定向
        block_text = '\n'.join(lines)
        if any([
            'for ' in block_text and ' in ' in block_text,
            '${' in block_text,  # 变量替换
            ' > ' in block_text and '.csv' in block_text,  # 输出重定向到文件
        ]):
            skip_block = True
        
        if skip_block:
            continue
        
        for line in lines:
            # 跳过注释
            if line.strip().startswith('#'):
                continue
            
            # 检测命令开始
            if 'python3' in line and 'query_tool.py' in line:
                in_command = True
                command_lines = [line]
            elif in_command:
                # 继续收集多行命令
                if line.strip().endswith('\\'):
                    command_lines.append(line)
                elif line.strip():
                    command_lines.append(line)
                    # 命令结束
                    full_command = ' '.join(command_lines)
                    examples.append({
                        'file': str(file_path),
                        'command': full_command
                    })
                    in_command = False
                    command_lines = []
                else:
                    # 空行，命令结束
                    if command_lines:
                        full_command = ' '.join(command_lines)
                        examples.append({
                            'file': str(file_path),
                            'command': full_command
                        })
                    in_command = False
                    command_lines = []
    
    return examples

def clean_command(command: str) -> str:
    """清理命令字符串"""
    # 移除反斜杠和多余空格
    command = command.replace('\\', ' ')
    command = re.sub(r'\s+', ' ', command)
    return command.strip()

def run_command(command: str, timeout: int = 60, max_retries: int = 2) -> Tuple[bool, str]:
    """执行命令并返回结果，支持重试"""
    for attempt in range(max_retries):
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if result.returncode == 0:
                return True, result.stdout
            else:
                # Check if it's a network error that should be retried
                error_msg = result.stderr
                if 'SSLError' in error_msg or 'ConnectionError' in error_msg:
                    if attempt < max_retries - 1:
                        continue  # Retry
                return False, error_msg
        except subprocess.TimeoutExpired:
            return False, f"Command timeout after {timeout}s"
        except Exception as e:
            return False, str(e)
    
    return False, "Max retries exceeded"

def main():
    print("=" * 80)
    print("测试所有 data-queries.md 文件中的示例命令")
    print("=" * 80)
    print()
    
    # 查找所有文件
    files = find_all_data_queries_files()
    print(f"✅ 找到 {len(files)} 个 data-queries.md 文件")
    print()
    
    # 提取所有示例
    all_examples = []
    for file_path in files:
        examples = extract_examples_from_file(file_path)
        all_examples.extend(examples)
    
    print(f"✅ 提取到 {len(all_examples)} 个示例命令")
    print()
    
    # 测试每个示例
    results = {
        'total': len(all_examples),
        'passed': 0,
        'failed': 0,
        'details': []
    }
    
    for i, example in enumerate(all_examples, 1):
        file_path = example['file']
        command = clean_command(example['command'])
        
        # 获取 skill 名称
        skill_name = Path(file_path).parent.parent.name
        market = Path(file_path).parent.parent.parent.name
        
        print(f"[{i}/{len(all_examples)}] 测试: {market}/{skill_name}")
        print(f"命令: {command[:100]}..." if len(command) > 100 else f"命令: {command}")
        
        success, output = run_command(command)
        
        if success:
            print(f"✅ 成功")
            results['passed'] += 1
            results['details'].append({
                'market': market,
                'skill': skill_name,
                'file': file_path,
                'command': command,
                'status': 'passed',
                'output': output[:200] if len(output) > 200 else output
            })
        else:
            print(f"❌ 失败")
            print()
            print("=" * 80)
            print("错误详情")
            print("=" * 80)
            print(f"Market: {market}")
            print(f"Skill: {skill_name}")
            print(f"File: {file_path}")
            print(f"Command: {command}")
            print()
            print("错误信息:")
            print(output)
            print("=" * 80)
            
            results['failed'] += 1
            results['details'].append({
                'market': market,
                'skill': skill_name,
                'file': file_path,
                'command': command,
                'status': 'failed',
                'error': output
            })
            
            # 保存当前结果
            output_file = "test_data_queries_results.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            print(f"\n⚠️  遇到错误，测试停止")
            print(f"✅ 部分结果已保存到: {output_file}")
            print(f"进度: {i}/{len(all_examples)} ({results['passed']} 成功, {results['failed']} 失败)")
            
            # 立即退出
            return False
        
        print()
    
    # 输出总结
    print("=" * 80)
    print("测试总结")
    print("=" * 80)
    print(f"总计: {results['total']}")
    print(f"成功: {results['passed']} ({results['passed']/results['total']*100:.1f}%)")
    print(f"失败: {results['failed']} ({results['failed']/results['total']*100:.1f}%)")
    print()
    
    # 保存详细结果
    output_file = "test_data_queries_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 详细结果已保存到: {output_file}")
    
    # 输出失败的命令
    if results['failed'] > 0:
        print()
        print("=" * 80)
        print("失败的命令")
        print("=" * 80)
        for detail in results['details']:
            if detail['status'] == 'failed':
                print(f"\n{detail['market']}/{detail['skill']}")
                print(f"文件: {detail['file']}")
                print(f"命令: {detail['command'][:100]}...")
                print(f"错误: {detail['error'][:200]}")
    
    return results['failed'] == 0

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
