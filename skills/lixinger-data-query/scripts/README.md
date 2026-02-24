# 理杏仁数据查询工具

## 独立运行（无需虚拟环境）

`query_tool.py` 是完全独立的工具，包含所有依赖代码。

### 特性

- ✅ **无需虚拟环境**：不需要 `source .venv/bin/activate`
- ✅ **无需安装依赖**：不需要 `pip install`
- ✅ **开箱即用**：直接运行即可

### 前置条件

1. Python 3.x 已安装
2. 有 `token.cfg` 文件（在项目根目录或当前目录）

### 使用示例

```bash
# 查询股票基本信息
python3 query_tool.py \
  --suffix "cn.company" \
  --params '{"stockCodes": ["600519"]}' \
  --columns "stockCode,name"

# 查询大宗交易
python3 query_tool.py \
  --suffix "cn.company.block-deal" \
  --params '{"stockCode": "300750", "startDate": "2026-01-01", "endDate": "2026-02-24"}' \
  --limit 10

# 查询财务数据
python3 query_tool.py \
  --suffix "cn.company.fundamental.non_financial" \
  --params '{"date": "2024-12-31"}' \
  --row-filter '{"pe_ttm": {">": 10, "<": 20}}' \
  --columns "stockCode,name,pe_ttm,pb"
```

### 目录结构

```
scripts/
├── query_tool.py          # 主查询工具
├── cache_manager.py       # 缓存管理器
├── lixinger_openapi/      # 理杏仁 API 库（内置）
│   ├── __init__.py
│   ├── query.py
│   ├── token.py
│   └── _version.py
├── token.cfg              # API Token 配置（可选）
└── README.md              # 本文档
```

### 工作原理

1. `query_tool.py` 在运行时会自动将当前目录添加到 Python 路径
2. 从本地的 `lixinger_openapi/` 目录导入所需模块
3. 自动查找 `token.cfg` 文件（向上查找最多 5 层目录）

### Token 配置

工具会按以下顺序查找 Token：

1. 环境变量 `LIXINGER_TOKEN`
2. 当前目录及父目录的 `token.cfg` 文件（向上查找 5 层）

`token.cfg` 格式：
```
your_token_here
```

### 更多文档

- 完整 API 列表：`../SKILL.md`
- LLM 使用指南：`../LLM_USAGE_GUIDE.md`
- 查询示例：`../EXAMPLES.md`
- API 文档：`../api_new/api-docs/`
