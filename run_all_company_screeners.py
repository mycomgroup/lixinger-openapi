#!/usr/bin/env python3
"""
批量运行所有 company-fundamental 类型的 screener
跳过已经跑过的，结果保存到指定目录
"""

import json
import os
import subprocess
import re
import time
from datetime import datetime
from glob import glob


def extract_all_company_fundamental_urls(file_path):
    """提取所有 company-fundamental 类型的 screener URL"""
    urls = []
    seen = set()

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                url = data.get("url", "")
                # 只保留 company-fundamental 类型
                if "company-fundamental/" in url and "screener-id=" in url:
                    match = re.search(r"screener-id=([a-zA-Z0-9]+)", url)
                    if match:
                        sid = match.group(1)
                        if sid not in seen:
                            seen.add(sid)
                            # 提取区域代码
                            area = "cn"
                            if "/hk" in url:
                                area = "hk"
                            elif "/us" in url:
                                area = "us"
                            urls.append({"url": url, "screener_id": sid, "area": area})
            except json.JSONDecodeError:
                continue

    return urls


def get_existing_screener_ids(output_dir):
    """获取已经运行过的 screener ID"""
    existing = set()
    pattern = os.path.join(output_dir, "screener_*_*.json")
    for filepath in glob(pattern):
        filename = os.path.basename(filepath)
        # 从文件名提取 screener_id
        # 格式: screener_{area}_{screener_id}.json
        match = re.search(r"screener_[a-z]+_([a-f0-9]+)\.json$", filename)
        if match:
            existing.add(match.group(1))
    return existing


def run_screener(url_info, output_dir, skill_dir, max_retries=3):
    """运行单个 screener 并保存结果，带重试机制"""
    screener_id = url_info["screener_id"]
    url = url_info["url"]
    area = url_info["area"]

    # 构建命令
    cmd = [
        "node",
        "request/fetch-lixinger-screener.js",
        "--url",
        url,
        "--output",
        "table-json",
    ]

    # 输出文件名
    safe_id = screener_id[:20]
    json_file = os.path.join(output_dir, f"screener_{area}_{safe_id}.json")
    md_file = os.path.join(output_dir, f"screener_{area}_{safe_id}.md")

    # 重试逻辑
    for attempt in range(max_retries):
        try:
            # 执行命令获取 JSON 结果
            result = subprocess.run(
                cmd, cwd=skill_dir, capture_output=True, text=True, timeout=60
            )

            # 检查是否是限流错误 (429)
            if result.returncode != 0 and "429" in result.stderr:
                if attempt < max_retries - 1:
                    wait_time = 2**attempt  # 指数退避: 1, 2, 4 秒
                    print(f"    ⚠️ 限流(429)，等待 {wait_time}s 后重试...")
                    time.sleep(wait_time)
                    continue

            if result.returncode == 0:
                # 保存 JSON 结果
                with open(json_file, "w", encoding="utf-8") as f:
                    f.write(result.stdout)

                # 同时获取 markdown 格式便于阅读
                cmd_md = [
                    "node",
                    "request/fetch-lixinger-screener.js",
                    "--url",
                    url,
                    "--output",
                    "markdown",
                ]
                result_md = subprocess.run(
                    cmd_md, cwd=skill_dir, capture_output=True, text=True, timeout=60
                )
                if result_md.returncode == 0:
                    with open(md_file, "w", encoding="utf-8") as f:
                        f.write(result_md.stdout)

                # 解析结果获取统计信息
                try:
                    data = json.loads(result.stdout)
                    return {
                        "success": True,
                        "screener_id": screener_id,
                        "area": area,
                        "url": url,
                        "total": data.get("total", 0),
                        "screener_name": data.get("screenerName", "Unknown"),
                        "screener_description": data.get("screenerDescription"),
                        "json_file": os.path.basename(json_file),
                        "md_file": os.path.basename(md_file),
                    }
                except:
                    return {
                        "success": True,
                        "screener_id": screener_id,
                        "area": area,
                        "url": url,
                        "json_file": os.path.basename(json_file),
                        "md_file": os.path.basename(md_file),
                    }
            else:
                # 保存错误信息
                error_file = os.path.join(
                    output_dir, f"screener_{area}_{safe_id}_error.txt"
                )
                with open(error_file, "w", encoding="utf-8") as f:
                    f.write(f"URL: {url}\n")
                    f.write(f"Error: {result.stderr}\n")

                return {
                    "success": False,
                    "screener_id": screener_id,
                    "area": area,
                    "url": url,
                    "error": result.stderr[:200],
                    "error_file": os.path.basename(error_file),
                }

        except subprocess.TimeoutExpired:
            error_file = os.path.join(
                output_dir, f"screener_{area}_{safe_id}_error.txt"
            )
            with open(error_file, "w", encoding="utf-8") as f:
                f.write(f"URL: {url}\n")
                f.write(f"Error: Timeout\n")

            return {
                "success": False,
                "screener_id": screener_id,
                "area": area,
                "url": url,
                "error": "Timeout",
                "error_file": os.path.basename(error_file),
            }
        except Exception as e:
            error_file = os.path.join(
                output_dir, f"screener_{area}_{safe_id}_error.txt"
            )
            with open(error_file, "w", encoding="utf-8") as f:
                f.write(f"URL: {url}\n")
                f.write(f"Error: {str(e)}\n")

            return {
                "success": False,
                "screener_id": screener_id,
                "area": area,
                "url": url,
                "error": str(e)[:200],
                "error_file": os.path.basename(error_file),
            }

    # 所有重试都失败
    return {
        "success": False,
        "screener_id": screener_id,
        "area": area,
        "url": url,
        "error": f"Failed after {max_retries} attempts",
    }


def main():
    # 配置
    links_file = "/Users/fengzhi/Downloads/git/lixinger-openapi/links.txt"
    skill_dir = (
        "/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/lixinger-screener"
    )
    output_dir = "/Users/fengzhi/Downloads/git/lixinger-openapi/url_results"

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    print(f"输出目录: {output_dir}")

    # 获取已存在的 screener
    existing_ids = get_existing_screener_ids(output_dir)
    print(f"已存在的 screener: {len(existing_ids)} 个")

    # 提取所有 URL
    print(f"\n正在从 {links_file} 提取所有 company-fundamental 筛选器...")
    all_urls = extract_all_company_fundamental_urls(links_file)
    print(f"总共找到: {len(all_urls)} 个筛选器")

    # 过滤掉已存在的
    urls_to_run = [u for u in all_urls if u["screener_id"][:20] not in existing_ids]
    skipped = len(all_urls) - len(urls_to_run)
    print(f"跳过已存在的: {skipped} 个")
    print(f"需要运行的: {len(urls_to_run)} 个\n")

    if len(urls_to_run) == 0:
        print("所有筛选器都已运行过，无需处理。")
        return

    # 统计
    cn_count = sum(1 for u in urls_to_run if u["area"] == "cn")
    hk_count = sum(1 for u in urls_to_run if u["area"] == "hk")
    print(f"  - A股 (cn): {cn_count}")
    print(f"  - 港股 (hk): {hk_count}")
    print()

    # 批量运行 - 带限流控制
    success_count = 0
    fail_count = 0
    results_summary = []
    consecutive_429_errors = 0  # 连续 429 错误计数
    base_delay = 3.0  # 基础延迟 3 秒

    print(f"开始处理，基础延迟: {base_delay}s，检测到连续限流会自动增加延迟\n")

    for i, url_info in enumerate(urls_to_run, 1):
        print(
            f"[{i}/{len(urls_to_run)}] 正在处理: {url_info['screener_id'][:20]}... [{url_info['area']}]"
        )

        result = run_screener(url_info, output_dir, skill_dir)

        if result["success"]:
            success_count += 1
            total = result.get("total", "N/A")
            name = result.get("screener_name", "Unknown")
            print(f"  ✓ 成功 | 结果数: {total:4d} | {name[:35] if name else 'N/A'}...")
            # 成功后重置限流计数
            if consecutive_429_errors > 0:
                consecutive_429_errors = 0
                if base_delay > 0.3:
                    base_delay = max(0.3, base_delay * 0.8)
                    print(f"    ↓ 恢复延迟至 {base_delay:.2f}s")
        else:
            fail_count += 1
            error_msg = result.get("error", "Unknown")[:80]
            print(f"  ✗ 失败: {error_msg}")
            # 检测限流错误
            if "429" in error_msg:
                consecutive_429_errors += 1
                # 如果连续 3 次 429，增加延迟
                if consecutive_429_errors >= 3:
                    base_delay = min(2.0, base_delay * 1.5)  # 最多增加到 2 秒
                    print(
                        f"    ⚠️ 连续 {consecutive_429_errors} 次限流，增加延迟至 {base_delay:.2f}s"
                    )

        results_summary.append(result)

        # 每个请求后 sleep，避免过快
        if i < len(urls_to_run):  # 最后一个不需要 sleep
            time.sleep(base_delay)

    # 保存本次运行的汇总结果
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_file = os.path.join(output_dir, f"_summary_batch_{timestamp}.json")
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(
            {
                "timestamp": datetime.now().isoformat(),
                "batch_info": {
                    "total_in_links": len(all_urls),
                    "existing": len(existing_ids),
                    "skipped": skipped,
                    "processed": len(urls_to_run),
                    "success": success_count,
                    "failed": fail_count,
                },
                "results": results_summary,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    # 同时保存一个易读的 markdown 汇总
    summary_md = os.path.join(output_dir, f"_summary_batch_{timestamp}.md")
    with open(summary_md, "w", encoding="utf-8") as f:
        f.write(f"# Company Fundamental Screener 批量获取结果\n\n")
        f.write(f"批次时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"## 批次统计\n\n")
        f.write(f"- 总共筛选器: {len(all_urls)}\n")
        f.write(f"- 已存在(跳过): {skipped}\n")
        f.write(f"- 本次处理: {len(urls_to_run)}\n")
        f.write(f"- 成功: {success_count}\n")
        f.write(f"- 失败: {fail_count}\n\n")

        f.write("## 详细结果\n\n")
        f.write("| # | 区域 | Screener ID | 名称 | 结果数 | 文件 |\n")
        f.write("|---|------|-------------|------|--------|------|\n")
        for i, r in enumerate(results_summary, 1):
            name = (
                r.get("screener_name", "N/A")[:25] if r.get("screener_name") else "N/A"
            )
            total = r.get("total", "N/A")
            area = r.get("area", "cn")
            file_link = r.get("json_file", r.get("error_file", "N/A"))
            f.write(
                f"| {i} | {area} | {r['screener_id'][:16]}... | {name} | {total} | {file_link} |\n"
            )

        # 添加统计信息
        successful_with_data = [
            r for r in results_summary if r.get("success") and r.get("total", 0) > 0
        ]
        successful_empty = [
            r for r in results_summary if r.get("success") and r.get("total", 0) == 0
        ]
        f.write(f"\n## 结果统计\n\n")
        f.write(f"- 有结果的筛选器 (>0): {len(successful_with_data)}\n")
        f.write(f"- 结果数为0的筛选器: {len(successful_empty)}\n")
        total_stocks = sum(
            r.get("total", 0) for r in results_summary if r.get("success")
        )
        f.write(f"- 本批次总股票数: {total_stocks}\n")

    # 打印汇总
    print(f"\n{'=' * 60}")
    print(f"批次完成!")
    print(f"本次处理: {len(urls_to_run)} 个")
    print(f"成功: {success_count}")
    print(f"失败: {fail_count}")
    successful_with_data = [
        r for r in results_summary if r.get("success") and r.get("total", 0) > 0
    ]
    print(f"有结果的筛选器: {len(successful_with_data)}")
    total_stocks = sum(r.get("total", 0) for r in results_summary if r.get("success"))
    print(f"本批次总股票数: {total_stocks}")
    print(f"结果保存在: {output_dir}")
    print(f"汇总文件: {summary_md}")


if __name__ == "__main__":
    main()
