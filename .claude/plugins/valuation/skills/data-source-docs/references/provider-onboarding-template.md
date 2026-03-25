# Provider Onboarding Template

新增一个 provider 时，优先按最小 Provider Pack 方式填写。

## 1. 基本信息

- `provider_key`:
- `display_name`:
- `docs_location`:
- `owner` (optional):

## 2. 鉴权方式

只写“如何读取”，不要写密钥本身。

- `auth_source`: 例如 `token.cfg` / `ENV:XXX_API_KEY` / `cookie_file`
- `auth_note`:

## 3. 最小查询入口

至少提供一个可运行命令或一个很薄的脚本。

### One command example

```bash
python3 <script_or_command> <args>
```

### Thin script (optional)

- `script_path`:
- `example_args`:

## 4. 覆盖范围

- `coverage`:
  - company / financials / cashflow / market / peers / macro / other
- `best_for`:
- `not_good_for`:

## 5. 返回与口径说明

- `response_shape`: JSON / CSV / DataFrame / other
- `default_unit`:
- `default_currency`:
- `date_or_period_style`:

## 6. 已知限制

- `known_limits`:
- `rate_limit` (optional):
- `stability_note` (optional):

## 7. 建议摘要

给 `data-source-docs` 的摘要至少应覆盖：
- provider key
- docs source
- auth style
- one-command entry
- coverage
- caveats

## 8. 示例

```yaml
provider_key: akshare
display_name: AkShare
docs_location: .claude/skills/lixinger-data-query/api_new/akshare_data/
auth_source: none
one_command_example: python3 -c "import akshare as ak; print(ak.stock_zh_a_spot_em().head())"
coverage:
  - cashflow
  - macro
  - market
best_for: 作为 A 股缺口字段补数
not_good_for: 强依赖单一稳定官方口径的字段
response_shape: DataFrame
default_unit: provider specific
default_currency: CNY
date_or_period_style: trade date or report period
known_limits:
  - 部分接口依赖第三方站点稳定性
  - 某些接口需要 cookie 或额外参数
```
