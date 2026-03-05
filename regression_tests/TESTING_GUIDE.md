# 测试指南

## 🎯 两个核心测试

### 1️⃣ API接口测试（推荐）

**目的**: 直接验证所有理杏仁API接口的可用性

**运行**:
```bash
cd regression_tests
python3 test_all_apis.py
```

**时间**: 3-5分钟  
**覆盖**: 90+个API接口  
**依赖**: 仅需Python和Token

### 2️⃣ 端到端测试

**目的**: 测试完整的用户问题处理流程

**运行**:
```bash
cd regression_tests
python3 e2e_runner.py
```

**时间**: 30-60分钟  
**覆盖**: 116个技能  
**依赖**: 需要Claude/OpenCode

## 🚀 快速开始

```bash
# 1. 验证环境
python3 validate_env.py

# 2. 运行API测试
python3 test_all_apis.py

# 3. 运行完整测试
./run_tests.sh --full
```

## 📊 测试模式

```bash
# 仅API测试（推荐）
./run_tests.sh --api-only

# 仅端到端测试
./run_tests.sh --e2e-only

# 完整测试
./run_tests.sh --full
```

## 📁 测试结果

- API测试: `api_test_results/`
- E2E测试: `e2e_results/`

## 🔧 环境要求

1. Python 3.7+
2. Token文件: `token.cfg`（项目根目录）
3. 查询工具: `../.claude/skills/lixinger-data-query/scripts/query_tool.py`

## 📝 详细文档

完整文档请参考: [README.md](README.md)

---

**快速测试**: `python3 test_all_apis.py`  
**完整测试**: `./run_tests.sh --full`
