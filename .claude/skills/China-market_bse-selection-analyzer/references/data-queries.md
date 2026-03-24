# 数据获取指南

使用 `query_tool.py` 获取 bse-selection-analyzer 所需的数据。

---

## 北交所分析常用查询

### 1. 获取北证50成分股列表

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/index/constituents" \
  --params '{"date": "latest", "stockCodes": ["899050"]}' \
  --flatten "constituents" \
  --columns "stockCode" \
  --limit 60
```

**说明**：
- 北证50指数代码：`899050`
- 使用 `--flatten "constituents"` 展开成分股数组
- 返回北交所50只核心成分股代码

---

### 2. 获取北交所股票基本面数据

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"date": "latest", "stockCodes": ["920001","920002","920019"], "metricsList": ["pe_ttm","pb","dyr","mc","to_r","ta"]}' \
  --columns "stockCode,pe_ttm,pb,dyr,mc,to_r,ta" \
  --limit 50
```

**常用指标**：
- `pe_ttm`: PE-TTM（滚动市盈率）
- `pb`: PB（市净率）
- `dyr`: 股息率
- `mc`: 市值
- `to_r`: 换手率
- `ta`: 成交金额
- `sp`: 股价
- `spc`: 涨跌幅

---

### 3. 获取北交所股票财务数据

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"date": "latest", "stockCodes": ["920001","920002","920019"], "metricsList": ["q.ps.toi.t_y2y","q.ps.np.t_y2y","q.ps.gp_m.t"]}' \
  --columns "stockCode,q.ps.toi.t_y2y,q.ps.np.t_y2y,q.ps.gp_m.t" \
  --limit 50
```

**常用指标**：
- `q.ps.toi.t_y2y`: 季度营收同比增速
- `q.ps.np.t_y2y`: 季度净利润同比增速
- `q.ps.gp_m.t`: 毛利率
- `y.ps.toi.t_y2y`: 年度营收同比增速
- `y.ps.np.t_y2y`: 年度净利润同比增速

---

### 4. 获取北证50指数基本面数据

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/index/fundamental" \
  --params '{"date": "latest", "stockCodes": ["899050"], "metricsList": ["pe_ttm.mcw","pb.mcw","dyr.mcw","mc","ta","cp","cpc"]}' \
  --limit 5
```

**常用指标**：
- `pe_ttm.mcw`: PE-TTM（市值加权）
- `pb.mcw`: PB（市值加权）
- `dyr.mcw`: 股息率（市值加权）
- `mc`: 总市值
- `ta`: 成交金额
- `cp`: 收盘点位
- `cpc`: 涨跌幅

---

## 参数说明

- `--suffix`: API 路径（参考下方可用 API 列表）
- `--params`: JSON 格式参数
- `--columns`: 指定返回字段（推荐使用，节省 30-40% token）
- `--row-filter`: 过滤条件
- `--flatten`: 展开嵌套数组
- `--limit`: 限制返回行数

---

## 本 Skill 常用 API

| API 路径 | 用途 | 示例 |
|---------|------|------|
| `cn/index/constituents` | 获取指数成分股 | 获取北证50成分股列表 |
| `cn/company/fundamental/non_financial` | 获取个股基本面 | PE、PB、市值、换手率 |
| `cn/company/fs/non_financial` | 获取个股财务数据 | 营收增速、利润增速、毛利率 |
| `cn/index/fundamental` | 获取指数基本面 | 指数PE、PB、点位 |

---

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../lixinger-data-query/SKILL.md`

