#!/bin/bash
# 理杏仁开放平台测试套件
# 包含两个核心测试：1) API接口测试  2) 端到端技能测试
#
# Version: 2.0.0
# Updated: 2026-02-24

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "================================================================================"
echo -e "${BLUE}理杏仁开放平台测试套件 v2.0.0${NC}"
echo "================================================================================"
echo ""
echo "本测试套件包含两个核心测试："
echo "  1️⃣  API接口测试 - 直接测试所有理杏仁API接口（推荐）"
echo "  2️⃣  端到端测试 - 通过Claude/OpenCode测试所有技能"
echo ""

# Parse arguments
TEST_MODE="quick"  # quick, api-only, e2e-only, full
if [ "$1" == "--api-only" ]; then
    TEST_MODE="api-only"
elif [ "$1" == "--e2e-only" ]; then
    TEST_MODE="e2e-only"
elif [ "$1" == "--full" ]; then
    TEST_MODE="full"
fi

# Test results
TOTAL_SUITES=0
PASSED_SUITES=0
FAILED_SUITES=0

# 1. Environment Validation
echo "================================================================================"
echo -e "${BLUE}步骤 0: 环境验证${NC}"
echo "================================================================================"
if python3 validate_env.py; then
    echo -e "${GREEN}✅ 环境验证通过${NC}"
else
    echo -e "${RED}❌ 环境验证失败，请先修复环境问题${NC}"
    exit 1
fi
echo ""

# 2. API Interface Tests (Core Test 1)
if [ "$TEST_MODE" == "quick" ] || [ "$TEST_MODE" == "api-only" ] || [ "$TEST_MODE" == "full" ]; then
    echo "================================================================================"
    echo -e "${BLUE}核心测试 1: API接口测试${NC}"
    echo "================================================================================"
    echo "测试所有理杏仁API接口的可用性和数据返回"
    echo "预计时间: 3-5分钟"
    echo ""
    
    TOTAL_SUITES=$((TOTAL_SUITES + 1))
    if python3 test_all_apis.py; then
        echo -e "${GREEN}✅ API接口测试通过${NC}"
        PASSED_SUITES=$((PASSED_SUITES + 1))
    else
        echo -e "${RED}❌ API接口测试失败${NC}"
        FAILED_SUITES=$((FAILED_SUITES + 1))
    fi
    echo ""
fi

# 3. End-to-End Tests (Core Test 2)
if [ "$TEST_MODE" == "e2e-only" ] || [ "$TEST_MODE" == "full" ]; then
    echo "================================================================================"
    echo -e "${BLUE}核心测试 2: 端到端技能测试${NC}"
    echo "================================================================================"
    echo "通过Claude/OpenCode测试所有119个技能的完整流程"
    echo "预计时间: 30-60分钟（取决于技能数量）"
    echo ""
    
    TOTAL_SUITES=$((TOTAL_SUITES + 1))
    if python3 e2e_runner.py; then
        echo -e "${GREEN}✅ 端到端测试通过${NC}"
        PASSED_SUITES=$((PASSED_SUITES + 1))
    else
        echo -e "${RED}❌ 端到端测试失败${NC}"
        FAILED_SUITES=$((FAILED_SUITES + 1))
    fi
    echo ""
fi

# 4. Valuation Plugin Regression Validation
echo "================================================================================"
echo -e "${BLUE}核心测试 3: Valuation Plugin 回归验证${NC}"
echo "================================================================================"
echo "验证 auto_valuation.py 核心计算结果与基准值一致（容差 ±1%）"
echo ""

VALUATION_SCRIPT="$SCRIPT_DIR/../.claude/plugins/valuation/skills/company-valuation/scripts/validate_sample.py"
if [ -f "$VALUATION_SCRIPT" ]; then
    TOTAL_SUITES=$((TOTAL_SUITES + 1))
    if python3 "$VALUATION_SCRIPT"; then
        echo -e "${GREEN}✅ Valuation Plugin 回归验证通过${NC}"
        PASSED_SUITES=$((PASSED_SUITES + 1))
    else
        echo -e "${RED}❌ Valuation Plugin 回归验证失败${NC}"
        FAILED_SUITES=$((FAILED_SUITES + 1))
    fi
else
    echo -e "${YELLOW}⚠️  validate_sample.py 未找到，跳过 Valuation Plugin 回归验证${NC}"
fi
echo ""

# Summary
echo "================================================================================"
echo -e "${BLUE}测试总结${NC}"
echo "================================================================================"
echo "测试套件总数: $TOTAL_SUITES"
echo -e "通过: ${GREEN}$PASSED_SUITES${NC}"
echo -e "失败: ${RED}$FAILED_SUITES${NC}"
echo ""

if [ $FAILED_SUITES -eq 0 ]; then
    echo -e "${GREEN}🎉 所有测试通过！${NC}"
    echo ""
    echo "查看详细结果:"
    echo "  - API测试: regression_tests/api_test_results/"
    echo "  - E2E测试: regression_tests/e2e_results/"
    exit 0
else
    echo -e "${RED}❌ 部分测试失败${NC}"
    echo ""
    echo "请查看详细日志以了解失败原因"
    exit 1
fi
