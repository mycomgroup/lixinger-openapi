# 金融分析项目最佳实践

基于历史 `analysis_*` 项目的经验总结，帮助 AI 更高效地完成金融分析任务。

---

## 📋 常见错误和解决方案

### 0. API 调用错误完整清单（基于 367 个示例测试）

**测试总结**：
- 测试了 367 个 data-queries.md 示例命令
- 发现并修复了 44 种错误类型
- 共修复 208+ 处错误，涉及 78+ 个文件
- 覆盖 A股、港股、美股三大市场的 162 个 API

**最常见的 10 大错误**：
1. **API 路径格式错误**（100+ 处）：使用点号而非斜杠
2. **参数名称错误**（50+ 处）：stockCodes/stockCode 单复数混淆
3. **缺失 metricsList**（30+ 处）：fundamental/fs API 必需参数
4. **无效指标**（25+ 处）：使用 API 不支持的 metrics
5. **缺失 source 参数**（10+ 处）：industry API 必需参数
6. **缺失 type 参数**（8+ 处）：candlestick API 必需参数
7. **API 路径不存在**（6+ 处）：拼写错误或使用错误的 API
8. **港股 fs API 限制**（5+ 处）：仅支持利润表指标
9. **空的 metricsList**（3+ 处）：数组为空但 API 要求至少 1 项
10. **日期过时**（所有文件）：使用 2024 年日期而非 2026 年

本节总结了在测试所有 skills 的 data-queries.md 示例时发现的 44 种 API 调用错误类型。这些错误覆盖了 A股、港股、美股三大市场的 162 个 API。

#### 错误类型 0.1：API 路径格式错误（点号 vs 斜杠）
```bash
# ❌ 错误：使用点号
--suffix "cn.company.dividend"
--suffix "hk.company.candlestick"

# ✅ 正确：使用斜杠
--suffix "cn/company/dividend"
--suffix "hk/company/candlestick"
```
**影响范围**：所有 API  
**修复文件数**：100+ 个 data-queries.md 文件

#### 错误类型 0.2：参数名称错误（单数 vs 复数）

**0.2.1 stockCodes vs stockCode**
```bash
# ❌ 错误：某些 API 只接受单数形式
--params '{"stockCodes": ["00700"]}'  # hk/company/dividend
--params '{"stockCodes": ["000001"]}'  # cn/index/candlestick

# ✅ 正确：使用单数形式
--params '{"stockCode": "00700"}'  # hk/company/dividend
--params '{"stockCode": "000001"}'  # cn/index/candlestick
```
**受影响 API**：
- `hk/company/dividend`
- `cn/index/candlestick`
- `hk/index/mutual-market`
- `hk/company/industries`

**0.2.2 industryCode vs stockCodes/stockCode**
```bash
# ❌ 错误：使用 industryCode
--params '{"industryCode": "H50"}'  # hk/industry/fundamental/hsi
--params '{"industryCode": "H50"}'  # hk/industry/mutual-market/hsi

# ✅ 正确：使用 stockCodes 或 stockCode
--params '{"stockCodes": ["H50"]}'  # hk/industry/fundamental/hsi
--params '{"stockCode": "H50"}'     # hk/industry/mutual-market/hsi
```
**受影响 API**：
- `hk/industry/fundamental/hsi`
- `hk/industry/mutual-market/hsi`

**0.2.3 indexCode vs stockCode**
```bash
# ❌ 错误：使用 indexCode
--params '{"indexCode": "HK001"}'  # hk/index/mutual-market

# ✅ 正确：使用 stockCode
--params '{"stockCode": "HK001"}'  # hk/index/mutual-market
```
**受影响 API**：
- `hk/index/mutual-market`
- `hk/index/fundamental`

#### 错误类型 0.3：缺失必需参数

**0.3.1 metricsList 参数**
```bash
# ❌ 错误：缺少 metricsList
--params '{"stockCodes": ["600519"], "date": "2026-02-24"}'
# Error: "metricsList" is required

# ✅ 正确：添加 metricsList
--params '{"stockCodes": ["600519"], "date": "2026-02-24", "metricsList": ["pe_ttm", "pb", "dyr"]}'
```
**受影响 API**：
- `cn/company/fundamental/non_financial`
- `cn/company/fs/non_financial`
- `cn/index/fundamental`
- `hk/company/fundamental/non_financial`
- `hk/index/fundamental`
- `us/index/fundamental`

**0.3.2 source 参数**
```bash
# ❌ 错误：缺少 source
--params '{"level": "one"}'
# Error: "source" is required

# ✅ 正确：添加 source
--params '{"source": "sw", "level": "one"}'  # A股
--params '{"source": "hsi"}'                  # 港股
```
**受影响 API**：
- `cn/industry`
- `hk/industry`

**0.3.3 type 参数**
```bash
# ❌ 错误：缺少 type
--params '{"stockCode": "00700", "startDate": "2026-01-01"}'
# Error: "type" is required

# ✅ 正确：添加 type
--params '{"stockCode": "00700", "type": "normal", "startDate": "2026-01-01"}'
```
**受影响 API**：
- `cn/index/candlestick`
- `hk/company/candlestick`

**0.3.4 stockCodes 参数**
```bash
# ❌ 错误：缺少 stockCodes
--params '{"date": "2026-02-24", "metricsList": ["pe_ttm.mcw"]}'
# Error: "stockCodes" is required

# ✅ 正确：添加 stockCodes
--params '{"stockCodes": ["H50"], "date": "2026-02-24", "metricsList": ["pe_ttm.mcw"]}'
```
**受影响 API**：
- `hk/industry/fundamental/hsi`
- `hk/index/fundamental`

**0.3.5 areaCode 参数（宏观数据）**
```bash
# ❌ 错误：缺少 areaCode
--params '{"startDate": "2025-02-01"}'
# Error: "areaCode" is required

# ✅ 正确：添加 areaCode
--params '{"areaCode": "cn", "startDate": "2025-02-01", "metricsList": ["m.m0.t", "m.m1.t"]}'
```
**受影响 API**：
- `macro/money-supply`
- `macro/gdp`
- `macro/cpi`
- `macro/ppi`

#### 错误类型 0.4：无效指标（metricsList）

**0.4.1 A股 fundamental API 无效指标**
```bash
# ❌ 错误：使用不支持的指标
--params '{"metricsList": ["roe_ttm", "roa_ttm"]}'
# Error: (roe_ttm,roa_ttm) are invalid price metrics

# ✅ 正确：使用支持的指标
--params '{"metricsList": ["pe_ttm", "pb", "dyr", "mc"]}'
```
**cn/company/fundamental/non_financial 支持的指标**：
- 估值指标：`pe_ttm`, `pb`, `ps_ttm`, `pcf_ttm`, `dyr`
- 市场指标：`mc` (市值), `ta` (成交额), `tr` (换手率)
- 不支持：`roe`, `roa`, `roe_ttm`, `roa_ttm` 等财务指标

**0.4.2 港股 fundamental API 无效指标**
```bash
# ❌ 错误：使用不支持的指标
--params '{"metricsList": ["pe", "ps", "roe", "roa", "roe_ttm", "roa_ttm"]}'
# Error: (pe,ps,roe,roa,roe_ttm,roa_ttm) are invalid price metrics

# ✅ 正确：使用支持的指标
--params '{"metricsList": ["pe_ttm", "pb", "ps_ttm", "dyr", "mc"]}'
```
**hk/company/fundamental/non_financial 支持的指标**：
- 估值指标：`pe_ttm`, `pb`, `ps_ttm`, `pcf_ttm`, `dyr`
- 市场指标：`mc`, `ta`, `tr`
- 不支持：`pe`, `ps`, `roe`, `roa`, `roe_ttm`, `roa_ttm`

**0.4.3 港股 industry API 无效指标**
```bash
# ❌ 错误：使用不支持的指标
--params '{"metricsList": ["cp", "cpc"]}'
# Error: (cp,cpc) are invalid price metrics

# ✅ 正确：使用支持的指标
--params '{"metricsList": ["pe_ttm.mcw", "pb.mcw", "mc", "ta"]}'
```
**hk/industry/fundamental/hsi 不支持的指标**：
- `cp` (收盘价)
- `cpc` (涨跌幅)
- 建议使用：`pe_ttm.mcw`, `pb.mcw`, `mc`, `ta`

**0.4.4 指标格式要求（.mcw 后缀）**
```bash
# ❌ 错误：缺少后缀
--params '{"metricsList": ["pe_ttm", "pb", "dyr"]}'  # 指数 API

# ✅ 正确：添加 .mcw 后缀
--params '{"metricsList": ["pe_ttm.mcw", "pb.mcw", "dyr.mcw"]}'
```
**需要后缀的 API**：
- `cn/index/fundamental`
- `hk/index/fundamental`
- `us/index/fundamental`
- `hk/industry/fundamental/hsi`

#### 错误类型 0.5：API 限制和特殊规则

**0.5.1 港股 fs API 仅支持利润表**
```bash
# ❌ 错误：使用资产负债表或现金流量表指标
--params '{"metricsList": ["q.bs.ta.t", "q.cf.ncf_oa.t"]}'
# Error: Invalid metrics

# ✅ 正确：仅使用利润表指标
--params '{"metricsList": ["q.ps.toi.t", "q.ps.np.t", "q.ps.gp_m.t"]}'
```
**hk/company/fs/non_financial 限制**：
- 仅支持：`q.ps.*` (利润表指标)
- 不支持：`q.bs.*` (资产负债表), `q.cf.*` (现金流量表)
- 替代方案：查看原始财报或使用 `hk/company/fundamental/non_financial`

**0.5.2 批量查询限制**
```bash
# ❌ 错误：某些 API 使用 startDate 时只能查询一个代码
--params '{"stockCodes": ["000300", "000905"], "startDate": "2026-01-01"}'
# Error: "stockCodes" must contain 1 items

# ✅ 正确：使用循环查询
for code in 000300 000905; do
  python3 query_tool.py --params "{\"stockCodes\": [\"${code}\"], \"startDate\": \"2026-01-01\"}" ...
done
```
**受影响 API**：
- `cn/index/fundamental` (使用 startDate 时)
- `hk/industry/fundamental/hsi` (使用 startDate 时)

**0.5.3 JSON 占位符错误**
```bash
# ❌ 错误：使用 ... 占位符
--params '{"stockCodes": ["00700", ...]}'
# Error: Invalid JSON

# ✅ 正确：使用实际值或添加 --limit
--params '{"stockCodes": ["00700", "00941", "01299"]}' --limit 20
```

#### 错误类型 0.6：API 路径拼写错误

**0.6.1 constituents 拼写错误**
```bash
# ❌ 错误：双写 's'
--suffix "hk/index/constituentss"

# ✅ 正确：单个 's'
--suffix "hk/index/constituents"
```

**0.6.2 API 路径不存在**
```bash
# ❌ 错误：使用不存在的 API
--suffix "cn/company/revenue-structure"
--suffix "hk/industry/candlestick/hsi"

# ✅ 正确：使用正确的 API
--suffix "cn/company/operation-revenue-constitution"
--suffix "hk/industry/fundamental/hsi"  # 使用 fundamental 代替 candlestick
```

**0.6.3 major-shareholder API 路径**
```bash
# ❌ 错误：路径不完整
--suffix "cn/company/major-shareholder-change"

# ✅ 正确：完整路径
--suffix "cn/company/major-shareholders-shares-change"
```

#### 错误类型 0.7：日期参数问题

**0.7.1 使用过时日期**
```bash
# ❌ 错误：使用 2024 年日期（现在是 2026 年）
--params '{"date": "2024-12-31"}'

# ✅ 正确：使用最近日期
--params '{"date": "2026-02-25"}'
--params '{"startDate": "2026-02-01"}'
```

**0.7.2 日期范围过大**
```bash
# ❌ 错误：查询过多历史数据
--params '{"startDate": "2010-01-01"}'  # 16年数据

# ✅ 正确：限制日期范围
--params '{"startDate": "2025-01-01"}' --limit 100
```

---

### 错误类型总结表

| 错误类型 | 受影响 API 数量 | 修复文件数 | 主要市场 |
|---------|---------------|-----------|---------|
| API 路径格式（点号→斜杠） | 所有 API | 100+ | A股/港股/美股 |
| 参数名称错误 | 10+ | 30+ | 主要港股 |
| 缺失必需参数 | 20+ | 50+ | A股/港股/美股 |
| 无效指标 | 15+ | 40+ | 主要港股 |
| API 限制 | 5+ | 20+ | 港股 |
| 路径拼写错误 | 5+ | 10+ | A股/港股 |
| 日期问题 | 所有 API | 100+ | A股/港股/美股 |

**总计**：33 种错误类型，185+ 处修复，70+ 个文件

---

### 1. API 调用错误（详细案例）

#### 错误 1.1：日期参数过时
```bash
# ❌ 错误：使用过时日期
--params '{"date": "2024-12-31"}'

# ✅ 正确：使用最近日期
--params '{"date": "2026-02-24"}'
--params '{"startDate": "2026-02-20"}'
```

**教训**：
- 永远使用最近的日期（当前月份或上个月）
- 避免使用超过3个月的历史日期
- 数据过时会导致分析结果无意义

#### 错误 1.2：API 路径格式错误
```bash
# ❌ 错误：使用点号
--suffix "cn.company.dividend"

# ✅ 正确：使用斜杠
--suffix "cn/company/dividend"
```

#### 错误 1.3：stockCodes 参数错误
```bash
# ❌ 错误：多个股票代码（某些 API 不支持）
--params '{"stockCodes": ["000300", "000905", "000852"]}'
# Error: "stockCodes" must contain 1 items

# ✅ 正确：单个查询或循环查询
for code in 000300 000905 000852; do
  python3 query_tool.py --params "{\"stockCodes\": [\"${code}\"]}" ...
done
```

**教训**：
- 使用 API 前必须 grep 查看文档
- 确认 API 是否支持批量查询
- 某些 API（如 cn/index/fundamental）使用 startDate 时只能传一个代码

#### 错误 1.4：metricsList 参数错误
```bash
# ❌ 错误：使用不存在的指标
--params '{"metricsList": ["roe_ttm"]}'
# Error: (roe_ttm) are invalid price metrics

# ✅ 正确：查看 API 文档确认支持的指标
cat skills/lixinger-data-query/api_new/api-docs/cn_company_fundamental_non_financial.md
--params '{"metricsList": ["pe_ttm", "pb", "dyr"]}'
```

**教训**：
- 不同 API 支持的指标不同
- fundamental API 需要 metricsList
- fs（财务）API 需要不同的 metricsList

#### 错误 1.5：数据为空
```bash
# 查询结果为空，可能原因：
# 1. 日期参数错误（date 不存在数据）
# 2. 股票代码错误
# 3. API 路径错误

# 解决方案：使用 startDate + limit
--params '{"startDate": "2026-02-20", "limit": 1}'
```

---

### 2. 数据处理错误

#### 错误 2.1：CSV 数据追加时重复表头
```bash
# ❌ 错误：直接追加会包含表头
python3 query_tool.py ... >> data.csv
python3 query_tool.py ... >> data.csv  # 第二次会有重复表头

# ✅ 正确：使用 tail -n +2 跳过表头
python3 query_tool.py ... > data.csv  # 第一次
python3 query_tool.py ... | tail -n +2 >> data.csv  # 后续追加
```

#### 错误 2.2：数据文件路径错误
```bash
# ❌ 错误：忘记创建目录
python3 query_tool.py ... > data/stocks.csv
# Error: No such file or directory

# ✅ 正确：先创建目录
mkdir -p analysis_xxx/data
python3 query_tool.py ... > analysis_xxx/data/stocks.csv
```

---

### 3. 项目结构错误

#### 错误 3.1：没有创建项目文件夹
```bash
# ❌ 错误：直接在根目录操作
python3 query_tool.py ... > index_data.csv

# ✅ 正确：创建项目文件夹
PROJECT="analysis_$(date +%Y%m%d_%H%M%S)_主题"
mkdir -p ${PROJECT}/{data,output,scripts}
```

#### 错误 3.2：文件命名不规范
```bash
# ❌ 错误：文件名不清晰
data.csv
result.csv
output.md

# ✅ 正确：使用描述性文件名
data/index_valuation.csv
data/quality_stocks.csv
output/allocation_plan.md
```

---

## ✅ 最佳实践

### 1. 项目初始化流程

```bash
# 第一步：创建项目文件夹
PROJECT="analysis_$(date +%Y%m%d_%H%M%S)_主题关键词"
mkdir -p ${PROJECT}/{data,output,scripts}

# 第二步：创建 README.md
cat > ${PROJECT}/README.md << 'EOF'
# 项目标题

## 分析目标
[描述分析目标]

## 使用 Skills
- skills/China-market/xxx/

## 执行时间
$(date +%Y-%m-%d\ %H:%M:%S)

## 数据来源
- 理杏仁 API
- 分析日期：$(date +%Y-%m-%d)
EOF
```

### 2. 数据获取流程

```bash
# 第一步：grep 查看 API 文档（必须！）
cat skills/lixinger-data-query/api_new/api-docs/cn_index_fundamental.md

# 第二步：确认参数格式
# - 使用斜杠而非点号
# - 确认是否支持批量查询
# - 确认 metricsList 支持的指标

# 第三步：执行查询（使用最近日期）
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/index/fundamental" \
  --params '{"stockCodes": ["000300"], "startDate": "2026-02-20", "metricsList": ["pe_ttm.mcw", "pb.mcw"]}' \
  --limit 1 \
  > ${PROJECT}/data/index_valuation.csv

# 第四步：验证数据
cat ${PROJECT}/data/index_valuation.csv
```

### 3. 批量查询流程

```bash
# 方法 1：循环查询（推荐）
for code in 000300 000905 000852; do
  python3 query_tool.py \
    --params "{\"stockCodes\": [\"${code}\"], \"startDate\": \"2026-02-20\"}" \
    ... | tail -n +2 >> data.csv  # 跳过表头
done

# 方法 2：先查询第一个（保留表头）
python3 query_tool.py --params '{"stockCodes": ["000300"]}' ... > data.csv
# 再查询其他（跳过表头）
for code in 000905 000852; do
  python3 query_tool.py --params "{\"stockCodes\": [\"${code}\"]}" ... | tail -n +2 >> data.csv
done
```

### 4. 数据分析流程

```python
#!/usr/bin/env python3
"""
分析脚本模板
"""
import pandas as pd

def load_data():
    """加载数据"""
    try:
        df = pd.read_csv('data/xxx.csv')
        print(f"✅ 数据加载成功：{len(df)} 行")
        return df
    except FileNotFoundError:
        print("❌ 数据文件不存在")
        return None
    except Exception as e:
        print(f"❌ 数据加载失败：{e}")
        return None

def analyze_data(df):
    """分析数据"""
    if df is None or len(df) == 0:
        print("❌ 数据为空，无法分析")
        return
    
    # 数据清洗
    df['stockCode'] = df['stockCode'].astype(str).str.strip()
    
    # 分析逻辑
    for _, row in df.iterrows():
        code = row['stockCode']
        pe = row['pe_ttm.mcw']
        print(f"{code}: PE={pe:.2f}")

def main():
    """主函数"""
    print("=" * 70)
    print("数据分析报告")
    print("=" * 70)
    
    df = load_data()
    analyze_data(df)
    
    print("=" * 70)
    print("分析完成")
    print("=" * 70)

if __name__ == '__main__':
    main()
```

### 5. 报告生成流程

```bash
# 使用 fsWrite 创建报告
# 优点：
# - 一次性写入完整内容
# - 避免追加时的格式问题
# - 便于版本控制

# 报告结构：
# 1. 标题和元信息
# 2. 市场环境分析
# 3. 配置方案
# 4. 风险控制
# 5. 执行建议
# 6. 监控指标
```

---

## 📊 数据质量检查清单

### 查询前检查
- [ ] 已 grep 查看 API 文档
- [ ] 确认 API 路径格式（斜杠）
- [ ] 确认参数格式（stockCodes 单数/复数）
- [ ] 使用最近日期（2026-02-xx）
- [ ] 确认 metricsList 支持的指标

### 查询后检查
- [ ] 数据文件不为空
- [ ] 数据有表头
- [ ] 数据行数合理（>0）
- [ ] 数值字段无异常（非 NaN）
- [ ] 日期字段正确

### 分析前检查
- [ ] 数据文件路径正确
- [ ] 数据格式正确（CSV）
- [ ] 数据可以正常加载
- [ ] 数据字段完整

---

## 🔄 项目复用建议

### 1. 参考历史项目

**查找相似项目**：
```bash
# 查看所有历史项目
ls -d analysis_*

# 查看项目 README
cat analysis_xxx/README.md

# 查看项目脚本
ls analysis_xxx/scripts/
```

**可复用的项目**：
- `analysis_20260225_115511_portfolio_allocation/`：资产配置方案（100万）
- `analysis_20260225_141848_10m_portfolio/`：资产配置方案（1000万）
- `analysis_20260225_132632_aggressive_portfolio/`：积极型配置
- `analysis_20260225_114923_maotai_dividend/`：分红数据查询

### 2. 复用脚本

**数据获取脚本**：
```bash
# 复制脚本到新项目
cp analysis_xxx/scripts/01_fetch_index_valuation.sh ${PROJECT}/scripts/

# 修改参数
# - 更新日期
# - 更新股票代码
# - 更新输出路径
```

**分析脚本**：
```bash
# 复制 Python 分析脚本
cp analysis_xxx/scripts/04_comprehensive_analysis.py ${PROJECT}/scripts/

# 修改逻辑
# - 更新数据文件路径
# - 更新分析逻辑
# - 更新输出格式
```

### 3. 复用报告模板

**配置方案模板**：
```markdown
# 标题

## 一、市场环境分析
[指数估值、行业分析]

## 二、配置策略
[配置原则、配置结构]

## 三、具体配置方案
[详细配置表格]

## 四、风险控制要点
[风险识别、控制措施]

## 五、执行建议
[建仓策略、交易要点]

## 六、动态调整机制
[再平衡、止盈止损]

## 七、监控指标
[日/周/月/季度监控]
```

---

## 🎯 效率提升技巧

### 1. 使用 --columns 过滤字段

```bash
# ❌ 低效：返回所有字段（浪费 token）
python3 query_tool.py --suffix "cn/company" --params '{"stockCodes": ["600519"]}'

# ✅ 高效：只返回需要的字段（节省 30-40% token）
python3 query_tool.py \
  --suffix "cn/company" \
  --params '{"stockCodes": ["600519"]}' \
  --columns "stockCode,cnName,industryName"
```

### 2. 使用 --limit 限制行数

```bash
# ❌ 低效：返回所有历史数据
python3 query_tool.py --params '{"startDate": "2020-01-01"}'

# ✅ 高效：只返回最近的数据
python3 query_tool.py --params '{"startDate": "2026-02-01"}' --limit 10
```

### 3. 使用 --row-filter 过滤数据

```bash
# ❌ 低效：查询后再过滤
python3 query_tool.py ... > data.csv
grep "条件" data.csv > filtered.csv

# ✅ 高效：查询时直接过滤
python3 query_tool.py ... --row-filter "dyr>0.05"
```

### 4. 批量操作使用脚本

```bash
# ❌ 低效：手动执行多次
python3 query_tool.py --params '{"stockCodes": ["600519"]}' ...
python3 query_tool.py --params '{"stockCodes": ["601318"]}' ...
python3 query_tool.py --params '{"stockCodes": ["600036"]}' ...

# ✅ 高效：使用循环
for code in 600519 601318 600036; do
  python3 query_tool.py --params "{\"stockCodes\": [\"${code}\"]}" ...
done
```

---

## 📝 文档规范

### README.md 必备内容

```markdown
# 项目标题

## 分析目标
[明确的分析目标]

## 投资者画像（如适用）
- 资金规模
- 风险偏好
- 投资期限

## 使用 Skills
- skills/China-market/xxx/

## 执行时间
YYYY-MM-DD HH:MM:SS

## 数据来源
- 理杏仁 API
- 分析日期：YYYY-MM-DD

## 执行记录
### 数据文件
- data/xxx.csv: 说明

### 代码脚本
- scripts/xxx.sh: 说明

### 输出报告
- output/xxx.md: 说明

## 遇到的问题和解决方案
[记录错误和解决方法，便于后续参考]
```

### 报告文件命名规范

```
output/
├── allocation_plan.md        # 配置方案
├── action_checklist.md       # 执行清单
├── summary.md                # 一页总结
└── risk_analysis.md          # 风险分析
```

---

## 🚨 常见陷阱

### 1. 不要记忆 API 列表
```bash
# ❌ 错误：凭记忆使用 API
python3 query_tool.py --suffix "cn/company/xxx"

# ✅ 正确：每次都 grep 查看文档
grep -r "关键词" skills/lixinger-data-query/api_new/api-docs/
cat skills/lixinger-data-query/api_new/api-docs/xxx.md
```

### 2. 不要使用过时日期
```bash
# ❌ 错误：使用 2024 年日期（现在是 2026 年）
--params '{"date": "2024-12-31"}'

# ✅ 正确：使用最近日期
--params '{"date": "2026-02-25"}'
--params '{"startDate": "2026-02-01"}'
```

### 3. 不要忽略错误信息
```bash
# 如果查询失败，仔细阅读错误信息：
# - ValidationError: 参数格式错误
# - Api was not found: API 路径错误
# - invalid metrics: 指标不支持

# 根据错误信息调整参数，不要盲目重试
```

### 4. 不要过度查询
```bash
# ❌ 错误：查询大量历史数据
--params '{"startDate": "2010-01-01"}'  # 16年数据

# ✅ 正确：只查询需要的数据
--params '{"startDate": "2025-01-01"}' --limit 100
```

---

## 📚 学习资源

### 必读文档
1. `skills/lixinger-data-query/SKILL.md` - 数据查询工具总览
2. `skills/lixinger-data-query/LLM_USAGE_GUIDE.md` - LLM 使用指南
3. `skills/lixinger-data-query/EXAMPLES.md` - 查询示例
4. `.kiro/steering/lixinger-skills.md` - 金融分析技能包

### 参考项目
1. `analysis_20260225_115511_portfolio_allocation/` - 完整的配置方案流程
2. `analysis_20260225_141848_10m_portfolio/` - 大额资金配置
3. `analysis_20260225_132632_aggressive_portfolio/` - 积极型配置

### API 文档
```bash
# 查看所有 API 文档
ls skills/lixinger-data-query/api_new/api-docs/

# 常用 API
cat skills/lixinger-data-query/api_new/api-docs/cn_index_fundamental.md
cat skills/lixinger-data-query/api_new/api-docs/cn_company_fundamental_non_financial.md
cat skills/lixinger-data-query/api_new/api-docs/cn_company_dividend.md
```

---

## 🎓 总结

### 核心原则
1. **先 grep 后查询**：使用 API 前必须查看文档
2. **使用最近日期**：避免使用过时数据
3. **创建项目文件夹**：一个对话 = 一个项目
4. **记录执行过程**：README.md 记录问题和解决方案
5. **参考历史项目**：复用成功的脚本和模板

### 效率提升
1. 使用 `--columns` 过滤字段（节省 30-40% token）
2. 使用 `--limit` 限制行数
3. 使用循环批量查询
4. 复用历史项目的脚本

### 质量保证
1. 查询前检查参数格式
2. 查询后验证数据质量
3. 分析前检查数据完整性
4. 报告中记录数据来源和日期

---

## 📖 附录：API 错误速查表

### A股常见错误

| API | 常见错误 | 正确用法 |
|-----|---------|---------|
| cn/company/fundamental/non_financial | 缺少 metricsList | 添加 `"metricsList": ["pe_ttm", "pb", "dyr"]` |
| cn/company/fs/non_financial | 缺少 metricsList | 添加 `"metricsList": ["q.ps.toi.t", "q.ps.np.t"]` |
| cn/index/fundamental | 缺少 metricsList 和 .mcw 后缀 | 使用 `"metricsList": ["pe_ttm.mcw", "pb.mcw"]` |
| cn/index/candlestick | 缺少 type 参数 | 添加 `"type": "normal"` |
| cn/industry | 缺少 source 参数 | 添加 `"source": "sw"` |
| cn/company/operation-revenue-constitution | 路径错误 | 不是 revenue-structure |

### 港股常见错误

| API | 常见错误 | 正确用法 |
|-----|---------|---------|
| hk/company/dividend | 使用 stockCodes | 改为 `"stockCode": "00700"` (单数) |
| hk/company/fundamental/non_financial | 使用 pe/ps/roe/roa | 改为 `pe_ttm`, `ps_ttm` (不支持 roe/roa) |
| hk/company/fs/non_financial | 使用 bs/cf 指标 | 仅支持 `q.ps.*` (利润表) |
| hk/company/candlestick | 缺少 type 参数 | 添加 `"type": "normal"` |
| hk/industry/fundamental/hsi | 使用 industryCode | 改为 `"stockCodes": ["H50"]` |
| hk/industry/fundamental/hsi | 使用 cp/cpc 指标 | 改为 `pe_ttm.mcw`, `pb.mcw` |
| hk/index/fundamental | 使用 indexCode | 改为 `"stockCodes": ["HK001"]` |
| hk/index/mutual-market | 使用 indexCode | 改为 `"stockCode": "HK001"` (单数) |
| hk/index/constituents | 路径拼写错误 | 不是 constituentss (双s) |

### 美股常见错误

| API | 常见错误 | 正确用法 |
|-----|---------|---------|
| us/index/fundamental | 缺少 metricsList 和 .mcw 后缀 | 使用 `"metricsList": ["pe_ttm.mcw", "pb.mcw"]` |
| us/company/fs/non_financial | 缺少 metricsList | 添加财务指标列表 |

### 宏观数据常见错误

| API | 常见错误 | 正确用法 |
|-----|---------|---------|
| macro/money-supply | 缺少 areaCode 和 metricsList | 添加 `"areaCode": "cn", "metricsList": ["m.m0.t"]` |
| macro/gdp | 缺少 areaCode 和 metricsList | 添加 `"areaCode": "cn", "metricsList": ["q.gdp.t"]` |
| macro/cpi | 缺少 areaCode 和 metricsList | 添加 `"areaCode": "cn", "metricsList": ["cpi"]` |

---

## 🔍 快速诊断指南

遇到 API 错误时，按以下顺序检查：

1. **ValidationError: "xxx" is required**
   - 检查是否缺少必需参数（metricsList, source, type, stockCodes, areaCode）
   - grep 查看 API 文档确认所有必需参数

2. **ValidationError: (xxx) are invalid metrics**
   - 检查 metricsList 中的指标是否支持
   - 港股 fundamental API 不支持 roe/roa
   - 港股 industry API 不支持 cp/cpc
   - 指数 API 需要 .mcw 后缀

3. **Api was not found**
   - 检查 API 路径格式（使用斜杠而非点号）
   - 检查路径拼写（constituents 不是 constituentss）
   - 检查 API 是否存在（某些 API 不存在如 hk/industry/candlestick）

4. **ValidationError: "stockCodes" must contain 1 items**
   - 某些 API 使用 startDate 时只能查询一个代码
   - 使用循环分别查询每个代码

5. **数据为空**
   - 检查日期是否过时（使用 2026 年而非 2024 年）
   - 检查股票代码是否正确
   - 使用 startDate 而非 date 参数

6. **Command timeout**
   - 添加 --limit 参数限制返回行数
   - 缩小日期范围
   - 使用 --columns 过滤字段

---

## 📚 参考资源

### 测试工具
- `test_data_queries_examples.py`: 自动化测试所有 data-queries.md 示例
- `DATA_QUERIES_FIX_SUMMARY.md`: 详细的错误修复记录

### API 文档位置
```bash
# A股 API 文档
ls skills/lixinger-data-query/api_new/api-docs/cn_*.md

# 港股 API 文档
ls skills/lixinger-data-query/api_new/api-docs/hk_*.md

# 美股 API 文档
ls skills/lixinger-data-query/api_new/api-docs/us_*.md

# 宏观数据 API 文档
ls skills/lixinger-data-query/api_new/api-docs/macro_*.md
```

### 查找 API 文档
```bash
# 按关键词搜索
grep -r "分红" skills/lixinger-data-query/api_new/api-docs/
grep -r "估值" skills/lixinger-data-query/api_new/api-docs/
grep -r "财务" skills/lixinger-data-query/api_new/api-docs/

# 查看具体 API 文档
cat skills/lixinger-data-query/api_new/api-docs/cn_company_fundamental_non_financial.md
cat skills/lixinger-data-query/api_new/api-docs/hk_company_fundamental_non_financial.md
```

---

**最后更新**：2026-02-26  
**维护者**：AI Assistant  
**用途**：指导 AI 更高效地完成金融分析任务  
**测试覆盖**：367 个示例命令，33 种错误类型，185+ 处修复
