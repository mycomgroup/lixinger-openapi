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

def main():
    parser = argparse.ArgumentParser(description="Lixinger Data Query Tool")
    parser.add_argument("--suffix", required=True, help="API URL suffix (e.g., 'cn.company')")
    parser.add_argument("--params", required=True, help="JSON string of query parameters")
    parser.add_argument("--format", choices=["json", "text", "csv"], default="text", help="Output format")
    parser.add_argument("--limit", type=int, default=100, help="Limit number of rows returned (default: 100)")
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

    # Load metadata
    metadata = {}
    metadata_path = os.path.join(os.path.dirname(__file__), "../resources/metadata.json")
    if os.path.exists(metadata_path):
        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load metadata: {str(e)}", file=sys.stderr)

    try:
        query_params = json.loads(args.params)
        
        # Handle Session Lists (Use)
        if args.use_list:
            saved_codes = cache.get_list(args.use_list)
            if saved_codes:
                query_params['stockCodes'] = saved_codes
            else:
                print(f"Warning: Session list '{args.use_list}' not found.", file=sys.stderr)

        # Check for matching metadata
        # Normalize suffix (replace . with / for lookup)
        lookup_suffix = args.suffix.replace('.', '/')
        # 美股接口适配
        if lookup_suffix.startswith('us/'):
            # 确保美股接口路径正确
            pass
        api_meta = metadata.get(lookup_suffix)

        # Handle Caching
        result = None
        if args.cache:
            # Determine max_age based on metadata
            max_age_days = 1
            if api_meta:
                freq = api_meta.get('update_frequency', 'daily')
                if freq == 'realtime':
                    max_age_days = 0.04 # ~1 hour
                elif freq == 'weekly':
                    max_age_days = 7
                elif freq == 'monthly':
                    max_age_days = 30
            
            result = cache.get(args.suffix, query_params, max_age_days=max_age_days)

        if not result:
            if args.format == "json":
                result = query_json(args.suffix, query_params)
            else:
                result = query_json(args.suffix, query_params)
            
            if args.cache and result and result.get('code') == 1:
                expiry_days = 1
                if api_meta:
                    freq = api_meta.get('update_frequency', 'daily')
                    if freq == 'realtime': expiry_days = 0.04
                    elif freq == 'weekly': expiry_days = 7
                    elif freq == 'monthly': expiry_days = 30
                cache.set(args.suffix, query_params, result, expiry_days=expiry_days)

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
            # Apply conversions if it's a list of dictionaries
            if api_meta and result.get('code') == 1 and isinstance(result.get('data'), list):
                for item in result['data']:
                    for conv in api_meta.get('conversions', []):
                        field = conv['field']
                        if field in item and item[field] is not None:
                            try:
                                val = float(item[field])
                                if conv['operation'] == 'div':
                                    val = val / conv['factor']
                                elif conv['operation'] == 'mul':
                                    val = val * conv['factor']
                                
                                if 'round' in conv:
                                    val = round(val, conv['round'])
                                item[conv.get('name', field)] = val
                            except (ValueError, TypeError):
                                pass

            # Truncate data list
            if result.get('code') == 1 and isinstance(result.get('data'), list):
                if len(result['data']) > args.limit:
                    result['data'] = result['data'][:args.limit]
                    result['_note'] = f"Output truncated to {args.limit} rows."
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            # Convert JSON result to DataFrame if it's not already (it isn't if we used query_json)
            # We recreate the structure expected by query_dataframe logic
            if result.get('code') == 1:
                from pandas import json_normalize
                df = json_normalize(result['data']) if result.get('data') else pd.DataFrame()
                
                # Apply conversions to DataFrame
                if api_meta:
                    for conv in api_meta.get('conversions', []):
                        field = conv['field']
                        if field in df.columns:
                            try:
                                # Convert to numeric if needed
                                df[field] = pd.to_numeric(df[field], errors='coerce')
                                
                                new_val = df[field]
                                if conv['operation'] == 'div':
                                    new_val = new_val / conv['factor']
                                elif conv['operation'] == 'mul':
                                    new_val = new_val * conv['factor']
                                
                                # Use new column name if provided, otherwise overwrite
                                target_col = conv.get('name', field)
                                if 'round' in conv:
                                    df[target_col] = new_val.round(conv['round'])
                                else:
                                    df[target_col] = new_val
                            except Exception as conv_err:
                                print(f"Warning: Conversion for {field} failed: {str(conv_err)}", file=sys.stderr)

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
