# 行业板块细节化 Skills 路线图

## 目标

在行业/概念主流程基础上，补齐“细分下钻 + 因子归因 + 拥挤度风控”，将输出从观点型升级为可执行、可复评的结构化研究结果。

## 状态总览

### P0（已落地）

1. `industry-subsector-decomposer` ✅
   - 行业一级→二级→三级下钻
   - 细分强弱分层与贡献度分解
   - 输出下一阶段优先子方向

2. `sector-factor-attributor` ✅
   - 三维归因：估值 / 盈利预期 / 风险溢价
   - 风格因子暴露矩阵
   - 归因质量与证据缺口声明

3. `board-crowding-risk-monitor` ✅
   - 四维拥挤度评分
   - 五类脆弱触发器
   - 分级操作建议（NORMAL/WATCH/REDUCE/AVOID）

## P1（规划中）

4. `earnings-catalyst-tracker` ⏳
   - 财报季与预期差映射
   - 上修/下修扩散路径

5. `policy-implementation-tracker` ⏳
   - 政策链条落地强度跟踪
   - 顶层到地方执行的传导观察

6. `industry-style-profiler` ⏳
   - 行业风格画像与漂移监控
   - 跨行业风格替代建议

## P2（规划中）

7. `global-linkage-translator` ⏳
   - 海外变量向 A 股行业映射

8. `supply-demand-signal-builder` ⏳
   - 行业供需高频代理指标模板

9. `sector-pairs-rotation` ⏳
   - 行业配对轮动观察框架

## 集成原则（持续有效）

- 新增 skill 必须提供：`SKILL.md + references/data-queries.md + references/methodology.md + references/output-template.md`
- 必须声明“§ 独立调用接口”，可被外部插件直接复用
- 输出必须接入统一 contracts，并通过 QA 三档决策
- 允许降级，但必须显式输出 `data_gaps`，禁止静默降级

## 下一阶段重点

- 优先推进 P1 的事件化能力（财报催化、政策落地）
- 保持与 Orchestrator 命令口径一致，避免文档与能力漂移
- 所有新增能力继续遵循同一 fail-safe 与质量门禁体系