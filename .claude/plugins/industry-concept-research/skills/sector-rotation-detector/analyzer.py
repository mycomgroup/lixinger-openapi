import pandas as pd
import numpy as np
import logging
from datetime import timedelta

logger = logging.getLogger(__name__)

class RotationAnalyzer:
    def __init__(self, data_provider, top_n=10, stock_top_count=5, up_limit=30, return_days=5, back_days=30):
        self.provider = data_provider
        self.top_n = top_n
        self.stock_top_count = stock_top_count
        self.up_limit = up_limit
        self.return_days = return_days
        self.back_days = back_days
        
    def _group_top_list(self, group):
        """Get the top stock names in an industry group based on return."""
        if group.empty:
            return ""
        filtered = group[group["up_limit_count"] < self.up_limit]
        if filtered.empty:
            filtered = group
            
        top = filtered.nlargest(self.stock_top_count, "return")
        names = top["name"].tolist()
        return "、".join([str(n) for n in names if pd.notna(n)])

    def _group_score_series(self, group):
        """Calculate the average score of an industry group."""
        if group.empty:
            return 0
        filtered = group[group["up_limit_count"] < self.up_limit]
        if filtered.empty:
            filtered = group
        score = filtered["return"].mean()
        return float(score) if not pd.isna(score) else 0.0

    def calc_returns_for_date(self, trade_day, df_industry):
        """Calculate returns for individual stock returns ending on trade_day"""
        end_date = pd.to_datetime(trade_day)
        start_date = end_date - timedelta(days=self.back_days + 10)
        
        stock_codes = df_industry["code"].tolist()
        df_hist = self.provider.get_stock_history_bulk(stock_codes, start_date, end_date)
        
        if df_hist.empty:
            return pd.DataFrame()
            
        results = []
        for code, group in df_hist.groupby("code"):
            if len(group) >= self.return_days + 1:
                group = group.sort_values("date")
                current_price = group["close"].iloc[-1]
                past_price = group["close"].iloc[-(self.return_days + 1)]
                ret = (current_price / past_price - 1) * 100
                up_limit_count = group["is_limit_up"].sum()
                
                results.append({
                    "code": code,
                    "return": ret,
                    "up_limit_count": up_limit_count
                })
                
        if not results:
            return pd.DataFrame()
            
        df_ret = pd.DataFrame(results)
        # Merge with industry info
        df_merged = pd.merge(df_ret, df_industry, on="code", how="inner")
        return df_merged

    def build_daily_top(self, df_return, trade_day):
        """Build daily top industry rankings"""
        if df_return.empty or "em_industry" not in df_return.columns:
            return pd.DataFrame()

        s_tops = df_return.groupby("em_industry").apply(self._group_top_list)
        s_scores = df_return.groupby("em_industry").apply(self._group_score_series)

        df = pd.DataFrame({
            "scores": s_scores,
            "top": s_tops,
            "score": s_scores,
        }, index=s_tops.index).sort_values(by="score", ascending=False).head(self.top_n).reset_index()

        df = df.rename(columns={"em_industry": "industry"})
        df["date"] = trade_day
        df["rank"] = np.arange(1, len(df) + 1)

        return df[["date", "industry", "rank", "score", "top", "scores"]]

    def calc_transition_metrics(self, cat_df, trade_days):
        """Calculate sector transition metrics over the trade days."""
        day_sets = {
            day: set(cat_df.loc[cat_df["date"] == day, "industry"])
            for day in trade_days
        }

        top1_switches = 0
        overlap_counts = []
        churn_counts = []
        new_entries = 0
        new_entries_retained = 0
        two_day_persistent = 0
        two_day_persistent_retained = 0
        high_score_total = 0
        high_score_cooldown = 0
        
        day_top1 = {}
        for day in trade_days:
            daily = cat_df[cat_df["date"] == day].sort_values("rank")
            day_top1[day] = daily.iloc[0]["industry"] if not daily.empty else None

        score_lookup = cat_df.set_index(["date", "industry"])["score"].to_dict()

        for index in range(1, len(trade_days)):
            prev_day = trade_days[index - 1]
            cur_day = trade_days[index]
            prev_set = day_sets.get(prev_day, set())
            cur_set = day_sets.get(cur_day, set())
            overlap = len(prev_set & cur_set)
            overlap_counts.append(overlap)
            churn_counts.append(self.top_n - overlap)
            
            if day_top1.get(prev_day) != day_top1.get(cur_day):
                top1_switches += 1

        for index in range(1, len(trade_days) - 1):
            prev_day = trade_days[index - 1]
            cur_day = trade_days[index]
            next_day = trade_days[index + 1]
            prev_set = day_sets.get(prev_day, set())
            cur_set = day_sets.get(cur_day, set())
            next_set = day_sets.get(next_day, set())

            new_set = cur_set - prev_set
            new_entries += len(new_set)
            new_entries_retained += len(new_set & next_set)

            persistent_set = prev_set & cur_set
            two_day_persistent += len(persistent_set)
            two_day_persistent_retained += len(persistent_set & next_set)

        for index in range(len(trade_days) - 1):
            cur_day = trade_days[index]
            next_day = trade_days[index + 1]
            
            today_scores = cat_df[(cat_df["date"] == cur_day) & (cat_df["score"] >= 15)]
            for _, row in today_scores.iterrows():
                high_score_total += 1
                next_score = score_lookup.get((next_day, row["industry"]), 0)
                if next_score < row["score"]:
                    high_score_cooldown += 1

        transition_count = max(len(trade_days) - 1, 1)
        return {
            "avg_overlap": float(np.mean(overlap_counts)) if overlap_counts else 0.0,
            "avg_churn": float(np.mean(churn_counts)) if churn_counts else 0.0,
            "top1_switch_rate": top1_switches / transition_count,
            "new_entry_retention_rate": (new_entries_retained / new_entries) if new_entries else 0.0,
            "two_day_persistent_retention_rate": (two_day_persistent_retained / two_day_persistent) if two_day_persistent else 0.0,
            "high_score_cooldown_rate": (high_score_cooldown / high_score_total) if high_score_total else 0.0,
        }

    def build_summary(self, cat_df, trade_days):
        """Create summary statistics of industries"""
        score_pivot = cat_df.pivot(index="date", columns="industry", values="score").fillna(0)
        rank_pivot = cat_df.pivot(index="date", columns="industry", values="rank")

        latest_day = trade_days[-1]
        recent_days = trade_days[-3:] if len(trade_days) >= 3 else trade_days
        previous_days = trade_days[-6:-3] if len(trade_days) >= 6 else trade_days[:max(1, len(trade_days) // 2)]

        summary = pd.DataFrame({
            "appear_days": cat_df.groupby("industry")["date"].nunique(),
            "avg_rank": cat_df.groupby("industry")["rank"].mean(),
            "avg_score": cat_df.groupby("industry")["score"].mean(),
            "max_score": cat_df.groupby("industry")["score"].max()
        }).fillna(0)

        summary["latest_score"] = score_pivot.loc[latest_day] if latest_day in score_pivot.index else 0
        summary["latest_rank"] = rank_pivot.loc[latest_day] if latest_day in rank_pivot.index else np.nan
        summary["recent3_avg"] = score_pivot.loc[recent_days].mean() if len(recent_days) > 0 else 0
        summary["prev3_avg"] = score_pivot.loc[previous_days].mean() if len(previous_days) > 0 else 0
        summary["trend_3d"] = summary["recent3_avg"] - summary["prev3_avg"]
        summary["in_latest_top10"] = summary["latest_score"] > 0

        summary = summary.sort_values(
            by=["appear_days", "latest_score", "avg_score", "avg_rank"],
            ascending=[False, False, False, True]
        )
        return summary, score_pivot
