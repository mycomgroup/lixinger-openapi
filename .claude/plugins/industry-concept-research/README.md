# Industry & Concept Research Plugin

面向 A 股“行业板块 + 概念板块”研究的一体化插件。

## 插件目标

将以下 6 个能力统一编排，形成从“市场观察 → 轮动判断 → 产业链验证 → 政策映射 → 跟踪监控”的完整闭环：

- `industry-board-analyzer`：行业板块分析
- `sector-rotation-detector`：行业轮动探测
- `industry-chain-mapper`：产业链映射与景气跟踪
- `concept-board-analyzer`：概念板块分析
- `policy-sensitivity-brief`：政策敏感度简报
- `industry-report-analyzer`：行业研报分析

## 目录结构

- `commands/`：统一命令入口
- `skills/`：核心能力技能包
- `ARCHITECTURE.md`：架构设计文档（模块、流程、数据与扩展方案）

## Commands

- `/industry-board-analyzer [范围/窗口]`
- `/sector-rotation-detector [范围/窗口]`
- `/industry-chain-mapper [产业链主题]`
- `/concept-board-analyzer [概念主题]`
- `/policy-sensitivity-brief [政策主题]`
- `/industry-report-analyzer [行业/研报主题]`
- `/industry-concept-research [研究主题]`（综合编排入口）

## 统一执行流程

1. 先用行业/概念横截面识别“哪里最强、哪里分化”；
2. 再用轮动框架判断“为什么强、能否持续”；
3. 用产业链映射验证“利润与景气是否可传导”；
4. 用政策敏感度判断“催化与扰动方向”；
5. 用行业研报分析校准“机构预期与关键假设”；
6. 最终输出可执行监控清单与失效条件。
