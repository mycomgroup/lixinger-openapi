# 数据获取指南 — board-crowding-risk-monitor

使用 `query_tool.py` 获取板块拥挤度监控所需数据。

---

## API 清单

### 1. 获取行业换手率与估值分位数（核心数据）

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/industry/fundamental/sw_2021" \
  --params '{"date": "2026-03-27", "stockCodes": ["360000"], "metricsList": ["pe_ttm.mcw","pe_ttm.y10.mcw.cvpos","pb.mcw","to_r","ta","mc"]}' \
  --columns "stockCode,date,pe_ttm.mcw,pe_ttm.y10.mcw.cvpos,pb.mcw,to_r,ta,mc" \
  --limit 1
```

**用途**：获取目标行业当日：
- `pe_ttm.y10.mcw.cvpos`：PE 10年历史分位数（直接用于估值维度拥挤度子分）
- `to_r`：换手率（需要历史序列计算分位数）
- `ta`：成交额（用于计算全市场占比）

---

### 2. 获取行业换手率历史序列（计算换手率分位）

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/industry/fundamental/sw_2021" \
  --params '{"startDate": "2023-03-27", "endDate": "2026-03-27", "stockCodes": ["360000"], "metricsList": ["to_r","ta"]}' \
  --columns "stockCode,date,to_r,ta" \
  --limit 800
```

**用途**：获取近3年换手率历史数据，用于计算当前换手率的历史分位数。

**换手率分位计算**：
```python
# 计算当前换手率在历史序列中的分位数（越高越拥挤）
history = [all historical to_r values]
current = today_to_r
percentile = len([x for x in history if x < current]) / len(history)
```

---

### 3. 获取全市场成交额（计算行业成交占比）

```bash
# 获取所有申万一级行业的成交额，加总得到全市场行业成交额近似值
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/industry/fundamental/sw_2021" \
  --params '{"date": "2026-03-27", "stockCodes": ["110000","210000","220000","230000","240000","270000","280000","330000","340000","350000","360000","370000","410000","420000","430000","450000","460000","480000","490000","510000","610000","620000","630000","640000","650000","710000","720000","730000"], "metricsList": ["ta"]}' \
  --columns "stockCode,ta" \
  --limit 50
```

**成交占比计算**：
```python
total_market_ta = sum([ta for all industries])
target_share = target_ta / total_market_ta

# 全A日成交额通常在1.5-4万亿之间
# 也可直接用常见值（近6个月均值约2.5万亿）作为分母近似
```

---

### 4. 获取行业成分股（获取龙头股用于龙头破位检验）

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/industry/constituents/sw_2021" \
  --params '{"stockCodes": ["360000"]}' \
  --columns "stockCode,name,mc" \
  --limit 20
```

**用途**：获取行业成分股，按市值排序，取前2名作为"龙头股"监控对象。
- 若龙头股收盘价跌破20日均线 → 触发"龙头破位"脆弱触发器

**注意**：龙头股的具体价格数据需通过其他方式获取（如 AKShare 或人工观察），理杏仁 API 目前不提供个股日线行情。

---

### 5. 行业成交额历史序列（计算成交萎缩触发器）

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/industry/fundamental/sw_2021" \
  --params '{"startDate": "2026-02-25", "endDate": "2026-03-27", "stockCodes": ["360000"], "metricsList": ["ta","to_r"]}' \
  --columns "stockCode,date,ta,to_r" \
  --limit 25
```

**用途**：获取近20个交易日的成交额序列，用于：
- 计算"成交萎缩"触发器：近3日均值是否低于20日均值的70%
- 计算"量价背离"触发器：近5日成交额是否萎缩超过25%

---

### 6. 概念板块数据（AKShare，可选）

当 `subject_type = "concept"` 时，可尝试使用 AKShare 获取概念资金流：

```python
# AKShare 接口（需 Python 环境）
import akshare as ak
df = ak.stock_fund_flow_concept()
# 返回：concept_name, 今日主力净流入, 今日资金流入
```

**注意**：若 AKShare 不可用，降级为仅使用理杏仁行业数据，在 `data_gaps` 中标注。

---

## 拥挤度子分计算参考

### 换手率子分（0-100）

```python
def turnover_sub_score(to_r_percentile):
    """to_r_percentile: 0-1 的历史分位数"""
    return min(100, to_r_percentile * 100)
    # 分位数90% → 子分90
    # 分位数50% → 子分50
```

### 成交占比子分（0-100）

```python
def volume_share_sub_score(current_share, historical_75_pct_share):
    """current_share: 当日成交占比（0-1）"""
    if current_share >= historical_75_pct_share * 1.5:
        return 100
    elif current_share >= historical_75_pct_share:
        return 75 + (current_share - historical_75_pct_share) / (historical_75_pct_share * 0.5) * 25
    else:
        return current_share / historical_75_pct_share * 75
```

### 估值分位子分（直接使用 pe_ttm.y10.mcw.cvpos）

```python
def valuation_sub_score(pe_percentile):
    """pe_percentile: 0-1 的 PE 历史分位数"""
    return min(100, pe_percentile * 100)
```

---

## 数据源对比

| 数据需求 | API | 可用性 | 备注 |
|---------|-----|-------|------|
| 换手率历史序列 | cn/industry/fundamental/sw_2021（startDate模式） | 高 | 核心数据 |
| PE 历史分位数 | pe_ttm.y10.mcw.cvpos 字段 | 高 | 直接可用 |
| 行业成交额 | ta 字段 | 高 | 需计算占比 |
| 概念资金流 | AKShare | 低 | 降级数据源 |
| 龙头股日线价格 | 需要独立个股数据源 | 低 | 降级数据源 |

---

## 查找更多 API

详细的 API 发现方法，参考：`.claude/plugins/query_data/lixinger-api-docs/SKILL.md`
