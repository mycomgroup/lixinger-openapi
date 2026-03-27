# 数据获取指南

使用 `query_tool.py` 获取 opposing-pair-detector 所需数据。

---

## 默认代理代码

| 主题 | 指数代码 | 指数名称 |
|---|---|---|
| 大盘 | `000300` | 沪深300 |
| 大盘防御 | `000016` | 上证50 |
| 小盘 | `932000` | 中证2000 |
| 银行 | `399986` | 中证银行 |
| 科技 | `931186` | 中证科技 |
| 软件 | `930601` | 中证软件 |
| TMT 备选 | `000998` | 中证TMT |
| 周期 | `000968` | 300周期 |

---

## 核心查询

### 1. 拉取单个指数最近日线

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/candlestick" \
  --params '{"stockCode":"000300","type":"normal","startDate":"2026-03-24","endDate":"2026-03-27"}' \
  --columns "date,close,change" \
  --limit 5
```

### 2. 银行 vs 科技

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/candlestick" \
  --params '{"stockCode":"399986","type":"normal","startDate":"2026-03-24","endDate":"2026-03-27"}' \
  --columns "date,close,change" \
  --limit 5

python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/candlestick" \
  --params '{"stockCode":"931186","type":"normal","startDate":"2026-03-24","endDate":"2026-03-27"}' \
  --columns "date,close,change" \
  --limit 5
```

### 3. 大盘 vs 2000

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/candlestick" \
  --params '{"stockCode":"000300","type":"normal","startDate":"2026-03-24","endDate":"2026-03-27"}' \
  --columns "date,close,change" \
  --limit 5

python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/candlestick" \
  --params '{"stockCode":"932000","type":"normal","startDate":"2026-03-24","endDate":"2026-03-27"}' \
  --columns "date,close,change" \
  --limit 5
```

### 4. 周期 vs 科技

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/candlestick" \
  --params '{"stockCode":"000968","type":"normal","startDate":"2026-03-24","endDate":"2026-03-27"}' \
  --columns "date,close,change" \
  --limit 5

python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/candlestick" \
  --params '{"stockCode":"931186","type":"normal","startDate":"2026-03-24","endDate":"2026-03-27"}' \
  --columns "date,close,change" \
  --limit 5
```

---

## 辅助查询

### 查找指数代码

当代理代码需要扩展时，先查指数库，不要硬猜：

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index" \
  --params '{}' \
  --columns "stockCode,name,series,source" \
  --row-filter '{"name":{"contains":"银行"}}' \
  --limit 50
```

可替换关键词：

- `银行`
- `软件`
- `科技`
- `2000`
- `周期`

---

## 使用规则

1. 默认看最近 `2-5` 个交易日，不要只看单个点位。
2. 如果 `T` 日数据不存在，自动退回上一个交易日，并写清楚日期。
3. 默认使用 `type=normal`。
4. 输出时建议自己用 `close_t / close_t-1 - 1` 再算一遍，避免只依赖接口自带四舍五入字段。

---

## 备注

- `cn/index/candlestick` 是本技能的主数据源。
- 如需补充北向或热度信息，可按需查 `cn/index/hot/mm_ha`，但它只做辅助，不应用来代替最新收盘判断。
