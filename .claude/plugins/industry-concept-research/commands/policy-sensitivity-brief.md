---
description: 评估目标行业对特定政策的敏感度，分析政策传导链条，推演超预期/符合预期/低于预期三种情景下的行业影响。
argument-hint: "[行业名称] [--policy 政策描述] [--event-date YYYY-MM-DD]"
---

# 政策敏感度简报

针对特定政策事件，评估目标行业的政策敏感度，分析从顶层定调到市场响应的完整传导链条，推演三种情景下的行业影响。

## 执行步骤

1. **确认参数**：
   - `industry`：目标行业名称（如"新能源"、"半导体"）；不填则扫描所有对当前政策环境敏感的行业
   - `policy`：可选，指定具体政策描述；不填则分析当前最重要的宏观政策背景
   - `event-date`：政策发布日期，默认近期

2. 加载 `policy-sensitivity-brief` skill（`.claude/plugins/industry-concept-research/skills/policy-sensitivity-brief/SKILL.md`），执行：
   - **政策链条分层梳理**：
     - Layer 1 顶层定调：中央经济工作会议 / 国务院政策
     - Layer 2 部委细则：工信部 / 发改委 / 财政部 / 证监会等
     - Layer 3 地方执行：各省市落地方案与补贴政策
     - Layer 4 市场响应：企业投资计划 / 产能扩张 / 盈利预期调整
   - **政策力度评分**（0-10分）：覆盖广度 × 执行力度 × 时间确定性
   - **行业敏感度矩阵**：直接受益 / 间接受益 / 中性 / 间接承压 / 直接承压
   - **三情景推演**：
     - 超预期（政策力度 > 市场预期）：概率 + 行业涨幅预估
     - 符合预期（政策力度 = 市场预期）：概率 + 行业影响预估
     - 低于预期（政策力度 < 市场预期）：概率 + 行业下行风险

3. 输出结构化结论，必须包含：
   - 政策链条传导图（四层结构）
   - 政策力度评分（0-10）+ 评分依据
   - 行业敏感度矩阵（各行业受影响方向与强度）
   - 三情景概率分布与行业影响
   - 最值得关注的行业（直接受益且政策执行确定性高）
   - 风险提示（政策退出 / 执行打折 / 市场预期已充分定价）

4. **置信度说明**：政策分析置信度受政策执行确定性影响，当政策处于"顶层定调"阶段尚未落地细则时，自动降级为 `WARNING`。

## 独立调用接口

本 skill 可被 `deep-research` 独立加载，最小输入：

```
{
  "industry_name": "新能源",
  "policy_description": "新能源汽车补贴政策延续至2027年",  # 可选
  "as_of_date": "2026-03-27"
}
```

输出：`policy_score`（政策力度0-10）、`sensitivity_matrix`（敏感度矩阵）、`scenarios`（三情景）

## 示例

```
/policy-sensitivity-brief 新能源
/policy-sensitivity-brief 半导体 --policy "国产替代专项基金扩大规模"
/policy-sensitivity-brief 房地产 --event-date 2026-03-15
/policy-sensitivity-brief --policy "降准50BP"
```
