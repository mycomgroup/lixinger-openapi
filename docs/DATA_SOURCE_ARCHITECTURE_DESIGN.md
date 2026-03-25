# 数据源架构设计（轻量 Provider Pack 版）

## 1. 背景

当前仓库已经有一条可工作的估值主链：

1. `cn-data-source` 提供 A 股取数入口。
2. `.claude/skills/lixinger-data-query` 承担实际查询执行。
3. `company-valuation` 消费估值输入并完成计算。

问题不在于“能不能扩数据源”，而在于**扩一个新 provider 的维护成本太高**。

如果每新增一个 provider 都要补：
- 一整套 provider -> canonical 映射
- domain priority
- 大量全局字段表
- 统一路由规则

那么 provider 一多，文档和映射都会变得脆弱，而且很难长期维护。

因此本次方案的目标不是再搭一个大框架，而是把当前体系收缩成**最小接入协议**。

---

## 2. 设计目标

### 2.1 目标

- 新增一个 provider 时，最低只需要：
  - 一份本地可读的 provider 文档
  - 本地鉴权信息来源
  - 最多一个查询命令或薄脚本
- 不要求为每个 provider 预先维护完整字段映射。
- `cn-data-source` 只做发现、路由、查询建议与溯源。
- `company-valuation` 主脚本保持不动。
- 允许按任务临时提取字段，而不是维护全局映射资产。
- 保留最小来源信息，方便回溯与解释。

### 2.2 非目标

本阶段**不做**以下事情：

- 不建设统一重型 SDK。
- 不重写 `.claude/skills/lixinger-data-query/scripts/query_tool.py`。
- 不引入全局 `provider registry` 作为强依赖运行时。
- 不为所有 provider 建一张完整的 provider -> canonical 大表。
- 不要求 `cn-data-source` 自动产出完整估值输入。

---

## 3. 核心结论

### 结论 1：新增 provider 采用 `Provider Pack`

一个 provider 的最小接入单元就是一个 **Provider Pack**。

它只需要包含四类信息：

1. **docs**：接口文档、说明文档或本地保存的网页/markdown
2. **auth**：本地如何读取鉴权，不在文档中暴露密钥本身
3. **one command**：一个最小可运行查询示例，或一个很薄的脚本
4. **scope note**：这个 provider 适合覆盖哪些数据，已知限制是什么

也就是说，后续新加 provider，不要求先统一 schema，只要求它**可被发现、可被调用、可被解释**。

### 结论 2：`cn-data-source` 改成“发现 / 路由 / 溯源”层

`cn-data-source` 不再承担“完整 canonical 编排器”的职责。

它负责：
- 判断当前任务需要什么数据
- 判断先看哪个 provider
- 给出查询入口或命令
- 说明结果来自哪里
- 在需要时帮助提取本次任务真正要用的最小字段集

它不再负责：
- 维护全局字段映射表
- 维护所有 provider 的 domain priority 资产
- 为所有任务统一产出完整 canonical JSON

### 结论 3：字段提取改为“按任务临时提取”

不预先维护 provider -> canonical 的全量映射。

而是：
- 先根据当前任务找到合适的数据源
- 再执行查询
- 最后只提取本次任务真正需要的字段

例如：
- 做 `company-valuation` 时，只提取估值模型需要的最小字段
- 做 `peer-analysis` 时，只提取可比公司与倍数相关字段
- 做 `scenario-modeling` 时，只提取情景分析要用的变量

### 结论 4：保留“任务边界上的最小标准化”

虽然不再维护全局映射，但**估值计算边界**仍然需要最小标准化。

换句话说：
- 仓库层面不维护“大而全的全局 canonical 映射”
- 但具体任务进入 `company-valuation` 之前，仍需把**本次运行的最小必需字段**整理为当前输入 schema

这一步是**task-local extraction**，不是全局 provider 治理。

---

## 4. 推荐目标架构

```text
Provider Docs / Summary
    └─ data-source-docs
         ├─ provider cached summary
         └─ onboarding template

Execution Hub
    └─ .claude/skills/lixinger-data-query
         ├─ 理杏仁查询
         ├─ AkShare 查询
         └─ future provider docs / one-command examples

Discovery / Routing / Provenance
    └─ cn-data-source
         ├─ 识别当前任务需要的数据
         ├─ 选择 provider
         ├─ 给出查询入口
         └─ 记录来源说明

Task Consumption
    └─ company-valuation / peer-analysis / scenario-modeling
         └─ 仅在当前任务里提取所需字段
```

---

## 5. 四层职责

### 5.1 Provider 文档与摘要层

当前承载：
- `.claude/plugins/valuation/skills/data-source-docs/`

职责：
- 保存 provider 的最小摘要
- 提供缓存后的 discoverability
- 帮助快速判断一个 provider 能不能覆盖当前需求

不负责：
- 不负责跨 provider 标准化
- 不负责最终估值入模
- 不负责统一执行

### 5.2 执行层

当前承载：
- `.claude/skills/lixinger-data-query/`

职责：
- 实际执行查询
- 处理参数、鉴权、返回格式
- 承载理杏仁、AkShare 和未来 provider 的单命令示例或薄脚本

定位说明：
- 这是**默认执行中枢**，不是标准化层
- 名字虽然是 `lixinger-data-query`，但短期不改名，以减少改动面

### 5.3 发现 / 路由 / 溯源层

当前承载：
- `.claude/plugins/valuation/skills/cn-data-source/SKILL.md`

职责：
- 面向任务做 provider 发现
- 给出推荐查询路径
- 提醒使用哪个命令 / 脚本
- 记录本次结果来自哪个 provider、哪个接口、哪个日期或报告期

不负责：
- 不维护全局字段映射表
- 不强制统一所有 provider 的返回结构
- 不承诺产出完整 canonical 输入

### 5.4 任务消费层

当前承载：
- `.claude/plugins/valuation/skills/company-valuation/`
- `.claude/plugins/valuation/skills/peer-analysis/`
- `.claude/plugins/valuation/skills/scenario-modeling/`

职责：
- 根据当前任务提取最小字段集
- 在需要计算时，整理成任务所需的输入结构
- 输出分析结果

关键边界：
- 只有在真正进入计算任务时，才做本次运行需要的最小标准化
- 这不是仓库级的全局映射治理

---

## 6. Provider Pack 最小接入协议

新增一个 provider 时，只要求补下面这些最小信息。

### 6.1 必填信息

1. `provider_key`
2. `docs_location`
3. `auth_source`
4. `one_command_example` 或 `thin_script`
5. `coverage`
6. `known_limits`

### 6.2 推荐存放位置

文档可放在以下任一位置：

- `.claude/skills/lixinger-data-query/api_new/{provider}_data/`
- 本地保存的 doc 文件路径
- 其他项目内固定可读目录

摘要缓存继续由 `data-source-docs` 维护。

### 6.3 鉴权规则

只记录“如何读取鉴权”，不记录密钥本身。

可接受的形式：
- `token.cfg`
- 环境变量名
- cookie 文件路径
- 本地配置文件名

### 6.4 命令规则

每个 provider 最多要求一个最小可运行命令，例如：

```bash
python3 some_query.py --symbol 600519 --field revenue
```

或直接是一段固定调用方式说明。

重点是：
- 能跑通一个查询
- 能证明 provider 可用
- 能让后续任务复用

不要求：
- 不要求先补完整映射
- 不要求先抽象成统一 SDK

---

## 7. 推荐工作流

### Step 1：先确定当前任务真正需要什么

不要一开始就试图把所有字段都拉齐。

先明确：
- 是估值
- 是同行分析
- 是情景分析
- 还是单纯找某个财务/市场/宏观字段

### Step 2：先看摘要，再看文档

优先顺序：
1. `data-source-docs` 缓存摘要
2. provider 原始文档
3. 已有查询示例或薄脚本

### Step 3：选择最合适的 provider

不依赖全局 priority 表，而是按当前任务判断：
- 谁覆盖这个字段
- 谁调用最稳定
- 谁的口径更适合本次任务
- 谁已经有可复用命令

### Step 4：执行一个最小查询

先拿到最小有效结果。

不要在 provider 接入阶段就追求完整字段覆盖。

### Step 5：只提取当前任务所需字段

例如在估值任务中，只提取：
- `revenue`
- `ebitda`
- `ebit`
- `net_income`
- `cash`
- `debt`
- `current_price`
- `shares`
- `risk_free_rate`

如果其中某几个字段缺失，再按任务需要补第二个 provider。

### Step 6：记录轻量溯源

对本次实际使用的字段或结果，记录：
- `provider`
- `dataset` / `endpoint`
- `field`
- `date` / `period_end`
- `unit`
- `note`

不要求每次都输出完整 `source_map`；但如果混用了多个 provider，建议为**实际用到的字段**保留简短溯源说明。

---

## 8. `cn-data-source` 的新契约

`cn-data-source` 的输出不再定义为“完整标准输入”，而是以下四类结果：

1. **provider 建议**
   - 当前任务先用哪个 provider
2. **查询入口**
   - 推荐命令、脚本或文档位置
3. **最小字段建议**
   - 本次任务应该先拿哪些字段
4. **来源说明**
   - 数据来自哪里、有没有混源、有没有口径风险

这意味着：
- `cn-data-source` 是入口和路由器
- 不是重型编排器
- 不是统一大映射中心

---

## 9. `company-valuation` 的边界

`company-valuation` 继续保持现有脚本和输入结构不动。

但数据进入估值前的处理方式改成：

- 先由 `cn-data-source` 帮助找到 provider
- 再执行最小查询
- 然后只把本次估值真正需要的字段整理成 `references/input-schema.md` 所要求的结构

重点：
- 这是**本次运行的输入整理**
- 不是为整个仓库沉淀一套 provider 全量映射

因此：
- `auto_valuation.py` 不需要修改
- `input-schema.md` 首阶段也不需要因为新增 provider 而频繁修改

---

## 10. 当前默认实践

在现有仓库里，建议维持如下默认习惯：

- A 股公司、利润表、资产负债表、市场数据：优先看理杏仁
- 现金流、无风险利率、部分宏观缺口字段：优先看 AkShare
- 其他新 provider：优先按 Provider Pack 判断，而不是强行塞进全局优先级表

这里的“优先”只是**实践经验**，不是必须维护成全局 registry。

---

## 11. 新数据源接入 Checklist

新增一个 provider 时，按下面顺序处理即可：

1. 放入 provider 文档
2. 明确本地鉴权信息来源
3. 写一个最小查询命令或薄脚本
4. 用 `data-source-docs` 生成或刷新摘要
5. 记录它适合的覆盖范围和限制
6. 在真实任务里按需使用
7. 只有在某类字段反复稳定复用时，才考虑沉淀局部映射示例

不需要默认做的事情：
- 不需要先补完整 provider -> canonical 映射
- 不需要先改 `auto_valuation.py`
- 不需要先建全局优先级注册表
- 不需要先建统一数据层

---

## 12. 本次方案对应的最小改动面

本轮只需要收敛以下文件定位：

- `docs/DATA_SOURCE_ARCHITECTURE_DESIGN.md`
- `.claude/plugins/valuation/skills/cn-data-source/SKILL.md`
- `.claude/plugins/valuation/skills/data-source-docs/SKILL.md`
- `.claude/plugins/valuation/commands/cn-company-valuation.md`
- `.claude/skills/lixinger-data-query/SKILL.md`
- `.claude/plugins/valuation/skills/data-source-docs/references/provider-onboarding-template.md`

如无必要，先不要动：
- `company-valuation/scripts/auto_valuation.py`
- `query_tool.py`
- 全局 schema

---

## 13. 方案结论

这次方案收缩后的核心只有三句话：

1. **新 provider 按 Provider Pack 接入**：`docs + auth + one command`。
2. **`cn-data-source` 只做发现 / 路由 / 溯源**：不再维护全量映射。
3. **字段整理改成按任务临时提取**：只在真正运行任务时整理最小字段集。

这样做的收益是：
- 新 provider 接入成本低
- 文档维护面小
- 不会因为 provider 变多而堆积脆弱映射
- 仍然保留足够的来源说明和解释能力
- 对现有执行脚本和估值主链改动最小
