---
inclusion: always
---

# 理杏仁金融分析技能包

你现在可以访问一个完整的金融量化分析技能包，基于理杏仁开放平台 API，支持 A股、港股、美股三大市场。

## 📊 技能包概览

- **116 个专业分析 Skills**：66 个 A股 + 13 个港股 + 37 个美股
- **162 个理杏仁 API**：覆盖基本面、财务、行情、宏观等数据
- **1000+ AkShare 接口**：补充特殊数据源
- **三级优先级体系**：Skills → 理杏仁 API → AkShare

## 🔍 如何查找 Skills

**不要记忆技能列表！使用 grep 动态查找：**

```bash
# 按关键词搜索 A股 skills
ls skills/China-market/ | grep -i "关键词"

# 按关键词搜索港股 skills
ls skills/HK-market/ | grep -i "关键词"

# 按关键词搜索美股 skills
ls skills/US-market/ | grep -i "关键词"

# 示例：查找分红相关 skills
ls skills/China-market/ | grep -i "dividend"
# 输出：dividend-corporate-action-tracker, high-dividend-strategy
```

**常用关键词映射**：
- 分红/股息 → dividend, yield
- 估值 → valuation, undervalued
- 风险 → risk, monitor
- 资金流向 → flow, fund
- 事件驱动 → event, disclosure, notice
- 组合管理 → portfolio, rebalancing
- 行业板块 → industry, sector, board

---

## � 项目工作目录管理

**对于复杂的市场分析任务，必须创建专门的项目文件夹来组织工作：**

### 何时创建项目文件夹

当遇到以下情况时，在当前工作目录创建项目子文件夹：

- 使用市场分析 Skills 进行复杂分析
- 需要下载和保存多个数据文件
- 需要生成分析报告和图表
- 需要保存分析方案和执行记录

### 项目文件夹命名规范

```bash
# 格式：analysis_YYYYMMDD_主题关键词
# 示例：
analysis_20260225_high_dividend_screening/
analysis_20260225_event_study_600089/
analysis_20260225_market_overview/
```

### 项目文件夹结构

```
analysis_YYYYMMDD_主题/
├── README.md              # 分析方案和执行记录
├── data/                  # 原始数据文件
│   ├── stock_list.csv
│   ├── dividend_data.csv
│   └── price_data.csv
├── analysis/              # 分析脚本和中间结果
│   └── analysis.py
├── output/                # 最终输出报告
│   └── report.md
└── logs/                  # 执行日志
    └── execution.log
```

### 创建项目文件夹示例

```bash
# 1. 创建项目文件夹
mkdir -p analysis_20260225_high_dividend/data
mkdir -p analysis_20260225_high_dividend/output

# 2. 创建 README.md 记录分析方案
cat > analysis_20260225_high_dividend/README.md << 'EOF'
# 高股息股票筛选分析

## 分析目标
筛选 A股市场优质高股息股票

## 使用 Skill
- skills/China-market/high-dividend-strategy/

## 数据来源
- 理杏仁 API: cn/company/fundamental/non-financial
- 理杏仁 API: cn/company/dividend

## 执行步骤
1. 查询股息率数据
2. 查询分红历史数据
3. 计算可持续性指标
4. 生成筛选报告

## 执行时间
2026-02-25
EOF

# 3. 下载数据到 data/ 目录
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/dividend" \
  --params '{"stockCode": "600519"}' \
  > analysis_20260225_high_dividend/data/dividend_600519.csv

# 4. 生成报告到 output/ 目录
# (分析完成后将报告保存到这里)
```

---

## 💡 使用方式

### ⚠️ 重要：使用优先级（必须严格遵守）

**三级优先级体系：市场分析 Skills > 数据查询工具 > AkShare 接口**

#### 第一优先级：市场分析 Skills（最优先）

使用 `skills/China-market/`、`skills/HK-market/`、`skills/US-market/` 中的 116 个分析 skills：

- **A股市场**：66 个专业分析 skills（`skills/China-market/`）
- **港股市场**：13 个专业分析 skills（`skills/HK-market/`）
- **美股市场**：37 个专业分析 skills（`skills/US-market/`）

**为什么优先使用**：
- 提供完整的分析方法论和工作流程
- 包含数据获取、分析逻辑、输出模板
- 适合复杂的金融分析任务
- 开箱即用，无需自己编写分析逻辑

**如何查找**：
```bash
# 查找 A股分析 skills
ls skills/China-market/

# 查找港股分析 skills
ls skills/HK-market/

# 查找美股分析 skills
ls skills/US-market/
```

#### 第二优先级：理杏仁数据查询工具（备选）

使用 `skills/lixinger-data-query/` 的 162 个理杏仁 API：

**何时使用**：
- 找不到合适的市场分析 skill
- 需要简单的数据查询
- 需要自定义分析逻辑

**如何使用**：
```bash
# 使用 query_tool.py 查询理杏仁 API
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company.dividend" \
  --params '{"stockCode": "600519"}' \
  --columns "date,dividendPerShare"
```

#### 第三优先级：AkShare 接口（最后备选）

使用 `skills/lixinger-data-query/api_new/akshare_data/` 的 1000+ AkShare 接口：

**何时使用**：
- 市场分析 skills 和理杏仁 API 都无法满足需求
- 需要特殊的数据源（如集思录可转债、东方财富龙虎榜等）

**如何使用**：
```python
import akshare as ak

# 示例：查询可转债数据
bond_cb_jsl_df = ak.bond_cb_jsl(cookie="")
print(bond_cb_jsl_df)
```

### 数据获取（核心）

**所有市场分析 skills 都使用 `query_tool.py` 获取数据**：

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company.dividend" \
  --params '{"stockCode": "600519"}' \
  --columns "date,dividendPerShare,dividendYield" \
  --limit 20
```

**关键参数**：
- `--suffix`: API 路径（参考 `skills/lixinger-data-query/SKILL.md`）
- `--params`: JSON 格式参数
- `--columns`: 指定返回字段（推荐使用，节省 30-40% token）
- `--row-filter`: 过滤条件
- `--limit`: 限制返回行数

### 工作流程（优化版）

当用户提出金融分析问题时，**严格按照以下流程执行**：

#### 步骤 0：判断是否需要创建项目文件夹

如果是复杂的市场分析任务（使用 Skills），创建项目文件夹：

```bash
# 创建项目文件夹
PROJECT_NAME="analysis_$(date +%Y%m%d)_主题关键词"
mkdir -p ${PROJECT_NAME}/{data,output}

# 创建 README.md 记录分析方案
cat > ${PROJECT_NAME}/README.md << EOF
# 分析标题

## 分析目标
[描述分析目标]

## 使用 Skill
- skills/[market]/[skill-name]/

## 数据来源
- [列出使用的 API]

## 执行步骤
1. [步骤1]
2. [步骤2]

## 执行时间
$(date +%Y-%m-%d)
EOF
```

#### 步骤 1：使用 grep 查找合适的 Skill（第一优先级）

**不要浏览技能列表！直接搜索：**

```bash
# A股分析
ls skills/China-market/ | grep -i "关键词"

# 港股分析
ls skills/HK-market/ | grep -i "关键词"

# 美股分析
ls skills/US-market/ | grep -i "关键词"

# 示例：查找高股息相关 skills
ls skills/China-market/ | grep -i "dividend"
# 输出：dividend-corporate-action-tracker, high-dividend-strategy
```

#### 步骤 2：查看 Skill 文档

```bash
# 查看 Skill 说明
cat skills/China-market/high-dividend-strategy/SKILL.md

# 查看数据获取指南
cat skills/China-market/high-dividend-strategy/references/data-queries.md
```

#### 步骤 3：获取数据并保存到项目文件夹

```bash
# 下载数据到项目的 data/ 目录
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/dividend" \
  --params '{"stockCode": "600519"}' \
  --columns "date,dividendPerShare,dividendYield" \
  > ${PROJECT_NAME}/data/dividend_data.csv
```

#### 步骤 4：执行分析并生成报告

- 按照 Skill 的方法论进行分析
- 将最终报告保存到 `${PROJECT_NAME}/output/report.md`

#### 步骤 5：如果找不到合适的 Skill，使用理杏仁 API（第二优先级）

```bash
# 搜索理杏仁 API
grep -r "关键词" skills/lixinger-data-query/api_new/api-docs/

# 查看 API 文档
cat skills/lixinger-data-query/api_new/api-docs/[api_name].md

# 使用 query_tool.py 查询
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company.dividend" \
  --params '{"stockCode": "600519"}' \
  --columns "date,dividendPerShare"
```

#### 步骤 6：如果理杏仁 API 也无法满足，使用 AkShare（第三优先级）

```bash
# 搜索 AkShare 接口
grep -r "关键词" skills/lixinger-data-query/api_new/akshare_data/

# 查看接口文档
cat skills/lixinger-data-query/api_new/akshare_data/[interface_name].md

# 使用 Python 调用
python3 -c "import akshare as ak; print(ak.interface_name())"
```

---

## 🎯 使用示例（优化版）

### 示例 1：高股息股票筛选（完整流程）

**用户问**："帮我筛选一下高股息的股票"

**执行步骤**：

```bash
# 1. 创建项目文件夹
PROJECT="analysis_20260225_high_dividend"
mkdir -p ${PROJECT}/{data,output}

# 2. 使用 grep 查找相关 Skill
ls skills/China-market/ | grep -i "dividend"
# 输出：dividend-corporate-action-tracker, high-dividend-strategy

# 3. 选择 high-dividend-strategy，查看文档
cat skills/China-market/high-dividend-strategy/SKILL.md

# 4. 创建分析方案
cat > ${PROJECT}/README.md << 'EOF'
# 高股息股票筛选分析

## 使用 Skill
- skills/China-market/high-dividend-strategy/

## 筛选标准
- 股息率 ≥ 4%
- 连续分红 ≥ 5年
- 分红率 30%-70%

## 执行时间
2026-02-25
EOF

# 5. 获取数据（示例：查询知名高股息股票）
for code in 601398 601288 600900 601088; do
  python3 skills/lixinger-data-query/scripts/query_tool.py \
    --suffix "cn/company/dividend" \
    --params "{\"stockCode\": \"${code}\"}" \
    > ${PROJECT}/data/dividend_${code}.csv
done

# 6. 按照 Skill 方法论进行分析
# 7. 生成报告保存到 output/report.md
```

### 示例 2：事件研究分析（完整流程）

**用户问**："分析一下特变电工发布业绩预告后股价的表现"

**执行步骤**：

```bash
# 1. 创建项目文件夹
PROJECT="analysis_20260225_event_study_600089"
mkdir -p ${PROJECT}/{data,output}

# 2. 使用 grep 查找相关 Skill
ls skills/China-market/ | grep -i "event"
# 输出：event-driven-detector, event-study

# 3. 选择 event-study，查看文档
cat skills/China-market/event-study/SKILL.md

# 4. 创建分析方案
cat > ${PROJECT}/README.md << 'EOF'
# 特变电工业绩预告事件研究

## 股票代码
600089

## 事件日期
2025-08-21

## 使用 Skill
- skills/China-market/event-study/

## 执行时间
2026-02-25
EOF

# 5. 获取公告数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/announcement" \
  --params '{"stockCode": "600089", "startDate": "2025-08-01", "endDate": "2025-09-30"}' \
  > ${PROJECT}/data/announcements.csv

# 6. 获取股价数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non-financial" \
  --params '{"stockCodes": ["600089"], "startDate": "2025-08-01", "endDate": "2025-09-30", "metricsList": ["sp", "spc", "tv"]}' \
  > ${PROJECT}/data/price_data.csv

# 7. 按照 Skill 方法论进行事件研究分析
# 8. 生成报告保存到 output/report.md
```

### 示例 3：简单数据查询（无需项目文件夹）

**用户问**："查询贵州茅台的基本信息"

**执行步骤**：

```bash
# 简单查询，无需创建项目文件夹
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company" \
  --params '{"stockCodes": ["600519"]}' \
  --columns "stockCode,name,industry"
```

---

## 📍 文件位置

### Skills 目录结构

```
skills/
├── lixinger-data-query/           # 数据查询工具（备选）
│   ├── SKILL.md                   # 主文档（162 个 API 列表）
│   ├── LLM_USAGE_GUIDE.md         # LLM 使用指南
│   ├── EXAMPLES.md                # 查询示例
│   ├── scripts/
│   │   └── query_tool.py          # 查询工具
│   └── api_new/api-docs/          # 162 个 API 文档
│
├── China-market/                  # 66 个 A股分析 skills（首选）
│   ├── dividend-corporate-action-tracker/
│   │   ├── SKILL.md               # Skill 说明
│   │   └── references/
│   │       ├── data-queries.md    # 数据获取指南
│   │       ├── methodology.md     # 方法论
│   │       └── output-template.md # 输出模板
│   └── ... (其他 65 个 skills)
│
├── HK-market/                     # 13 个港股分析 skills（首选）
│   ├── hk-market-overview/
│   │   ├── SKILL.md
│   │   └── references/
│   │       └── data-queries.md
│   └── ... (其他 12 个 skills)
│
└── US-market/                     # 37 个美股分析 skills（首选）
    ├── market-breadth-monitor/
    │   ├── SKILL.md
    │   └── references/
    │       └── data-queries.md
    └── ... (其他 36 个 skills)
```

### 关键文档

1. **API 列表**：`skills/lixinger-data-query/SKILL.md`
   - 包含所有 162 个 API 的列表和说明
   - 仅在找不到合适的分析 skill 时参考

2. **LLM 使用指南**：`skills/lixinger-data-query/LLM_USAGE_GUIDE.md`
   - 详细的调用流程和参数构造技巧

3. **数据获取指南**：
   - A股：`skills/China-market/{skill-name}/references/data-queries.md`
   - 港股：`skills/HK-market/{skill-name}/references/data-queries.md`
   - 美股：`skills/US-market/{skill-name}/references/data-queries.md`

---

## 🔑 环境配置

### Token 配置

确保项目根目录有 `token.cfg` 文件：
```bash
cat token.cfg
# 应该包含有效的理杏仁 API Token
```

### Python 环境

**✅ 无需虚拟环境！**

`query_tool.py` 已经是完全独立的工具：
- 无需 `source .venv/bin/activate`
- 无需 `pip install`
- 直接运行即可

```bash
# 直接运行，无需激活虚拟环境
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company" \
  --params '{"stockCodes": ["600519"]}' \
  --columns "stockCode,name"
```

---

## 💡 重要提示

### 0. 工作流程核心原则（最重要）

**必须严格遵守的执行顺序：**

1. **先 grep 搜索，不要浏览列表**
   ```bash
   ls skills/China-market/ | grep -i "关键词"
   ```

2. **复杂分析必须创建项目文件夹**
   ```bash
   mkdir -p analysis_YYYYMMDD_主题/{data,output}
   ```

3. **数据保存到项目的 data/ 目录**
   ```bash
   python3 ... > ${PROJECT}/data/filename.csv
   ```

4. **报告保存到项目的 output/ 目录**
   ```bash
   # 分析完成后保存到 output/report.md
   ```

### 1. Skill 使用优先级

**三级优先级体系（从高到低）**：

1. **第一优先级：市场分析 Skills**
   - 使用 grep 动态查找，不要记忆列表
   - 提供完整方法论和工作流程
   - **必须优先使用**

2. **第二优先级：理杏仁数据查询工具**
   - 仅在找不到合适 Skill 时使用
   - 需要自己编写分析逻辑

3. **第三优先级：AkShare 接口**
   - 仅在前两者都无法满足时使用
   - 用于特殊数据源

### 2. 数据获取原则

- **始终使用 `query_tool.py`**：唯一的数据获取工具
- **使用 `--columns` 过滤字段**：节省 30-40% token
- **数据保存到项目文件夹**：便于管理和复用

### 3. 项目管理原则

- **复杂分析必须创建项目文件夹**
- **简单查询无需项目文件夹**
- **项目命名规范**：`analysis_YYYYMMDD_主题`
- **README.md 记录分析方案**

### 4. 查找技巧

**使用 grep 而不是浏览列表：**

```bash
# 按功能查找
ls skills/China-market/ | grep -i "dividend"    # 分红
ls skills/China-market/ | grep -i "risk"        # 风险
ls skills/China-market/ | grep -i "flow"        # 资金流向
ls skills/China-market/ | grep -i "event"       # 事件驱动
ls skills/China-market/ | grep -i "portfolio"   # 组合管理
```

---

## 📚 相关文档

- **查询工具主文档**：`skills/lixinger-data-query/SKILL.md`
- **LLM 使用指南**：`skills/lixinger-data-query/LLM_USAGE_GUIDE.md`
- **查询示例**：`skills/lixinger-data-query/EXAMPLES.md`
- **API 文档目录**：`skills/lixinger-data-query/api_new/api-docs/`
- **理杏仁官方文档**：https://open.lixinger.com/

---

**版本**: v4.0.0  
**更新日期**: 2026-02-25  
**主要改进**：
- 删除冗长的技能列表，改为动态 grep 查找
- 添加项目工作目录管理机制
- 优化工作流程，强调先搜索再执行
- 简化文档结构，提高可读性

**技能总数**: 116 个市场分析 Skills + 162 个理杏仁 API + 1000+ AkShare 接口  
**数据源**: 理杏仁开放平台 + AkShare  
**支持市场**: A股、港股、美股
