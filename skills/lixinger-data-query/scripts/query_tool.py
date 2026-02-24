#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI Helper for Lixinger Data Query Skill.
Enables LLMs to query the Lixinger API via command line.
"""

import os
import sys
import json
import argparse
import pandas as pd
from pathlib import Path

# Add current directory to path for local imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lixinger_openapi.query import query_json, query_dataframe
from lixinger_openapi.token import set_token

def get_lixinger_token() -> str:
    """Find token in environment or token.cfg in parent directories."""
    token = os.getenv("LIXINGER_TOKEN")
    if token:
        return token
    
    # Search upwards for token.cfg
    curr = Path(os.getcwd()).resolve()
    for _ in range(5): # Check up to 5 levels
        cfg_path = curr / "token.cfg"
        if cfg_path.exists():
            try:
                with open(cfg_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        if content.startswith("["):
                            import configparser
                            config = configparser.ConfigParser()
                            config.read_string(content)
                            return config.get("lixinger", "token", fallback="")
                        return content
            except Exception:
                pass
        curr = curr.parent
    return ""

def apply_row_filter(data: list, row_filter: dict) -> list:
    """
    Apply row filter to data.
    
    Filter format:
    {
        "field_name": {
            "==": value,  # equals
            "!=": value,  # not equals
            ">": value,   # greater than
            ">=": value,  # greater than or equal
            "<": value,   # less than
            "<=": value,  # less than or equal
            "in": [values],  # in list
            "not_in": [values],  # not in list
            "startswith": value,  # string starts with
            "endswith": value,  # string ends with
            "contains": value  # string contains
        }
    }
    """
    if not row_filter:
        return data
    
    filtered_data = []
    for item in data:
        match = True
        for field, conditions in row_filter.items():
            if field not in item:
                match = False
                break
            
            value = item[field]
            
            # Handle None values
            if value is None:
                if "==" in conditions and conditions["=="] is not None:
                    match = False
                    break
                continue
            
            # Apply conditions
            if isinstance(conditions, dict):
                for op, target in conditions.items():
                    try:
                        if op == "==":
                            if value != target:
                                match = False
                                break
                        elif op == "!=":
                            if value == target:
                                match = False
                                break
                        elif op == ">":
                            if not (float(value) > float(target)):
                                match = False
                                break
                        elif op == ">=":
                            if not (float(value) >= float(target)):
                                match = False
                                break
                        elif op == "<":
                            if not (float(value) < float(target)):
                                match = False
                                break
                        elif op == "<=":
                            if not (float(value) <= float(target)):
                                match = False
                                break
                        elif op == "in":
                            if value not in target:
                                match = False
                                break
                        elif op == "not_in":
                            if value in target:
                                match = False
                                break
                        elif op == "startswith":
                            if not str(value).startswith(str(target)):
                                match = False
                                break
                        elif op == "endswith":
                            if not str(value).endswith(str(target)):
                                match = False
                                break
                        elif op == "contains":
                            if str(target) not in str(value):
                                match = False
                                break
                    except (ValueError, TypeError):
                        match = False
                        break
                
                if not match:
                    break
            else:
                # Simple equality check
                if value != conditions:
                    match = False
                    break
        
        if match:
            filtered_data.append(item)
    
    return filtered_data

def main():
    parser = argparse.ArgumentParser(description="Lixinger Data Query Tool")
    parser.add_argument("--suffix", required=True, help="API URL suffix (e.g., 'cn.company')")
    parser.add_argument("--params", required=True, help="JSON string of query parameters")
    parser.add_argument("--format", choices=["json", "text", "csv"], default="csv", help="Output format (default: csv)")
    parser.add_argument("--limit", type=int, default=100, help="Limit number of rows returned (default: 100)")
    parser.add_argument("--columns", help="Comma-separated list of columns to include (e.g., 'stockCode,name,pe_ttm')")
    parser.add_argument("--row-filter", help="JSON string for row filtering (e.g., '{\"pe_ttm\": {\">=\": 10, \"<=\": 20}}')")
    parser.add_argument("--flatten", help="Flatten nested array field (e.g., 'constituents' to extract nested items)")
    parser.add_argument("--cache", action=argparse.BooleanOptionalAction, default=True, help="Enable/disable caching")
    parser.add_argument("--save-list", help="Save the resulting stock codes to a named session list")
    parser.add_argument("--use-list", help="Use a previously saved session list as stockCodes")
    
    args = parser.parse_args()

    # Initialize Token
    token = get_lixinger_token()
    if token:
        set_token(token, write_token=False)

    # Import CacheManager only if needed
    from cache_manager import CacheManager
    cache = CacheManager()

    try:
        query_params = json.loads(args.params)
        
        # Parse row filter if provided
        row_filter = None
        if args.row_filter:
            try:
                row_filter = json.loads(args.row_filter)
            except json.JSONDecodeError:
                print("Error: Invalid JSON in --row-filter", file=sys.stderr)
                sys.exit(1)
        
        # Parse columns if provided
        columns = None
        if args.columns:
            columns = [c.strip() for c in args.columns.split(',')]
        
        # Handle Session Lists (Use)
        if args.use_list:
            saved_codes = cache.get_list(args.use_list)
            if saved_codes:
                query_params['stockCodes'] = saved_codes
            else:
                print(f"Warning: Session list '{args.use_list}' not found.", file=sys.stderr)

        # Handle Caching
        result = None
        if args.cache:
            # Default cache: 1 day
            max_age_days = 1
            result = cache.get(args.suffix, query_params, max_age_days=max_age_days)

        if not result:
            if args.format == "json":
                result = query_json(args.suffix, query_params)
            else:
                result = query_json(args.suffix, query_params)
            
            if args.cache and result and result.get('code') == 1:
                # Default cache expiry: 1 day
                cache.set(args.suffix, query_params, result, expiry_days=1)

        # Handle Session Lists (Save)
        if args.save_list and result and result.get('code') == 1 and isinstance(result.get('data'), list):
            # Try to find 'stockCode' or 'stockCodes' in data
            extracted_codes = []
            for item in result['data']:
                if 'stockCode' in item: extracted_codes.append(item['stockCode'])
                elif 'stockCodes' in item: extracted_codes.extend(item['stockCodes'])
            
            if extracted_codes:
                # Deduplicate
                unique_codes = list(dict.fromkeys(extracted_codes))
                cache.save_list(args.save_list, unique_codes)
                print(f"# NOTE: Saved {len(unique_codes)} codes to session list '{args.save_list}'", file=sys.stdout)

        if args.format == "json":
            # Apply row filter and column filter
            if result.get('code') == 1 and isinstance(result.get('data'), list):
                # Flatten nested arrays if specified
                if args.flatten:
                    flattened_data = []
                    for item in result['data']:
                        if args.flatten in item and isinstance(item[args.flatten], list):
                            # Extract nested items
                            for nested_item in item[args.flatten]:
                                flattened_data.append(nested_item)
                        else:
                            flattened_data.append(item)
                    result['data'] = flattened_data
                
                # Apply row filter
                if row_filter:
                    result['data'] = apply_row_filter(result['data'], row_filter)
                
                # Filter columns if specified
                if columns:
                    filtered_data = []
                    for item in result['data']:
                        filtered_item = {k: v for k, v in item.items() if k in columns}
                        filtered_data.append(filtered_item)
                    result['data'] = filtered_data
                
                # Truncate
                if len(result['data']) > args.limit:
                    result['data'] = result['data'][:args.limit]
                    result['_note'] = f"Output truncated to {args.limit} rows."
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            # Convert JSON result to DataFrame
            if result.get('code') == 1:
                from pandas import json_normalize
                
                # Flatten nested arrays if specified
                data = result.get('data', [])
                if args.flatten and data:
                    flattened_data = []
                    for item in data:
                        if args.flatten in item and isinstance(item[args.flatten], list):
                            # Extract nested items
                            for nested_item in item[args.flatten]:
                                flattened_data.append(nested_item)
                        else:
                            flattened_data.append(item)
                    data = flattened_data
                
                # Apply row filter
                if row_filter and data:
                    data = apply_row_filter(data, row_filter)
                
                df = json_normalize(data) if data else pd.DataFrame()
                
                # Filter columns if specified
                if columns and not df.empty:
                    # Only keep columns that exist in the dataframe
                    available_columns = [c for c in columns if c in df.columns]
                    if available_columns:
                        df = df[available_columns]
                    else:
                        print(f"Warning: None of the specified columns found in data. Available columns: {', '.join(df.columns)}", file=sys.stderr)
                
                # Truncate DataFrame
                if len(df) > args.limit:
                    df = df.head(args.limit)
                    print(f"# NOTE: Output truncated to {args.limit} rows.", file=sys.stdout)
                
                if args.format == "csv":
                    print(df.to_csv(index=False))
                else:
                    print(df.to_string())
            else:
                error_info = result.get('error', result.get('msg', 'Unknown error'))
                if isinstance(error_info, dict):
                    error_msg = error_info.get('message', str(error_info))
                    if 'messages' in error_info:
                        error_msg += " " + str(error_info['messages'])
                else:
                    error_msg = str(error_info)
                print(f"Error: {error_msg} (Code: {result.get('code', -1)})", file=sys.stderr)
                sys.exit(1)

    except json.JSONDecodeError:
        print("Error: Invalid JSON in --params", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
