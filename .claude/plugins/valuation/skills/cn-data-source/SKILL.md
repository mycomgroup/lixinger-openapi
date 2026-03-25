# cn-data-source

description: 为 A 股与估值相关任务提供数据源发现、路由、查询建议与溯源入口。当任务涉及 6 位股票代码、需要选择 provider，或需要解释字段来源时优先使用。该 skill 不负责维护完整 provider -> canonical 映射，只在当前任务中帮助提取最小字段集。

> 轻量数据源方案设计见 `docs/DATA_SOURCE_ARCHITECTURE_DESIGN.md`。
> 当前默认执行层继续复用 `.claude/skills/lixinger-data-query`。

## 角色定位

`cn-data-source` 现在只做四件事：

1. 识别当前任务需要哪些数据
2. 发现当前最适合的 provider
3. 给出查询入口或命令示例
4. 记录本次结果的来源说明

不负责：
- 不维护全量 provider -> canonical 映射表
- 不承诺自动产出完整估值输入 JSON
- 不把所有 provider 强行统一成一个返回结构

---

## 默认协作关系

- `data-source-docs`：负责 provider 摘要、文档缓存和 discoverability
- `.claude/skills/lixinger-data-query`：负责默认执行查询
- `company-valuation` / `peer-analysis` / `scenario-modeling`：按当前任务提取最小字段集

---

## 推荐工作流

### Step 1：先确定当前任务的最小字段需求

先判断任务是什么：
- 公司估值
- 同行对比
- 情景分析
- 单一字段查询
- 宏观 / 行业补数

不要一开始就尝试组装全量标准输入。

### Step 2：先看摘要，再看原始文档

优先顺序：
1. 先看 `data-source-docs` 的缓存摘要
2. 再看 provider 原始文档
3. 再看已有命令示例或薄脚本

### Step 3：选择 provider

选择标准：
- 当前任务是否覆盖目标字段
- 当前 provider 是否已有可复用命令
- 口径是否更适合本次任务
- 稳定性是否足够

### Step 4：执行最小查询

每次先执行一个最小可验证查询。

优先输出：
- 最少字段
- 最少行数
- 能证明接口可用的结果

### Step 5：只提取本次任务真正需要的字段

如果任务要进入 `company-valuation`，只整理当前估值所需的最小字段，例如：
- `financials.revenue`
- `financials.ebitda`
- `financials.ebit`
- `financials.net_income`
- `balance_sheet.cash`
- `balance_sheet.debt`
- `market.current_price`
- `shares.basic`
- `assumptions.cost_of_capital.risk_free_rate`

这一步是**按任务临时提取**，不是仓库级全局映射治理。

### Step 6：保留轻量溯源信息

如使用多个 provider，建议只为**实际使用的字段**保留来源信息。

推荐保留：
- `provider`
- `dataset` / `endpoint`
- `field`
- `date` / `period_end`
- `unit`
- `note`

示例：

```json
{
  "source_notes": [
    "revenue 来自 lixinger / cn.company.fs.non_financial / y.ps.toi.t / 2024-12-31",
    "operating_cash_flow 来自 akshare / stock_financial_report_sina / 2024-12-31"
  ]
}
```

如确实需要字段级对象结构，也可以只为本次实际使用字段输出精简版 `source_map`。

---

## A 股默认实践

当前仓库中，建议按经验优先考虑：

- 公司信息、利润表、资产负债表、市场数据：优先理杏仁
- 现金流、无风险利率、宏观缺口字段：优先 AkShare
- 新 provider：按文档与命令可用性判断，不强制纳入全局优先级表

注意混用时必须自行核对：
- 报告期
- 单位
- 币种
- 合并口径

---

## 新 Provider 最小接入要求

每个 provider 只要求补齐以下信息：

1. provider 文档路径或本地 doc 文件
2. 鉴权读取方式（如 `token.cfg`、环境变量、cookie 文件）
3. 一个最小查询命令，或一个很薄的脚本
4. 覆盖范围说明
5. 已知限制或注意事项

不要求默认补齐：
- 不要求先建全量字段映射
- 不要求先改 `company-valuation` schema
- 不要求先改估值主脚本

模板见：
- `.claude/plugins/valuation/skills/data-source-docs/references/provider-onboarding-template.md`

---

## 常用查询入口

### 理杏仁查询

```bash
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "<API后缀>" \
  --params '<JSON参数>' \
  --columns "<字段列表>"
```

### AkShare 查询

使用 Python 直接调用或复用 `.claude/skills/lixinger-data-query` 下已有文档与示例。

---

## 使用原则

- 优先复用已有 provider 文档和单命令示例
- 优先先拿到最小有效结果，再决定是否补第二个 provider
- 优先在任务边界上临时提取字段，不沉淀脆弱的全局映射
- 只有当某类字段长期、稳定、重复出现时，才考虑补局部示例或固定抽取模板
