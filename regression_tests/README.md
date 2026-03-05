# 理杏仁开放平台测试套件

Version: 2.0.0  
Updated: 2026-02-24

## 📊 概述

理杏仁开放平台的完整测试套件，包含两个核心测试：

1. **API接口测试** - 直接测试所有理杏仁API接口的可用性
2. **端到端测试** - 通过Claude/OpenCode测试所有116个技能的完整流程

## 🎯 两个核心测试

### 核心测试 1: API接口测试（推荐）

**文件**: `test_all_apis.py`

直接测试所有理杏仁API接口，验证数据可用性。

**特点**:
- ✅ 快速执行（3-5分钟）
- ✅ 确定性结果
- ✅ 覆盖90+个核心API
- ✅ 详细的错误报告
- ✅ 无需LLM依赖

**运行方式**:
```bash
cd regression_tests
python3 test_all_apis.py
```

**测试覆盖**:
- A股：公司、指数、行业、基金（40+接口）
- 港股：公司、指数、行业（20+接口）
- 美股：指数（10+接口）
- 宏观：经济数据（30+接口）

### 核心测试 2: 端到端测试

**文件**: `e2e_runner.py`

通过Claude/OpenCode测试完整的用户问题处理流程。

**特点**:
- 测试真实用户场景
- 验证技能触发逻辑
- 包含116个技能的测试用例
- 完整的数据获取和分析流程

**运行方式**:
```bash
cd regression_tests
python3 e2e_runner.py
```

**测试流程**:
```
用户问题 → 技能识别 → 数据获取 → 分析逻辑 → 结果输出
```

## 🚀 快速开始

### 1. 验证环境

```bash
cd regression_tests
python3 validate_env.py
```

### 2. 运行API接口测试（推荐）

```bash
python3 test_all_apis.py
```

### 3. 运行完整测试套件

```bash
# 快速模式（仅API测试）
./run_tests.sh

# 仅API测试
./run_tests.sh --api-only

# 仅端到端测试
./run_tests.sh --e2e-only

# 完整测试（API + E2E）
./run_tests.sh --full
```

## 📁 目录结构

```
regression_tests/
├── test_all_apis.py              # 核心测试1: API接口测试
├── e2e_runner.py                 # 核心测试2: 端到端测试
├── run_tests.sh                  # 统一测试运行器
├── validate_env.py               # 环境验证
├── user_scenarios.json           # 116个技能的测试场景
├── test_config.json              # 测试配置
├── README.md                     # 本文档
├── api_test_results/             # API测试结果目录
├── e2e_results/                  # E2E测试结果目录
└── legacy_tests/                 # 旧版测试（已归档）
```

## 📊 测试结果

### API测试结果

```
api_test_results/
├── api_test_summary_YYYYMMDD_HHMMSS.json    # 测试汇总
└── ...
```

**汇总报告格式**:
```json
{
  "version": "2.0.0",
  "timestamp": "2026-02-24T12:00:00",
  "total": 90,
  "success": 85,
  "failed": 5,
  "details": [...]
}
```

### E2E测试结果

```
e2e_results/
├── summary_YYYYMMDD_HHMMSS.json             # 测试汇总
├── skill_name_case_1_YYYYMMDD_HHMMSS/       # 各测试用例
│   ├── question.txt
│   ├── output.txt
│   └── metadata.json
└── ...
```

## 🔧 环境要求

### 必需

1. **Python 3.7+**
   ```bash
   python3 --version
   ```

2. **理杏仁 API Token**
   - 在项目根目录创建 `token.cfg` 文件
   - 内容为你的理杏仁 API Token

3. **查询工具**
   - 确保 `../.claude/skills/lixinger-data-query/scripts/query_tool.py` 存在

### 可选

- Claude CLI（用于端到端测试）

## 📝 测试用例说明

### API测试用例

每个测试用例包含：
- `name`: 测试名称
- `suffix`: API路径
- `params`: 请求参数

示例：
```python
{
    "name": "A股公司基本信息",
    "suffix": "cn.company",
    "params": {"stockCodes": ["600519", "000858"]}
}
```

### E2E测试用例

每个技能包含3-5个典型用户问题，例如：

```json
{
  "skill": "dividend-corporate-action-tracker",
  "description": "分红与配股跟踪器",
  "market": "China-market",
  "questions": [
    "查询贵州茅台的分红历史",
    "工商银行的股息率怎么样？",
    "帮我看看哪些股票最近要分红了"
  ]
}
```

## 🐛 故障排查

### 常见问题

1. **Token文件未找到**
   ```
   Error: Token file not found
   ```
   解决：在项目根目录创建 `token.cfg` 文件

2. **API调用失败**
   ```
   Error: HTTP 401 Unauthorized
   ```
   解决：检查 `token.cfg` 中的Token是否有效

3. **超时错误**
   ```
   Error: Execution timed out
   ```
   解决：检查网络连接，或增加超时时间

### 调试模式

直接运行查询工具：
```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company" \
  --params '{"stockCodes": ["600519"]}' \
  --format json
```

## 📈 性能基准

| 测试类型 | 执行时间 | 成功率目标 |
|---------|---------|-----------|
| 环境验证 | < 5秒 | 100% |
| API接口测试 | 3-5分钟 | > 90% |
| 端到端测试 | 30-60分钟 | > 80% |

## 🎓 最佳实践

### 开发流程

1. **修改代码前**
   ```bash
   python3 validate_env.py
   ```

2. **修改代码后**
   ```bash
   python3 test_all_apis.py
   ```

3. **提交代码前**
   ```bash
   ./run_tests.sh --full
   ```

## 📚 相关文档

- [更新日志](CHANGELOG.md)
- [测试总结](TEST_SUMMARY.md)
- [主项目文档](../README.md)

## 🔮 未来改进

- [ ] 并行测试执行
- [ ] HTML测试报告
- [ ] 性能基准测试
- [ ] 自动化CI/CD集成

---

**版本**: 2.0.0  
**更新日期**: 2026-02-24  
**维护者**: Lixinger OpenAPI Team
