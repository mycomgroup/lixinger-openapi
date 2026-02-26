# 金融分析技能包

完整的金融量化分析工具集，支持 A股、港股、美股三大市场。

## 📊 可用资源

- **116 个专业分析 Skills**：66 个 A股 + 13 个港股 + 37 个美股
- **162 个数据 API**：覆盖基本面、财务、行情、宏观等
- **1000+ AkShare 接口**：补充数据源
- **三级优先级**：Skills → 数据 API → AkShare

## 🔍 如何查找 Skills

**使用 grep 动态查找，不要记忆列表：**

```bash
# 按关键词搜索
ls skills/China-market/ | grep -i "关键词"
ls skills/HK-market/ | grep -i "关键词"
ls skills/US-market/ | grep -i "关键词"
```

**常用关键词**：dividend（分红）、valuation（估值）、risk（风险）、flow（资金）、event（事件）、portfolio（组合）、industry/sector（行业板块）

---

## 📁 项目工作目录管理（极简版）

### 核心规则：一个对话会话 = 一个项目文件夹

**规则极其简单**：
- **新对话** → 创建新项目文件夹
- **有上文** → 复用当前项目文件夹
- **所有操作**（数据查询、分析、报告）都在同一个文件夹中

### 文件夹命名规范

```bash
# 格式：analysis_YYYYMMDD_HHMMSS_主题关键词
analysis_20260225_143052_high_dividend/
analysis_20260225_144523_event_study_600089/
analysis_20260225_150138_market_overview/
```

### 项目文件夹结构

```
analysis_20260225_143052_high_dividend/
├── README.md              # 分析方案和执行记录
├── data/                  # 原始数据文件
│   ├── dividend_data.csv
│   ├── price_data.csv
│   └── company_info.csv
└── output/                # 最终输出报告
    └── report.md
```

### 工作流程

#### 第一次提问（新对话）

```bash
# 用户开启新对话
用户: "帮我筛选高股息股票"

# AI 创建新项目文件夹
PROJECT="analysis_$(date +%Y%m%d_%H%M%S)_high_dividend"
mkdir -p ${PROJECT}/{data,output}

# 创建 README.md
cat > ${PROJECT}/README.md << 'EOF'
# 高股息股票筛选分析

## 分析目标
筛选 A股市场优质高股息股票

## 使用 Skill
- skills/China-market/high-dividend-strategy/

## 执行时间
2026-02-25 14:30:52
EOF

# 下载数据到 data/
python3 skills/lixinger-data-query/scripts/query_tool.py ... \
  > ${PROJECT}/data/dividend_data.csv

# 生成报告到 output/
# (分析完成后保存)
```

#### 后续提问（同一对话）

```bash
# 用户在同一对话中继续
用户: "这些股票的分红历史怎么样？"

# AI 复用当前项目文件夹
PROJECT="analysis_20260225_143052_high_dividend"  # 已存在

# 追加数据到 data/
python3 skills/lixinger-data-query/scripts/query_tool.py ... \
  > ${PROJECT}/data/dividend_history.csv

# 更新 README.md
echo "## 追加分析：分红历史" >> ${PROJECT}/README.md

# 更新报告到 output/
```

### 用户如何控制

- **想开始新分析？** → 开启新对话
- **想继续当前分析？** → 在当前对话中继续提问
- **想查看历史分析？** → 查看对应的项目文件夹

---

## 💡 使用方式

### ⚠️ 使用优先级（严格遵守）

**三级优先级：市场分析 Skills > 数据 API > AkShare**

#### 第一优先级：市场分析 Skills

使用 `skills/China-market/`、`skills/HK-market/`、`skills/US-market/` 中的分析 skills。

**优势**：提供完整方法论、数据获取、分析逻辑、输出模板，开箱即用。

**查找方法**：
```bash
ls skills/China-market/ | grep -i "关键词"
```

#### 第二优先级：数据 API

使用 `skills/lixinger-data-query/` 的 162 个 API。

**使用场景**：找不到合适的 skill，或需要简单数据查询。

**使用前必须 grep 查看 API 文档**：
```bash
# 1. 用中文关键词搜索 API 文档正文
grep -r "分红" skills/lixinger-data-query/api_new/api-docs/
grep -r "股息" skills/lixinger-data-query/api_new/api-docs/
grep -r "市盈率\|PE" skills/lixinger-data-query/api_new/api-docs/
grep -r "市净率\|PB" skills/lixinger-data-query/api_new/api-docs/
grep -r "ROE\|净资产收益率" skills/lixinger-data-query/api_new/api-docs/
grep -r "营业收入\|营收" skills/lixinger-data-query/api_new/api-docs/
grep -r "净利润" skills/lixinger-data-query/api_new/api-docs/
grep -r "财报\|财务报表" skills/lixinger-data-query/api_new/api-docs/
grep -r "K线\|行情\|股价" skills/lixinger-data-query/api_new/api-docs/
grep -r "公告\|披露" skills/lixinger-data-query/api_new/api-docs/
grep -r "成分股\|指数" skills/lixinger-data-query/api_new/api-docs/
grep -r "基金持仓\|机构" skills/lixinger-data-query/api_new/api-docs/
grep -r "大宗交易\|龙虎榜" skills/lixinger-data-query/api_new/api-docs/
grep -r "融资融券" skills/lixinger-data-query/api_new/api-docs/
grep -r "陆股通\|港股通\|北向资金\|南向资金" skills/lixinger-data-query/api_new/api-docs/

# 2. 查看 API 文档（确保参数正确）
cat skills/lixinger-data-query/api_new/api-docs/[api_name].md

# 3. 执行查询
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/dividend" \
  --params '{"stockCode": "600519"}' \
  --columns "date,dividendPerShare"
```

#### 第三优先级：AkShare 接口

使用 `skills/lixinger-data-query/api_new/akshare_data/` 的 1000+ 接口。

**使用场景**：前两者无法满足需求，或需要补充数据源。

**使用前必须 grep 查看接口文档**：
```bash
# 查找相关接口
grep -r "关键词" skills/lixinger-data-query/api_new/akshare_data/

# 查看接口文档（确保用法正确）
cat skills/lixinger-data-query/api_new/akshare_data/[interface_name].md

# 使用 Python 调用
python3 -c "import akshare as ak; print(ak.interface_name())"
```

### 数据获取核心规则

**所有 skills 都使用 `query_tool.py` 获取数据**：

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/dividend" \
  --params '{"stockCode": "600519"}' \
  --columns "date,dividendPerShare,dividendYield" \
  --limit 20
```

**关键参数**：
- `--suffix`: API 路径（使用斜杠 `/` 而非点号 `.`）
- `--params`: JSON 格式参数
- `--columns`: 指定返回字段（节省 30-40% token）
- `--row-filter`: 过滤条件
- `--limit`: 限制返回行数

**⚠️ 日期规则**：
- **永远使用最近的日期**（如当前月份、上个月、最近一年）
- **不要使用过时日期**（如 2024 年的日期会导致分析结果无意义）
- 示例：`"date": "2026-02-25"` 或 `"startDate": "2025-02-01"`

### 工作流程

当用户提出金融分析问题时，**严格按照以下流程**：

#### 步骤 0：创建或复用项目文件夹

```bash
# 新对话：创建新项目文件夹
PROJECT="analysis_$(date +%Y%m%d_%H%M%S)_主题"
mkdir -p ${PROJECT}/{data,output}

# 有上文：复用当前项目文件夹
PROJECT="analysis_20260225_143052_主题"  # 已存在
```

#### 步骤 1：grep 查找合适的 Skill

```bash
ls skills/China-market/ | grep -i "关键词"
```

#### 步骤 2：查看 Skill 文档并总结思路

```bash
# 查看 Skill 说明和方法论
cat skills/China-market/high-dividend-strategy/SKILL.md
cat skills/China-market/high-dividend-strategy/references/data-queries.md
```

**看完后，先总结分析思路**：
- 明确分析目标和筛选标准
- 列出需要的数据和 API
- 规划分析步骤和输出内容
- 向用户确认思路后再开始执行

#### 步骤 3：获取数据（保存到项目文件夹）

**⚠️ 使用 API 前必须 grep 查看文档**：

```bash
# 1. 查看 API 文档（确保参数正确）
cat skills/lixinger-data-query/api_new/api-docs/cn_company_dividend.md

# 2. 下载数据到项目的 data/ 目录（使用最近日期）
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/dividend" \
  --params '{"stockCode": "600519", "startDate": "2025-01-01"}' \
  > ${PROJECT}/data/dividend_data.csv
```

#### 步骤 4：执行分析并生成报告

- 按照 Skill 方法论分析
- 报告保存到 `${PROJECT}/output/report.md`

#### 步骤 5：如果找不到 Skill，使用数据 API

```bash
# 1. 搜索 API
grep -r "关键词" skills/lixinger-data-query/api_new/api-docs/

# 2. 查看 API 文档（必须）
cat skills/lixinger-data-query/api_new/api-docs/[api_name].md

# 3. 总结思路后再执行查询
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/dividend" \
  --params '{"stockCode": "600519"}'
```

#### 步骤 6：如果 API 也无法满足，使用 AkShare

```bash
# 1. 搜索接口
grep -r "关键词" skills/lixinger-data-query/api_new/akshare_data/

# 2. 查看接口文档（必须）
cat skills/lixinger-data-query/api_new/akshare_data/[interface_name].md

# 3. 使用 Python 调用
python3 -c "import akshare as ak; print(ak.interface_name())"
```

---

## 🎯 使用示例

### 示例 1：高股息股票筛选

**用户问**："帮我筛选高股息股票"

```bash
# 1. 创建项目文件夹
PROJECT="analysis_$(date +%Y%m%d_%H%M%S)_high_dividend"
mkdir -p ${PROJECT}/{data,output}

# 2. grep 查找 Skill
ls skills/China-market/ | grep -i "dividend"

# 3. 查看 Skill 文档
cat skills/China-market/high-dividend-strategy/SKILL.md

# 4. 查看 API 文档（必须）
cat skills/lixinger-data-query/api_new/api-docs/cn_company_dividend.md

# 5. 获取数据（使用最近日期）
for code in 601398 601288 600900; do
  python3 skills/lixinger-data-query/scripts/query_tool.py \
    --suffix "cn/company/dividend" \
    --params "{\"stockCode\": \"${code}\", \"startDate\": \"2025-01-01\"}" \
    > ${PROJECT}/data/dividend_${code}.csv
done

# 6. 分析并生成报告到 output/report.md
```

### 示例 2：继续分析（同一对话）

**用户问**："这些股票的分红历史怎么样？"

```bash
# 复用当前项目文件夹
PROJECT="analysis_20260225_143052_high_dividend"

# 追加数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/dividend" \
  --params '{"stockCode": "601398", "startDate": "2020-01-01"}' \
  > ${PROJECT}/data/dividend_history_601398.csv

# 更新报告
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
│   └── ... (13 个 skills)
│
└── US-market/                     # 37 个美股分析 skills（首选）
    └── ... (37 个 skills)
```

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
  --suffix "cn/company" \
  --params '{"stockCodes": ["600519"]}' \
  --columns "stockCode,name"
```

---

## 📋 常用 API 速查

### ⚠️ API 路径格式

**必须使用斜杠 `/` 而不是点号 `.`**

```bash
# ✅ 正确
--suffix "cn/company/dividend"

# ❌ 错误
--suffix "cn.company.dividend"
```

### A股常用 API

| API 路径 | 说明 | 必需参数 |
|---|---|---|
| `cn/company` | 公司基本信息 | stockCodes |
| `cn/company/dividend` | 分红数据 | stockCode |
| `cn/company/fundamental/non_financial` | 基本面（PE/PB等） | stockCodes, date/startDate, metricsList |
| `cn/company/fs/non_financial` | 财务（营收/利润等） | stockCodes, date/startDate, metricsList |
| `cn/company/announcement` | 公告数据 | stockCode, startDate |
| `cn/index/fundamental` | 指数基本面 | stockCodes, date/startDate, metricsList |
| `cn/index/constituents` | 指数成分股 | indexCode, date |

### 港股常用 API

| API 路径 | 说明 | 必需参数 |
|---|---|---|
| `hk/company` | 公司基本信息 | stockCodes |
| `hk/company/dividend` | 分红数据 | stockCode |
| `hk/company/fundamental/non_financial` | 基本面数据 | stockCodes, date/startDate, metricsList |
| `hk/index/fundamental` | 指数基本面 | stockCodes, date/startDate, metricsList |

### 美股常用 API

| API 路径 | 说明 | 必需参数 |
|---|---|---|
| `us/company` | 公司基本信息 | stockCodes |
| `us/company/fs/non_financial` | 财务数据 | stockCodes, date/startDate, metricsList |
| `us/index/fundamental` | 指数基本面 | stockCodes, date/startDate, metricsList |

### 宏观数据 API

| API 路径 | 说明 | 必需参数 |
|---|---|---|
| `macro/money-supply` | 货币供应量 | date |
| `macro/cpi` | CPI数据 | date |
| `macro/ppi` | PPI数据 | date |
| `macro/gdp` | GDP数据 | date |

### 常见错误

#### 错误 1：`Api was not found`

**原因**：API 路径格式错误

**解决**：
```bash
# 1. 使用斜杠而非点号
--suffix "cn/company/dividend"  # ✅
--suffix "cn.company.dividend"  # ❌

# 2. grep 查看 API 文档确认路径
grep -r "dividend" skills/lixinger-data-query/api_new/api-docs/
```

#### 错误 2：`"metricsList" is required`

**原因**：fundamental 类 API 必须提供 metricsList

**解决**：
```bash
# ❌ 缺少 metricsList
--params '{"stockCodes": ["600519"], "date": "2026-02-25"}'

# ✅ 包含 metricsList
--params '{"stockCodes": ["600519"], "date": "2026-02-25", "metricsList": ["pe_ttm", "pb"]}'
```

#### 错误 3：`"stockCodes" is required`

**原因**：参数名称错误（单数 vs 复数）

**解决**：grep 查看 API 文档确认参数名
```bash
cat skills/lixinger-data-query/api_new/api-docs/cn_company.md
```

---

## 💡 核心原则

### 0. 工作流程

1. **新对话创建项目文件夹，有上文复用**
2. **先 grep 搜索，不要浏览列表**
3. **查看文档后先总结思路，确认后再执行**
4. **使用 API 前必须 grep 查看文档**
5. **永远使用最近日期，不用过时日期**
6. **数据保存到项目的 data/ 目录**
7. **报告保存到项目的 output/ 目录**

### 1. 优先级

**三级优先级（从高到低）**：
1. 市场分析 Skills（提供完整方法论）
2. 数据 API（需要自己编写分析逻辑）
3. AkShare 接口（补充数据源）

### 2. 数据获取

- **唯一工具**：`query_tool.py`
- **使用前必须 grep 查看 API 文档**
- **使用 `--columns` 过滤字段**（节省 30-40% token）
- **永远使用最近日期**

### 3. 项目管理

- **一个对话 = 一个项目文件夹**
- **命名规范**：`analysis_YYYYMMDD_HHMMSS_主题`
- **README.md 记录分析方案**

### 4. 查找技巧

```bash
# 按功能查找
ls skills/China-market/ | grep -i "dividend"
ls skills/China-market/ | grep -i "risk"
ls skills/China-market/ | grep -i "flow"
```

---

## 📚 相关文档

- **数据查询工具**：`skills/lixinger-data-query/SKILL.md`
- **API 文档目录**：`skills/lixinger-data-query/api_new/api-docs/`
- **AkShare 接口**：`skills/lixinger-data-query/api_new/akshare_data/`
