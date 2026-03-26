# 数据获取指南

使用 `query_tool.py` 获取 shareholder-structure-monitor 所需的数据。

---

## 查询示例

### 查询Cn.Company.Major Shareholder Change

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/major-shareholders-shares-change" \
  --params '{"date": "2026-02-24"}' --limit 20
```

### 查询Cn.Company.Shareholders Num

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/shareholders-num" \
  --params '{"stockCode": "600519"}'
```

### 查询Cn.Company.Majority Shareholders (前十大股东)

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/majority-shareholders" \
  --params '{"stockCode": "600519", "date": "2026-02-24"}' \
  --columns "stockCode,holderName,holderType,holdAmount,holdRatio" \
  --limit 10
```

### 查询Cn.Company.Nolimit Shareholders (前十大流通股东)

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/nolimit-shareholders" \
  --params '{"stockCode": "600519", "date": "2026-02-24"}' \
  --columns "stockCode,holderName,holderType,holdAmount,holdRatio" \
  --limit 10
```

### 查询Cn.Company.Fund Shareholders (公募基金持股)

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fund-shareholders" \
  --params '{"stockCode": "600519", "date": "2026-02-24"}' \
  --columns "stockCode,fundName,holdAmount,holdRatio" \
  --limit 20
```

### 查询Cn.Company.Pledge (股权质押)

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/pledge" \
  --params '{"stockCode": "600519", "date": "2026-02-24"}' \
  --columns "stockCode,pledgorName,pledgeAmount,pledgeRatio,startDate,endDate" \
  --limit 20
```

### 查询Cn.Company.Senior Executive Shares Change (高管增减持)

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/senior-executive-shares-change" \
  --params '{"stockCode": "600519", "startDate": "2026-01-01", "endDate": "2026-02-24"}' \
  --columns "stockCode,executiveName,position,changeType,changeAmount,changePrice,changeDate" \
  --limit 20
```

---

## 参数说明

- `--suffix`: API 路径（参考下方可用 API 列表）
- `--params`: JSON 格式参数
- `--columns`: 指定返回字段（推荐使用，节省 30-40% token）
- `--row-filter`: 过滤条件
- `--limit`: 限制返回行数

---

## 本 Skill 常用 API

### 核心股东结构数据
- `cn/company/major-shareholders-shares-change` - 大股东增减持数据
- `cn/company/shareholders-num` - 股东人数数据
- `cn/company/majority-shareholders` - 前十大股东持股信息
- `cn/company/nolimit-shareholders` - 前十大流通股东持股信息

### 机构持股数据
- `cn/company/fund-shareholders` - 公募基金持股信息
- `cn/company/fund-collection-shareholders` - 基金公司持股信息

### 质押与高管数据
- `cn/company/pledge` - 股权质押数据
- `cn/company/senior-executive-shares-change` - 高管增减持数据

---

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../../plugins/query_data/lixinger-api-docs/SKILL.md`

## 数据字典参考

### 股东类型说明
- 自然人: 个人投资者
- 法人: 企业法人
- 基金: 公募基金、私募基金
- QFI: 合格境外机构投资者
- 国有资产: 国有企业、国有资本
- 其他: 社会保障基金、金融产品等

### 持股比例计算
持股比例 = 持股数量 / 总股本 × 100%

### 风险预警阈值
- 单一股东持股比例 > 30%: 高集中度风险
- 前十大股东合计持股比例 > 80%: 高集中度风险
- 股权质押比例 > 50%: 高质押风险
- 高管净减持持续 3 个月以上: 需要关注