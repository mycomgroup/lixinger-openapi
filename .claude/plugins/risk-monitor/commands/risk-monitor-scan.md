# /risk-monitor-scan [watchlist]

对已选股票池做排雷扫描。

## 参数

- `watchlist`: 股票列表或组合标识
- `as_of_date`: 可选
- `mode`: `legacy_only` / `hybrid` / `engine_only`（默认 `legacy_only`）

## 输出要求

- 使用 `templates/post-selection-risk-clearance-output-template.md`
- 必须输出：建议剔除/降权/观察/保留
- 必须给出机制性风险解释与证伪条件

