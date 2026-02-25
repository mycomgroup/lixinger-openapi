#!/usr/bin/env python3
"""
Optimized regression test runner that executes each test case in an isolated directory
"""
import os
import json
import shutil
import subprocess
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).parent.resolve()
TEST_CASES_DIR = BASE_DIR / "cases"
RESULTS_DIR = BASE_DIR / "result"
SKILLS_MAP = {
    "lixinger-data-query": "lixinger-data-query",
    "macro-liquidity-monitor": "macro-liquidity-monitor",
    "us-macro-liquidity-monitor": "us-macro-liquidity-monitor",
    "ipo-lockup-risk-monitor": "ipo-lockup-risk-monitor",
    "shareholder-risk-check": "shareholder-risk-check",
    "peer-comparison-analyzer": "peer-comparison-analyzer",
    "us-peer-comparison-analyzer": "us-peer-comparison-analyzer",
    "dividend-corporate-action-tracker": "dividend-corporate-action-tracker",
    "weekly-market-brief-generator": "weekly-market-brief-generator",
    "us-weekly-market-brief-generator": "us-weekly-market-brief-generator",
    "volatility-regime-monitor": "volatility-regime-monitor",
    "us-volatility-regime-monitor": "us-volatility-regime-monitor",
    "margin-risk-monitor": "margin-risk-monitor",
    "goodwill-risk-monitor": "goodwill-risk-monitor",
    "suitability-report-generator": "suitability-report-generator",
    "us-suitability-report-generator": "us-suitability-report-generator",
    "quant-factor-screener": "quant-factor-screener",
    "us-quant-factor-screener": "us-quant-factor-screener",
    "concept-board-analyzer": "concept-board-analyzer",
    "st-delist-risk-scanner": "st-delist-risk-scanner",
    "rebalancing-planner": "rebalancing-planner",
    "us-rebalancing-planner": "us-rebalancing-planner",
    "block-deal-monitor": "block-deal-monitor",
    "esg-screener": "esg-screener",
    "us-esg-screener": "us-esg-screener",
    "high-dividend-strategy": "high-dividend-strategy",
    "industry-chain-mapper": "industry-chain-mapper",
    "undervalued-stock-screener": "undervalued-stock-screener",
    "us-undervalued-stock-screener": "us-undervalued-stock-screener",
    "dragon-tiger-list-analyzer": "dragon-tiger-list-analyzer",
    "investment-memo-generator": "investment-memo-generator",
    "us-investment-memo-generator": "us-investment-memo-generator",
    "bse-selection-analyzer": "bse-selection-analyzer",
    "tech-hype-vs-fundamentals": "tech-hype-vs-fundamentals",
    "us-tech-hype-vs-fundamentals": "us-tech-hype-vs-fundamentals",
    "equity-research-orchestrator": "equity-research-orchestrator",
    "us-equity-research-orchestrator": "us-equity-research-orchestrator",
    "risk-adjusted-return-optimizer": "risk-adjusted-return-optimizer",
    "us-risk-adjusted-return-optimizer": "us-risk-adjusted-return-optimizer",
    "event-study": "event-study",
    "us-event-study": "us-event-study",
    "fund-flow-monitor": "fund-flow-monitor",
    "etf-allocator": "etf-allocator",
    "us-etf-allocator": "us-etf-allocator",
    "small-cap-growth-identifier": "small-cap-growth-identifier",
    "us-small-cap-growth-identifier": "us-small-cap-growth-identifier",
    "financial-statement-analyzer": "financial-statement-analyzer",
    "us-financial-statement-analyzer": "us-financial-statement-analyzer",
    "factor-crowding-monitor": "factor-crowding-monitor",
    "us-factor-crowding-monitor": "us-factor-crowding-monitor",
    "portfolio-health-check": "portfolio-health-check",
    "us-portfolio-health-check": "us-portfolio-health-check",
    "portfolio-monitor-orchestrator": "portfolio-monitor-orchestrator",
    "us-portfolio-monitor-orchestrator": "us-portfolio-monitor-orchestrator",
    "market-breadth-monitor": "market-breadth-monitor",
    "us-market-breadth-monitor": "us-market-breadth-monitor",
    "event-driven-detector": "event-driven-detector",
    "us-event-driven-detector": "us-event-driven-detector",
    "sector-rotation-detector": "sector-rotation-detector",
    "us-sector-rotation-detector": "us-sector-rotation-detector",
    "valuation-regime-detector": "valuation-regime-detector",
    "us-valuation-regime-detector": "us-valuation-regime-detector",
    "hot-rank-sentiment-monitor": "hot-rank-sentiment-monitor",
    "market-overview-dashboard": "market-overview-dashboard",
    "limit-up-pool-analyzer": "limit-up-pool-analyzer",
    "insider-trading-analyzer": "insider-trading-analyzer",
    "us-insider-trading-analyzer": "us-insider-trading-analyzer",
    "shareholder-structure-monitor": "shareholder-structure-monitor",
    "policy-sensitivity-brief": "policy-sensitivity-brief",
    "us-policy-sensitivity-brief": "us-policy-sensitivity-brief",
    "sentiment-reality-gap": "sentiment-reality-gap",
    "liquidity-impact-estimator": "liquidity-impact-estimator",
    "us-liquidity-impact-estimator": "us-liquidity-impact-estimator",
    "limit-up-limit-down-risk-checker": "limit-up-limit-down-risk-checker",
    "us-sentiment-reality-gap": "us-sentiment-reality-gap"
}

def run_test_case(case_file: Path):
    """Run a single test case in isolated directory"""
    case_name = case_file.stem
    case_dir = RESULTS_DIR / case_name
    case_dir.mkdir(parents=True, exist_ok=True)

    print(f"🚀 Running test case: {case_name}")

    # Copy test case to isolated directory
    shutil.copy(case_file, case_dir / "input.json")

    # Determine skill from filename using flexible matching
    skill_name = None
    normalized_case = case_name.lower().replace('_', '-').replace(' ', '-')

    # Generate possible base names by removing common suffixes
    possible_names = [
        normalized_case,
        normalized_case.replace('-case-', '-').replace('-query-', '-').replace('-results', ''),
        normalized_case.split('-case-')[0],
        normalized_case.split('-query-')[0],
        normalized_case.split('_case_')[0],
        normalized_case.split('_query_')[0],
        # Special handling for disclosure-notice-monitor and similar patterns
        normalized_case.split('-monitor_')[0],
        normalized_case.split('-generator_')[0],
        normalized_case.split('-analyzer_')[0],
        normalized_case.split('-scanner_')[0]
    ]

    # Remove duplicates and empty strings
    possible_names = list(dict.fromkeys([n for n in possible_names if n]))

    # Check all possible names against SKILLS_MAP
    for name in possible_names:
        if name in SKILLS_MAP:
            skill_name = SKILLS_MAP[name]
            break

    # If still not found, try prefix match
    if skill_name is None:
        for prefix, command in SKILLS_MAP.items():
            if normalized_case.startswith(prefix):
                skill_name = command
                break

    if not skill_name:
        print(f"⚠️  Could not determine skill for {case_name}")
        return

    # Execute skill
    try:
        # Execute skill while unsetting CLAUDECODE env variable
        env = os.environ.copy()
        env.pop('CLAUDECODE', None)

        try:
            # Use stdin to pass input JSON instead of --input flag
            with open(case_dir / "input.json", 'r') as f:
                input_data = f.read()

            result = subprocess.run(
                ["claude", "skill", "run", skill_name],
                input=input_data,
                env=env,
                capture_output=True,
                text=True,
                check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed: {case_name}")
            print(f"Error: {e.stderr}")
            with open(case_dir / "error.log", "w") as f:
                f.write(e.stderr)
            return False

        # Save results
        with open(case_dir / "output.json", "w") as f:
            f.write(result.stdout)

        print(f"✅ Success: {case_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {case_name}")
        print(f"Error: {e.stderr}")
        with open(case_dir / "error.log", "w") as f:
            f.write(e.stderr)
        return False

def main():
    """Main execution loop"""
    RESULTS_DIR.mkdir(exist_ok=True)

    # Get all test cases
    test_cases = list(TEST_CASES_DIR.glob("*.json"))
    print(f"Found {len(test_cases)} test cases")

    # Execute all test cases
    results = {}
    for case_file in test_cases:
        success = run_test_case(case_file)
        results[case_file.stem] = "success" if success else "failed"

    # Save summary
    with open(RESULTS_DIR / "summary.json", "w") as f:
        json.dump({
            "total_cases": len(test_cases),
            "success": sum(1 for r in results.values() if r == "success"),
            "failed": sum(1 for r in results.values() if r == "failed"),
            "details": results
        }, f, indent=2)

    print(f"\n🔥 Test execution complete!")
    print(f"✅ Success: {sum(1 for r in results.values() if r == 'success')}")
    print(f"❌ Failed: {sum(1 for r in results.values() if r == 'failed')}")
    print(f"📊 Summary saved to: {RESULTS_DIR / 'summary.json'}")

if __name__ == "__main__":
    main()
