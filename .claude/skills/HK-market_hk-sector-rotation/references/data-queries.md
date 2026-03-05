# 港股行业轮动分析 - 数据获取指南

本文档说明如何使用 `query_tool.py` 获取港股行业轮动分析所需的数据。

---

## 核心数据需求

### 1. 行业表现数据
- 各行业涨跌幅
- 行业市值变化
- 行业成交量成交额
- 行业估值指标

### 2. 行业资金流向
- 南向资金行业分布
- 行业资金净流入
- 资金流向趋势
- 资金流向持续性

### 3. 相对强度数据
- 行业相对市场表现
- 行业排名变化
- 相对强度趋势
- 相对强度动量

### 4. 历史轮动数据
- 历史行业表现
- 轮动周期识别
- 轮动模式分析

---

## 数据查询示例

### 1. 获取所有行业当日表现 ⭐ 核心

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/industry/fundamental/hsi" \
  --params '{"stockCodes": ["H50"], "date": "2026-02-24", "metricsList": ["ta", "mc", "pe_ttm.mcw", "pb.mcw"]}' \
  --limit 50
```

**用途**: 获取所有行业的当日表现数据

**关键指标**:
- `ta`: 成交金额
- `mc`: 市值
- `pe_ttm.mcw`: PE-TTM（市值加权）
- `pb.mcw`: PB（市值加权）

### 2. 获取行业历史表现（用于轮动分析）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/industry/fundamental/hsi" \
  --params '{"stockCodes": ["H5070"], "startDate": "2026-01-01", "endDate": "2026-02-24", "metricsList": ["mc"]}' \
  --columns "industryCode,date,mc" \
  --limit 30
```

**用途**: 获取单个行业的历史表现，用于轮动趋势分析

**说明**: 使用 startDate 时只能查询单个行业，需要多个行业时使用循环查询

**行业代码示例**:
- H50: 能源业
- H5010: 原材料业
- H5020: 工业
- H5030: 非必需消费品
- H5040: 必需消费品
- H5050: 医疗保健
- H5060: 金融业
- H5070: 资讯科技业
- H5080: 电讯服务
- H5090: 公用事业
- H5100: 地产建筑业

### 3. 获取行业南向资金流向 ⭐ 核心

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/industry/mutual-market/hsi" \
  --params '{"stockCode": "H50", "startDate": "2026-01-01", "endDate": "2026-02-24", "metricsList": ["shareholdingsMoney", "shareholdingsMoneyToMarketCap"]}' \
  --columns "industryCode,date,shareholdingsMoney,shareholdingsMoneyToMarketCap" \
  --limit 50
```

**用途**: 获取各行业的南向资金持仓数据

**关键指标**:
- `shareholdingsMoney`: 南向资金持股金额（港币）
- `shareholdingsMoneyToMarketCap`: 南向资金持股占市值比例

**计算资金流向**:
```python
# 通过持股金额变化计算净流入
net_inflow = shareholdingsMoney_today - shareholdingsMoney_yesterday
```

### 4. 获取行业历史资金流向

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/industry/mutual-market/hsi" \
  --params '{"stockCode": "H50", "startDate": "2026-01-01", "endDate": "2026-02-24", "metricsList": ["shareholdingsMoney"]}' \
  --columns "date,shareholdingsMoney" \
  --limit 30
```

**用途**: 获取单个行业的历史资金流向趋势

### 5. 获取行业列表和分类

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/industry" \
  --params '{"source": "hsi"}' \
  --columns "industryCode,industryName,industryLevel" \
  --limit 50
```

**用途**: 获取所有行业分类信息，用于行业名称映射

### 6. 获取恒生指数表现（作为基准）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/index/fundamental" \
  --params '{"stockCodes": ["HSI"], "startDate": "2026-01-01", "endDate": "2026-02-24", "metricsList": ["cp", "cpc"]}' \
  --columns "date" \
  --limit 30
```

**用途**: 获取市场基准表现，用于计算相对强度

### 7. 获取行业估值历史分位数

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/industry/fundamental/hsi" \
  --params '{"stockCodes": ["H50", "H5010", "H5020", "H5030", "H5040", "H5050", "H5060", "H5070", "H5080", "H5090", "H5100"], "date": "2026-02-24", "metricsList": ["pe_ttm.mcw", "pe_ttm.y10.mcw.cvpos", "pb.mcw", "pb.y10.mcw.cvpos"]}' \
  --columns "industryCode,pe_ttm.mcw,pe_ttm.y10.mcw.cvpos,pb.mcw,pb.y10.mcw.cvpos" \
  --limit 50
```

**用途**: 获取行业估值及历史分位数，用于估值轮动分析

**关键指标**:
- `pe_ttm.y10.mcw.cvpos`: PE 10年历史分位数
- `pb.y10.mcw.cvpos`: PB 10年历史分位数

### 8. 获取行业成分股列表

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company" \
  --params '{}' \
  --columns "stockCode,name,market" \
  --limit 1000
```

**用途**: 获取所有港股公司列表

### 9. 获取个股行业归属

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/industries" \
  --params '{"stockCode": "00700"}' \
  --columns "stockCode,industryCode,industryName,industryLevel"
```

**用途**: 确定个股所属行业

### 10. 获取行业历史市值数据（用于趋势分析）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/industry/fundamental/hsi" \
  --params '{"stockCodes": ["H5070"], "startDate": "2026-01-01", "endDate": "2026-02-24", "metricsList": ["mc", "ta"]}' \
  --columns "date,mc,ta" \
  --limit 30
```

**用途**: 获取行业历史市值和成交额数据，用于趋势分析

**说明**: 理杏仁API不提供行业K线数据，使用市值和成交额数据分析行业趋势

---

## 行业轮动分析计算

### 1. 计算相对强度
```python
def calculate_relative_strength(sector_returns, market_return):
    """
    计算行业相对强度
    
    相对强度 = 行业收益率 / 市场收益率
    相对强度 > 1: 行业跑赢市场
    相对强度 < 1: 行业跑输市场
    """
    relative_strength = {}
    
    for sector, sector_return in sector_returns.items():
        rs = sector_return / market_return if market_return != 0 else 1.0
        relative_strength[sector] = round(rs, 2)
    
    return relative_strength

# 使用示例
sector_returns = {
    '科技': 3.2,
    '医疗保健': 2.8,
    '消费品': 2.1,
    '金融': 1.5,
    '地产': -1.8
}
market_return = 1.8  # 恒生指数涨幅

rs = calculate_relative_strength(sector_returns, market_return)
print("相对强度:", rs)
# 输出: {'科技': 1.78, '医疗保健': 1.56, '消费品': 1.17, '金融': 0.83, '地产': -1.0}
```

### 2. 计算行业资金净流入
```python
def calculate_sector_flow(today_holdings, yesterday_holdings):
    """
    计算行业资金净流入
    """
    sector_flows = {}
    
    for sector in today_holdings.keys():
        today = today_holdings[sector]
        yesterday = yesterday_holdings.get(sector, today)
        
        net_flow = today - yesterday
        flow_rate = (net_flow / yesterday * 100) if yesterday != 0 else 0
        
        sector_flows[sector] = {
            'net_flow': round(net_flow / 100000000, 2),  # 转换为亿元
            'flow_rate': round(flow_rate, 2)
        }
    
    return sector_flows

# 使用示例
today_holdings = {
    '科技': 150000000000,  # 1500亿港元
    '医疗保健': 80000000000,
    '消费品': 120000000000
}
yesterday_holdings = {
    '科技': 145000000000,
    '医疗保健': 78000000000,
    '消费品': 118000000000
}

flows = calculate_sector_flow(today_holdings, yesterday_holdings)
for sector, flow in flows.items():
    print(f"{sector}: 净流入{flow['net_flow']}亿 ({flow['flow_rate']:+.2f}%)")
```

### 3. 识别轮动信号
```python
def detect_rotation_signal(sector_data, threshold=0.5):
    """
    识别行业轮动信号
    
    参数:
    - sector_data: 行业数据（包含相对强度、资金流向等）
    - threshold: 轮动信号阈值
    
    返回:
    - rotation_signal: 轮动信号强度（0-10）
    - rotation_direction: 轮动方向
    """
    # 计算相对强度变化
    rs_changes = []
    for sector, data in sector_data.items():
        rs_change = data['rs_current'] - data['rs_previous']
        rs_changes.append((sector, rs_change))
    
    # 按相对强度变化排序
    rs_changes.sort(key=lambda x: x[1], reverse=True)
    
    # 识别强势和弱势行业
    strong_sectors = [s for s, c in rs_changes[:3] if c > threshold]
    weak_sectors = [s for s, c in rs_changes[-3:] if c < -threshold]
    
    # 计算轮动信号强度
    if len(strong_sectors) >= 2 and len(weak_sectors) >= 2:
        signal_strength = min(10, len(strong_sectors) + len(weak_sectors))
        rotation_direction = f"{weak_sectors[0]}→{strong_sectors[0]}"
    else:
        signal_strength = 0
        rotation_direction = "无明显轮动"
    
    return {
        'signal_strength': signal_strength,
        'rotation_direction': rotation_direction,
        'strong_sectors': strong_sectors,
        'weak_sectors': weak_sectors
    }
```

### 4. 计算行业配置建议
```python
def calculate_allocation_suggestion(sector_data, benchmark_weights):
    """
    计算行业配置建议
    
    基于相对强度、资金流向、估值分位数等因素
    """
    suggestions = {}
    
    for sector, data in sector_data.items():
        score = 0
        
        # 相对强度评分（40%权重）
        if data['relative_strength'] > 1.2:
            score += 40
        elif data['relative_strength'] > 1.0:
            score += 20
        elif data['relative_strength'] < 0.8:
            score -= 40
        elif data['relative_strength'] < 1.0:
            score -= 20
        
        # 资金流向评分（30%权重）
        if data['flow_rate'] > 5:
            score += 30
        elif data['flow_rate'] > 0:
            score += 15
        elif data['flow_rate'] < -5:
            score -= 30
        elif data['flow_rate'] < 0:
            score -= 15
        
        # 估值评分（30%权重）
        if data['pe_percentile'] < 30:
            score += 30
        elif data['pe_percentile'] < 50:
            score += 15
        elif data['pe_percentile'] > 70:
            score -= 30
        elif data['pe_percentile'] > 50:
            score -= 15
        
        # 确定配置建议
        benchmark_weight = benchmark_weights.get(sector, 10)
        if score >= 50:
            suggestion = '超配'
            target_weight = benchmark_weight * 1.2
        elif score <= -50:
            suggestion = '低配'
            target_weight = benchmark_weight * 0.8
        else:
            suggestion = '标配'
            target_weight = benchmark_weight
        
        suggestions[sector] = {
            'score': score,
            'suggestion': suggestion,
            'target_weight': round(target_weight, 1)
        }
    
    return suggestions
```

### 5. 轮动周期分析
```python
def analyze_rotation_cycle(historical_data, window=20):
    """
    分析行业轮动周期
    
    参数:
    - historical_data: 历史行业表现数据
    - window: 滚动窗口大小（天）
    """
    cycles = []
    
    for i in range(window, len(historical_data)):
        window_data = historical_data[i-window:i]
        
        # 计算窗口内的行业排名变化
        rank_changes = calculate_rank_changes(window_data)
        
        # 识别轮动周期
        if is_rotation_cycle(rank_changes):
            cycle_info = {
                'start_date': window_data[0]['date'],
                'end_date': window_data[-1]['date'],
                'duration': window,
                'rotation_pattern': identify_pattern(rank_changes)
            }
            cycles.append(cycle_info)
    
    return cycles

def calculate_rank_changes(window_data):
    """计算排名变化"""
    first_ranks = window_data[0]['sector_ranks']
    last_ranks = window_data[-1]['sector_ranks']
    
    changes = {}
    for sector in first_ranks.keys():
        changes[sector] = last_ranks[sector] - first_ranks[sector]
    
    return changes

def is_rotation_cycle(rank_changes):
    """判断是否为轮动周期"""
    # 如果有行业排名变化超过3位，认为发生了轮动
    significant_changes = [abs(c) for c in rank_changes.values() if abs(c) >= 3]
    return len(significant_changes) >= 2
```

---

## 完整轮动分析流程

### 步骤1: 获取所有行业当日表现
```bash
# 获取所有行业表现
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/industry/fundamental/hsi" \
  --params '{"stockCodes": ["H50", "H5010", "H5020", "H5030", "H5040", "H5050", "H5060", "H5070", "H5080", "H5090", "H5100"], "date": "2026-02-24", "metricsList": ["ta", "mc"]}' \
  --columns "industryCode,date,ta,mc" \
  --limit 50
```

### 步骤2: 获取行业资金流向
```bash
# 获取当日和前一日的资金数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/industry/mutual-market/hsi" \
  --params '{"stockCode": "H50", "startDate": "2026-01-01", "endDate": "2026-02-24", "metricsList": ["shareholdingsMoney"]}' \
  --columns "industryCode,date,shareholdingsMoney" \
  --limit 100
```

### 步骤3: 获取市场基准表现
```bash
# 获取恒生指数表现
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/index/fundamental" \
  --params '{"stockCodes": ["HSI"], "date": "2026-02-24", "metricsList": ["mc", "ta"]}' \
  --columns "date,mc,ta"
```

### 步骤4: 计算相对强度和轮动信号（需要脚本处理）
```python
# 使用上述计算函数处理数据
# 输出轮动分析报告
```

---

## 参数说明

- `--suffix`: API 路径
- `--params`: JSON 格式参数
  - `stockCodes`: 行业代码数组
  - `industryCode`: 单个行业代码
  - `date`: 指定日期
  - `startDate/endDate`: 日期范围
  - `metricsList`: 指标列表
- `--columns`: 指定返回字段（推荐使用）
- `--limit`: 限制返回行数

---

## 本 Skill 常用 API

### 核心 API ⭐
- `hk/industry/fundamental/hsi` - 港股行业基本面（最重要）
- `hk/industry/mutual-market/hsi` - 港股行业南向资金（最重要）
- `hk/index/fundamental` - 港股指数基本面（市场基准）

### 辅助 API
- `hk/industry` - 行业分类信息
- `hk/company` - 港股公司信息
- `hk/company/industries` - 个股行业归属

---

## 数据更新频率

- **行业表现**: 每日更新
- **资金流向**: 每日更新（T+1）
- **估值数据**: 每日更新
- **历史数据**: 5年以上

---

## 缺失数据说明

以下数据理杏仁API无法直接提供，需要通过计算或外部数据源补充：

### 1. 实时行业表现
- **问题**: 无法获取盘中实时数据
- **替代方案**: 使用日度数据进行分析

### 2. 机构持仓明细
- **问题**: 无法获取机构行业配置明细
- **替代方案**: 使用南向资金作为参考

### 3. 行业轮动历史模式
- **问题**: 需要自行分析历史数据识别模式
- **替代方案**: 使用历史数据进行统计分析

### 4. 行业景气度指标
- **问题**: 无法直接获取行业景气度数据
- **替代方案**: 通过财务数据和估值推算

### 5. 政策影响因子
- **问题**: 无法量化政策对行业的影响
- **替代方案**: 结合新闻和研报进行定性分析

---

## 使用示例

### 示例1: 识别当前强势行业

```bash
# 1. 获取所有行业表现
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/industry/fundamental/hsi" \
  --params '{"stockCodes": ["H50", "H5010", "H5020", "H5030", "H5040", "H5050", "H5060", "H5070", "H5080", "H5090", "H5100"], "date": "2026-02-24", "metricsList": ["ta"]}' \
  --columns "industryCode,ta" \
  --limit 50

# 2. 获取行业名称
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/industry" \
  --params '{"source": "hsi"}' \
  --columns "industryCode,industryName" \
  --limit 50

# 3. 排序并输出TOP5强势行业（需要脚本处理）
# 输出示例：
# 1. 科技板块: +3.2%
# 2. 医疗保健: +2.8%
# 3. 消费品: +2.1%
# 4. 金融板块: +1.5%
# 5. 工业板块: +1.2%
```

### 示例2: 分析行业资金轮动

```bash
# 1. 获取近5日行业资金数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/industry/mutual-market/hsi" \
  --params '{"stockCode": "H50", "startDate": "2026-01-01", "endDate": "2026-02-24", "metricsList": ["shareholdingsMoney"]}' \
  --columns "industryCode,date,shareholdingsMoney" \
  --limit 250

# 2. 计算每日净流入（需要脚本处理）
# 3. 识别资金流入和流出行业
# 输出示例：
# 净流入行业:
# • 科技板块: +68.5亿 (持续流入)
# • 医疗保健: +32.1亿 (持续流入)
# 
# 净流出行业:
# • 地产板块: -25.3亿 (持续流出)
# • 公用事业: -12.6亿 (资金撤离)
```

### 示例3: 计算相对强度排名

```bash
# 1. 获取行业表现
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/industry/fundamental/hsi" \
  --params '{"stockCodes": ["H50", "H5010", "H5020", "H5030", "H5040", "H5050", "H5060", "H5070", "H5080", "H5090", "H5100"], "date": "2026-02-24", "metricsList": ["mc", "ta"]}' \
  --columns "industryCode,mc,ta" \
  --limit 50

# 2. 获取市场基准
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/index/fundamental" \
  --params '{"stockCodes": ["HSI"], "date": "2026-02-24", "metricsList": ["mc", "ta"]}' \
  --columns "mc,ta"

# 3. 计算相对强度（需要脚本处理）
# 相对强度 = 行业涨跌幅 / 市场涨跌幅
# 输出示例：
# 1. 科技板块: 相对强度 1.78 (强势)
# 2. 医疗保健: 相对强度 1.56 (强势)
# 3. 金融板块: 相对强度 0.83 (弱势)
```

### 示例4: 生成配置建议

```bash
# 1. 获取行业综合数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/industry/fundamental/hsi" \
  --params '{"stockCodes": ["H50", "H5010", "H5020", "H5030", "H5040", "H5050", "H5060", "H5070", "H5080", "H5090", "H5100"], "date": "2026-02-24", "metricsList": ["mc", "ta", "pe_ttm.mcw", "pe_ttm.y10.mcw.cvpos"]}' \
  --columns "industryCode,mc,ta,pe_ttm.mcw,pe_ttm.y10.mcw.cvpos" \
  --limit 50

# 2. 获取资金流向
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/industry/mutual-market/hsi" \
  --params '{"stockCode": "H50", "startDate": "2026-01-01", "endDate": "2026-02-24", "metricsList": ["shareholdingsMoney"]}' \
  --columns "industryCode,date,shareholdingsMoney" \
  --limit 100

# 3. 综合分析生成配置建议（需要脚本处理）
# 输出示例：
# 超配建议:
# • 科技板块 (目标权重: 25%)
# • 医疗保健 (目标权重: 15%)
# 
# 低配建议:
# • 地产板块 (目标权重: 5%)
# • 公用事业 (目标权重: 3%)
```

---

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../lixinger-data-query/SKILL.md`

## 相关文档

- **API 文档**: `../../lixinger-data-query/SKILL.md`
- **使用指南**: `../../lixinger-data-query/LLM_USAGE_GUIDE.md`
- **Skill 说明**: `../SKILL.md`

---

**更新日期**: 2026-02-24  
**版本**: v1.0.0
