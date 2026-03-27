import matplotlib.pyplot as plt
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class RotationVisualizer:
    def __init__(self, output_dir="./output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        # Setup Chinese fonts
        plt.rcParams["font.sans-serif"] = ["SimHei", "Arial Unicode MS", "DejaVu Sans", "sans-serif"]
        plt.rcParams["axes.unicode_minus"] = False

    def plot_category(self, score_pivot, summary, title, lookback_days, trade_day):
        """Plot the core sector hotness scores and Top10 frequencies."""
        leaders = summary.head(8).index.tolist()
        if not leaders:
            logger.warning(f"No leaders found for {title} category, skipping plot.")
            return

        fig, axes = plt.subplots(1, 2, figsize=(18, 6))

        score_pivot[leaders].plot(ax=axes[0], marker="o")
        axes[0].set_title(f"{title} 近 {lookback_days} 个交易日核心热点得分")
        axes[0].set_xlabel("交易日")
        axes[0].set_ylabel("得分")
        axes[0].tick_params(axis="x", rotation=45)
        axes[0].grid(alpha=0.25)
        axes[0].legend(loc="best", fontsize=8)

        summary.head(10).sort_values("appear_days").plot(
            kind="barh", y="appear_days", ax=axes[1], legend=False, color="#4472C4"
        )
        axes[1].set_title(f"{title} 近 {lookback_days} 日上榜天数 Top10")
        axes[1].set_xlabel("进入 Top10 的天数")
        axes[1].set_ylabel("行业")
        axes[1].grid(axis="x", alpha=0.25)

        plt.tight_layout()
        
        filename = f"rotation_{title}_{trade_day}.png"
        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=150, bbox_inches="tight")
        plt.close(fig)
        logger.info(f"Saved visualization plot to {filepath}")
