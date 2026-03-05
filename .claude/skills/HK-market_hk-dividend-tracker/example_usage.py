#!/usr/bin/env python3
"""
Example: Using HK Market Data Toolkit

This example shows how HK market skills can fetch data using lixinger_wrapper.
"""

import sys
import os
# Add the toolkit scripts directory to path
toolkit_path = os.path.join(os.path.dirname(__file__), '..', 'findata-toolkit-hk', 'scripts')
sys.path.insert(0, os.path.abspath(toolkit_path))

from lixinger_wrapper import get_stock_price, init_lixinger

if __name__ == "__main__":
    # Initialize the API
    if not init_lixinger():
        print("Failed to initialize Lixinger API. Check token configuration.")
        sys.exit(1)
    
    # Example: Fetch recent price data for HSBC (00005)
    print("Fetching HSBC Holdings (00005) price data...")
    df = get_stock_price("00005", start_date="2024-01-01", limit=10)
    
    if df is not None:
        print(f"\nSuccessfully fetched {len(df)} rows of data:")
        print(df[['date', 'open', 'close', 'high', 'low', 'volume']])
        
        # Calculate some basic metrics
        latest = df.iloc[0]
        print(f"\nLatest close price: HKD {latest['close']}")
        print(f"Turnover rate: {latest['to_r']:.4%}")
    else:
        print("Failed to fetch data.")
