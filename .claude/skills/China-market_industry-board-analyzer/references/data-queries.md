# 数据获取指南

使用 `query_tool.py` 获取 industry-board-analyzer 所需的数据。

---

## 实际使用API清单（2026-03-24更新）

### 1. cn/industry - 行业分类信息

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/industry" \
  --params '{"source": "sw", "level": "one"}' \
  --columns "stockCode,name" \
  --limit 50
```

**用途**: 获取申万一级行业分类列表（28个行业）

**返回字段**: stockCode, name

---

### 2. cn/industry/fundamental/sw_2021 - 行业基本面数据

#### 2.1 当日快照（多行业批量查询）

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/industry/fundamental/sw_2021" \
  --params '{"date": "2026-03-23", "stockCodes": ["110000","210000","220000","230000","240000","270000","280000","330000","340000","350000","360000","370000","410000","420000","430000","450000","460000","480000","490000","510000","610000","620000","630000","640000","650000","710000","720000","730000"], "metricsList": ["pe_ttm.mcw","pe_ttm.y10.mcw.cvpos","pb.mcw","pb.y10.mcw.cvpos","dyr.mcw","mc","to_r","ta"]}' \
  --columns "stockCode,pe_ttm.mcw,pe_ttm.y10.mcw.cvpos,pb.mcw,pb.y10.mcw.cvpos,dyr.mcw,mc,to_r,ta" \
  --limit 50
```

**用途**: 获取所有行业的估值指标（PE-TTM、PB、股息率、市值、成交额等）

**返回字段**:
- `pe_ttm.mcw`: PE-TTM（市值加权）
- `pe_ttm.y10.mcw.cvpos`: PE-TTM 10年分位数
- `pb.mcw`: PB（市值加权）
- `pb.y10.mcw.cvpos`: PB 10年分位数
- `dyr.mcw`: 股息率
- `mc`: 市值
- `to_r`: 换手率
- `ta`: 成交金额

**注意事项**:
- 使用 `date` 参数时，`stockCodes` 支持多个行业代码
- 日期格式: YYYY-MM-DD
- 数据通常在T+1日更新

#### 2.2 历史数据查询（单行业，用于计算涨跌幅）

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/industry/fundamental/sw_2021" \
  --params '{"startDate": "2026-02-20", "endDate": "2026-02-28", "stockCodes": ["490000"], "metricsList": ["mc"]}' \
  --columns "stockCode,date,mc" \
  --limit 5
```

**用途**: 获取单个行业的历史市值数据，用于计算行业涨跌幅

**注意事项**:
- 使用 `startDate` 参数时，`stockCodes` 只能包含1个行业代码
- 日期格式: YYYY-MM-DD
- 通过比较不同时期的市值变化来计算行业涨跌幅

#### 2.3 批量历史查询（逐个行业）

```bash
for code in 110000 210000 220000 230000 240000 270000 280000 330000 340000 350000 360000 370000; do
  python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
    --suffix "cn/industry/fundamental/sw_2021" \
    --params "{\"startDate\": \"2026-02-20\", \"endDate\": \"2026-02-28\", \"stockCodes\": [\"$code\"], \"metricsList\": [\"mc\"]}" \
    --columns "stockCode,date,mc" \
    --limit 1
done
```

**用途**: 批量获取各行业的历史市值数据

---

### 3. cn/industry/fs/sw_2021/hybrid - 行业财务数据

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/industry/fs/sw_2021/hybrid" \
  --params '{"date": "2025-09-30", "stockCodes": ["490000"], "metricsList": ["q.ps.oi.t","q.ps.oi.t_y2y","q.ps.np.t","q.ps.np.t_y2y"]}' \
  --columns "stockCode,q.ps.oi.t,q.ps.oi.t_y2y,q.ps.np.t,q.ps.np.t_y2y" \
  --limit 1
```

**用途**: 获取行业财务数据（营业收入、净利润等）

**返回字段**:
- `q.ps.oi.t`: 营业收入（当期）
- `q.ps.oi.t_y2y`: 营业收入同比
- `q.ps.np.t`: 净利润（当期）
- `q.ps.np.t_y2y`: 净利润同比

**注意事项**:
- 该API目前仅对金融行业（如非银金融490000）返回数据
- 其他行业可能暂无数据
- 日期格式: YYYY-MM-DD 或 latest
- 建议作为可选数据源使用

---

## 分析方法论

### 1. 行业涨跌幅计算

通过比较不同时期的行业市值来计算涨跌幅：

```python
# 1个月涨跌幅
perf_1m = (current_mc - historical_mc_1m) / historical_mc_1m * 100

# 3个月涨跌幅
perf_3m = (current_mc - historical_mc_3m) / historical_mc_3m * 100
```

### 2. 行业综合评分

基于以下维度计算综合评分：

```python
# 估值分位得分 (0-100, 越低越好)
pe_score = max(0, 100 - pe_pos)
pb_score = max(0, 100 - pb_pos)

# 涨跌幅得分 (标准化到0-100)
perf_score = (perf_1m + 25) / 50 * 100

# 股息率得分
dyr_score = min(100, dyr * 20)

# 综合评分 (加权平均)
total_score = pe_score * 0.3 + pb_score * 0.3 + perf_score * 0.3 + dyr_score * 0.1
```

### 3. 估值分位数解读

- **PE分位数 < 30%**: 历史低估区域
- **PE分位数 30%-70%**: 历史中位区域
- **PE分位数 > 70%**: 历史高估区域
- **PE分位数 > 90%**: 历史极高估区域

---

## 数据源对比

| API | 数据内容 | 更新频率 | 备注 |
|-----|---------|---------|------|
| cn/industry | 行业分类信息 | 不定期 | 申万一级/二级/三级 |
| cn/industry/fundamental/sw_2021 | PE/PB/股息率/市值 | 日频 | 核心数据源 |
| cn/industry/fs/sw_2021/hybrid | 财务数据 | 季频 | 仅金融行业有数据 |
| cn/industry/constituents/sw_2021 | 行业成分股 | 不定期 | 可用于个股分析 |

---

## 参数说明

- `--suffix`: API 路径
- `--params`: JSON 格式参数
- `--columns`: 指定返回字段（推荐使用，节省 30-40% token）
- `--row-filter`: 过滤条件
- `--limit`: 限制返回行数

---

## 注意事项

1. **日期参数**: 
   - 使用 `date` 参数时，`stockCodes` 支持多个行业代码
   - 使用 `startDate` 参数时，`stockCodes` 只能包含1个行业代码

2. **数据更新**:
   - 基本面数据通常在T+1日更新
   - 财务数据按季度更新

3. **API限制**:
   - 每个API有访问次数限制
   - 建议使用缓存减少重复查询

---

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../lixinger-data-query/SKILL.md`

---

## 本次分析实际数据查询（2026-03-24）

### 1. 获取申万一级行业分类

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/industry" \
  --params '{"source": "sw", "level": "one"}' \
  --limit 50
```

**结果**: 获取到28个申万一级行业

---

### 2. 获取所有行业估值数据（批量查询）

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/industry/fundamental/sw_2021" \
  --params '{"date": "2026-03-23", "stockCodes": ["110000", "210000", "220000", "230000", "240000", "270000", "280000", "330000", "340000", "350000", "360000", "370000", "410000", "420000", "430000", "450000", "460000", "480000", "490000", "510000", "610000", "620000", "630000", "640000", "650000", "710000", "720000", "730000"], "metricsList": ["pe_ttm.y10.mcw.cvpos", "pe_ttm.mcw", "pb.mcw", "dyr.mcw", "mc", "ta"]}' \
  --columns "stockCode,date,pe_ttm.y10.mcw.cvpos,pe_ttm.mcw,pb.mcw,dyr.mcw,mc,ta"
```

**返回字段说明**:
- `pe_ttm.y10.mcw.cvpos`: PE-TTM 10年分位数（0-1，越低越低估）
- `pe_ttm.mcw`: PE-TTM（市值加权）
- `pb.mcw`: PB（市值加权）
- `dyr.mcw`: 股息率
- `mc`: 市值（元）
- `ta`: 成交金额（元）

**本次分析核心发现**:
| 行业 | PE分位点 | PE-TTM | 股息率 | 估值状态 |
|------|----------|--------|--------|----------|
| 非银金融 | 0.0% | 10.17 | 2.31% | 极度低估 |
| 食品饮料 | 1.4% | 20.04 | 3.80% | 极度低估 |
| 家用电器 | 12.8% | 14.94 | 3.79% | 低估 |
| 银行 | 72.0% | 6.69 | 4.65% | 合理偏高 |
| 电子 | 89.4% | 74.54 | 0.53% | 高估 |
| 计算机 | 79.7% | 179.31 | 0.78% | 高估 |

---

### 3. 获取单行业历史数据（用于计算涨跌幅）

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/industry/fundamental/sw_2021" \
  --params '{"startDate": "2026-02-01", "endDate": "2026-03-24", "stockCodes": ["480000"], "metricsList": ["pe_ttm.y10.mcw.cvpos", "pe_ttm.mcw", "pb.mcw", "dyr.mcw", "mc", "ta"]}' \
  --columns "stockCode,date,pe_ttm.y10.mcw.cvpos,pe_ttm.mcw,pb.mcw,dyr.mcw,mc,ta" \
  --limit 10
```

**用途**: 获取银行行业近2个月的估值变化趋势

---

## 数据源选择说明

### 理杏仁API（本次使用）
- **优势**: 数据质量高、更新及时、支持历史查询
- **适用**: 估值分析、历史分位数计算
- **限制**: 暂无行业资金流向数据

### AkShare（备用数据源）
- **接口**: `stock_fund_flow_industry`
- **优势**: 有行业资金流向数据
- **适用**: 资金流向分析
- **限制**: 数据可能有延迟

---

## 分析结论摘要

### 低估行业（PE分位点<30%）
1. **非银金融** (0.0%): 估值极度低估，但需关注景气度
2. **食品饮料** (1.4%): 估值处于历史低位，股息率3.80%
3. **家用电器** (12.8%): 估值低估，股息率3.79%
4. **交通运输** (25.6%): 估值偏低，股息率2.71%
5. **公用事业** (32.6%): 估值合理偏低，股息率2.31%

### 高估行业（PE分位点>70%）
1. **电子** (89.4%): 估值高估，警惕调整风险
2. **化工** (89.6%): 估值高估，周期性风险
3. **轻工制造** (97.3%): 估值极高估
4. **建筑材料** (88.7%): 估值高估
5. **计算机** (79.7%): 估值高估，AI主题驱动

### 高股息行业（股息率>3%）
1. **银行** (4.65%): 股息率最高
2. **食品饮料** (3.80%): 低估+高股息
3. **家用电器** (3.79%): 低估+高股息
4. **纺织服装** (3.30%): 中等估值+高股息
