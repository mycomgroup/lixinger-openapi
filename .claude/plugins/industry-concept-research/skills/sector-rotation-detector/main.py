import argparse
import logging
from datetime import date
import pandas as pd
from data_provider import DataProvider
from analyzer import RotationAnalyzer
from visualizer import RotationVisualizer
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Sector Rotation Analyzer")
    parser.add_argument("--lookback", type=int, default=30, help="Number of trading days to look back")
    parser.add_argument("--return-days", type=int, default=5, help="Days to calculate return")
    parser.add_argument("--back-days", type=int, default=30, help="Days backend delta for calculation")
    parser.add_argument("--top-n", type=int, default=10, help="Number of top industries to track")
    parser.add_argument("--workers", type=int, default=10, help="Max workers for concurrent API fetches")
    parser.add_argument("--db-path", type=str, default="data/rotation_data.db", help="Path to sqlite DB cache")
    args = parser.parse_args()

    print("=" * 100)
    print(f"板块轮动 {args.lookback} 交易日统计分析 | 优化入库版")
    print("=" * 100)

    # Resolve paths relative to the script directory
    base_dir = Path(__file__).parent
    db_full_path = base_dir / args.db_path
    output_dir = base_dir / "output"

    # Initialize components
    provider = DataProvider(db_path=str(db_full_path))
    analyzer = RotationAnalyzer(provider, top_n=args.top_n, return_days=args.return_days, back_days=args.back_days)
    visualizer = RotationVisualizer(output_dir=str(output_dir))

    # Get trade days
    trade_days = provider.get_trade_days(date.today(), args.lookback)
    formatted_days = [d.strftime("%Y-%m-%d") for d in trade_days]
    logger.info(f"Analysis period: {formatted_days[0]} ~ {formatted_days[-1]} ({len(formatted_days)} days)")

    # Get industry mapping
    industry_mapping = provider.get_industry_mapping(top_components=50)
    if not industry_mapping:
        logger.error("Failed to build industry mapping. Exiting.")
        return

    # Fetch data concurrently for the required window
    all_codes = list(industry_mapping.keys())
    start_fetch = pd.to_datetime(trade_days[0]) - pd.Timedelta(days=args.back_days + 20)
    end_fetch = pd.to_datetime(trade_days[-1])
    provider.fetch_and_cache_daily_data(all_codes, start_fetch.date(), end_fetch.date(), max_workers=args.workers)

    # Process each trading day
    records = []
    
    # Flatten mapping to dataframe for passing
    df_ind = pd.DataFrame([
        {"code": code, "name": info["name"], "em_industry": info["em_industry"]} 
        for code, info in industry_mapping.items()
    ])

    for i, day in enumerate(formatted_days):
        logger.info(f"Processing day {i+1}/{len(formatted_days)}: {day}")
        df_return = analyzer.calc_returns_for_date(day, df_ind)
        if df_return.empty:
            logger.warning(f"No return data available for {day}")
            continue
            
        daily_top = analyzer.build_daily_top(df_return, day)
        if not daily_top.empty:
            records.append(daily_top)
            
    if not records:
        logger.error("No valid ranking records generated.")
        return
        
    all_top = pd.concat(records, ignore_index=True)
    logger.info(f"Total industry ranking records processed: {len(all_top)}")
    
    # Generate report metrics
    title = "em_industry"
    category_name = "东方财富行业"
    
    metrics = analyzer.calc_transition_metrics(all_top, formatted_days)
    summary, score_pivot = analyzer.build_summary(all_top, formatted_days)
    
    # Plot results
    visualizer.plot_category(score_pivot, summary, category_name, args.lookback, formatted_days[-1])

    # CLI Output exactly matching original format
    latest_day = formatted_days[-1]
    prev_day = formatted_days[-2] if len(formatted_days) > 1 else formatted_days[-1]
    latest_set = set(all_top.loc[all_top["date"] == latest_day, "industry"])
    prev_set = set(all_top.loc[all_top["date"] == prev_day, "industry"])
    new_today = sorted(latest_set - prev_set)

    print("\n" + "=" * 100)
    print(f"{category_name} - 近{args.lookback}个交易日轮动统计")
    print("=" * 100)
    print(f"平均连续重叠行业数: {metrics['avg_overlap']:.2f} / {args.top_n}")
    print(f"平均每日新切换行业数: {metrics['avg_churn']:.2f} / {args.top_n}")
    print(f"Top1 龙头切换率: {metrics['top1_switch_rate']:.2%}")
    print(f"新上榜行业次日留榜率: {metrics['new_entry_retention_rate']:.2%}")
    print(f"连续2天在榜行业第3天留榜率: {metrics['two_day_persistent_retention_rate']:.2%}")
    print(f"高分行业(>=15分)次日降温率: {metrics['high_score_cooldown_rate']:.2%}")
    print("今天新进入 Top10:", "、".join(new_today) if new_today else "无")

    display_cols = ["appear_days", "avg_rank", "avg_score", "max_score", "latest_score", "latest_rank", "trend_3d", "in_latest_top10"]
    print(f"\n{category_name}统计摘要（Top 12）:")
    print(summary[display_cols].head(12).round(2))

    recent_days = formatted_days[-5:] if len(formatted_days) >= 5 else formatted_days
    top_industries = summary.head(10).index
    recent_matrix = score_pivot.loc[recent_days, top_industries].T.fillna(0)
    recent_matrix.columns = [str(col)[:10] for col in recent_matrix.columns]
    print("\n最近5个交易日得分矩阵（Top10 常驻行业）:")
    print(recent_matrix.round(2))
    
    # Focus Conclusion
    em_latest = summary[summary["in_latest_top10"]].head(8)
    focus_list = em_latest[(em_latest["appear_days"] >= 6) | (em_latest["trend_3d"] > 0)].head(5)
    
    print("\n" + "=" * 100)
    print(f"{args.lookback} 交易日核心结论")
    print("=" * 100)
    print(f"1. 东方财富行业板块平均每日有 {metrics['avg_churn']:.2f} 个席位发生切换，说明轮动很明显，但不是完全随机。")
    print(f"2. 新上榜行业次日留榜率为 {metrics['new_entry_retention_rate']:.2%}，连续2天在榜行业第3天留榜率为 {metrics['two_day_persistent_retention_rate']:.2%}。")
    print(f"3. 高分行业(>=15分)次日降温率为 {metrics['high_score_cooldown_rate']:.2%}，高分后追涨需要防回落。")
    print("4. 今天更值得看的方向:")
    if focus_list.empty:
        print('   • 暂无明显同时满足"常驻"或"近3日升温"的行业。')
    else:
        for idx, row in focus_list.iterrows():
            print(f"   • {idx}: 上榜 {int(row.appear_days)} 天, 最新得分 {row.latest_score:.0f}, 近3日趋势 {row.trend_3d:+.2f}")
    
    print("\n任务完成。")

if __name__ == "__main__":
    main()
