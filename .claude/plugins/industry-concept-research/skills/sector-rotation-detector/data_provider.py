import akshare as ak
import pandas as pd
import sqlite3
import time
from datetime import datetime, timedelta
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from collections import defaultdict

logger = logging.getLogger(__name__)

class DataProvider:
    def __init__(self, db_path="rotation_data.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._init_db()

    def _init_db(self):
        """Initialize the SQLite tables"""
        cursor = self.conn.cursor()
        # Daily market data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_market_data (
                date TEXT,
                code TEXT,
                close REAL,
                pchg REAL,
                is_limit_up INTEGER,
                PRIMARY KEY (date, code)
            )
        ''')
        # Industry mapping table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS industry_mapping (
                code TEXT PRIMARY KEY,
                name TEXT,
                em_industry TEXT
            )
        ''')
        self.conn.commit()

    def get_trade_days(self, end_date, count):
        """Get past trading days ending at end_date"""
        start_date = end_date - timedelta(days=count * 2 + 20)
        try:
            df = ak.index_zh_a_hist(
                symbol="000001",
                period="daily",
                start_date=start_date.strftime("%Y%m%d"),
                end_date=end_date.strftime("%Y%m%d")
            )
            dates = df["日期"].values[-count:]
            return [pd.to_datetime(d).date() for d in dates]
        except Exception as e:
            logger.warning(f"Failed to fetch trading days: {e}, using weekday approximation")
            dates = []
            current = end_date
            while len(dates) < count:
                if current.weekday() < 5:
                    dates.insert(0, current)
                current -= timedelta(days=1)
            return dates[:count]

    def _fetch_stock_hist(self, code, start_date, end_date):
        """Fetch stock history from API"""
        try:
            df = ak.stock_zh_a_hist(
                symbol=code,
                period="daily",
                start_date=start_date.strftime("%Y%m%d"),
                end_date=end_date.strftime("%Y%m%d")
            )
            if df is not None and not df.empty:
                df = df.rename(columns={"日期": "date", "收盘": "close", "涨跌幅": "pchg"})
                df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
                df["code"] = code
                df["is_limit_up"] = (df["pchg"] >= 9.8).astype(int)
                return df[["date", "code", "close", "pchg", "is_limit_up"]]
        except Exception:
            pass
        return pd.DataFrame()

    def fetch_and_cache_daily_data(self, codes, start_date, end_date, max_workers=5):
        """Fetch and cache stock daily data concurrently"""
        start_str = start_date.strftime("%Y-%m-%d")
        end_str = end_date.strftime("%Y-%m-%d")
        
        # Check existing data to avoid redundant fetching
        logger.info(f"Checking missing dates for {len(codes)} stocks between {start_str} and {end_str}")
        cursor = self.conn.cursor()
        
        codes_to_fetch = []
        for code in codes:
            cursor.execute('''
                SELECT COUNT(*) FROM daily_market_data 
                WHERE code=? AND date>=? AND date<=?
            ''', (code, start_str, end_str))
            count = cursor.fetchone()[0]
            # Assuring roughly 1 trading day per weekday minus holidays. 
            # Very simple heuristic: if we have 0 or very few, we fetch.
            # For exact checking, one could verify every date, but for speed, if we miss data we fetch the chunk.
            expected_days = (end_date - start_date).days * 5 // 7
            if count < expected_days * 0.8:  # crude threshold
                codes_to_fetch.append(code)
                
        if not codes_to_fetch:
            logger.info("All requested data appears to be cached.")
            return

        logger.info(f"Need to fetch API data for {len(codes_to_fetch)} stocks.")
        new_data = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_code = {
                executor.submit(self._fetch_stock_hist, code, start_date, end_date): code 
                for code in codes_to_fetch
            }
            
            for i, future in enumerate(as_completed(future_to_code)):
                code = future_to_code[future]
                try:
                    df = future.result()
                    if not df.empty:
                        new_data.append(df)
                except Exception as e:
                    logger.debug(f"Error fetching data for {code}: {e}")
                    
                if (i + 1) % 50 == 0:
                    logger.info(f"Progress: {i + 1}/{len(codes_to_fetch)}")

        if new_data:
            combined_df = pd.concat(new_data, ignore_index=True)
            logger.info(f"Inserting {len(combined_df)} new daily records into database...")
            # Use REPLACE to handle duplicate inserts 
            combined_df.to_sql("temp_daily", self.conn, if_exists="replace", index=False)
            cursor.execute('''
                INSERT OR REPLACE INTO daily_market_data (date, code, close, pchg, is_limit_up)
                SELECT date, code, close, pchg, is_limit_up FROM temp_daily
            ''')
            self.conn.commit()
            cursor.execute('DROP TABLE IF EXISTS temp_daily')
            logger.info("Data caching completed.")

    def get_stock_history_bulk(self, codes, start_date, end_date):
        """Retrieve cached history for multiple stocks from DB"""
        start_str = start_date.strftime("%Y-%m-%d")
        end_str = end_date.strftime("%Y-%m-%d")
        
        # Make sure data exists
        self.fetch_and_cache_daily_data(codes, start_date, end_date)
        
        # Build query for bulk selection
        codes_placeholder = ",".join(["?"] * len(codes))
        query = f'''
            SELECT date, code, close, pchg, is_limit_up 
            FROM daily_market_data 
            WHERE code IN ({codes_placeholder}) AND date>=? AND date<=?
            ORDER BY date
        '''
        params = list(codes) + [start_str, end_str]
        df = pd.read_sql_query(query, self.conn, params=params)
        df["date"] = pd.to_datetime(df["date"])
        return df

    def get_industry_mapping(self, top_components=50):
        """Fetch and cache industry mapping for stocks"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT code, name, em_industry FROM industry_mapping')
        rows = cursor.fetchall()
        
        if rows:
            mapping = {r[0]: {"name": r[1], "em_industry": r[2]} for r in rows}
            logger.info(f"Loaded {len(mapping)} industry mappings from cache")
            return mapping
            
        logger.info(f"Fetching top {top_components} industry boards and constituents from EastMoney...")
        mapping = defaultdict(dict)
        try:
            df = ak.stock_board_industry_name_em()
            # Select major industries by total market cap
            df = df.nlargest(top_components, "总市值")
            boards = df[["板块名称", "板块代码"]].values.tolist()
            
            for board_name, _ in boards:
                try:
                    cons_df = ak.stock_board_industry_cons_em(symbol=board_name)
                    if cons_df is not None and not cons_df.empty:
                        for _, row in cons_df.iterrows():
                            code = row.get("代码", "")
                            if code and "em_industry" not in mapping[code]:
                                mapping[code]["em_industry"] = board_name
                                mapping[code]["name"] = row.get("名称", "")
                    time.sleep(0.1)
                except Exception:
                    continue
            
            # Save mapping to DB
            if mapping:
                data_to_insert = [
                    (code, info["name"], info["em_industry"]) 
                    for code, info in mapping.items()
                ]
                cursor.executemany('''
                    INSERT OR REPLACE INTO industry_mapping (code, name, em_industry)
                    VALUES (?, ?, ?)
                ''', data_to_insert)
                self.conn.commit()
                logger.info(f"Saved {len(mapping)} industry mappings to database.")
                
            return dict(mapping)
        except Exception as e:
            logger.error(f"Failed to fetch industry mapping: {e}")
            return {}
