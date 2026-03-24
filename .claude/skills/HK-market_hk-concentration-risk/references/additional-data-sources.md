# 港股集中度风险监控 - 增强数据源

本文档说明理杏仁API之外需要补充的数据源。

---

## 缺失数据清单

### 1. 组合持仓数据 ⚠️ 必需

**数据内容**:
- 持仓股票列表
- 每只股票的持仓数量
- 每只股票的权重
- 持仓成本
- 当前市值

**数据来源**:
- 券商交易系统
- 组合管理系统
- Excel/CSV文件导入

**数据格式示例**:
```json
{
  "portfolio": {
    "name": "港股价值组合",
    "total_value": 10000000,
    "holdings": [
      {
        "stock_code": "00700",
        "stock_name": "腾讯控股",
        "shares": 10000,
        "cost": 350.00,
        "current_price": 380.00,
        "market_value": 3800000,
        "weight": 0.38
      },
      {
        "stock_code": "09988",
        "stock_name": "阿里巴巴",
        "shares": 15000,
        "cost": 80.00,
        "current_price": 85.00,
        "market_value": 1275000,
        "weight": 0.1275
      }
    ]
  }
}
```

---

### 2. 风险因子数据 ⚠️ 重要

**数据内容**:
- 市场风险因子（Beta）
- 风格风险因子（Size, Value, Momentum等）
- 行业风险因子
- 因子暴露度

**数据来源**:
- Barra风险模型
- MSCI风险模型
- 自建风险模型
- 学术研究数据

**数据格式示例**:
```json
{
  "risk_factors": {
    "00700": {
      "market_beta": 1.15,
      "size_factor": -0.85,
      "value_factor": -0.32,
      "momentum_factor": 0.45,
      "volatility_factor": 0.28
    }
  }
}
```

**替代方案**:
如果无法获取专业风险模型数据，可以使用简化方法：
- 使用历史收益率计算Beta
- 使用市值作为Size因子
- 使用PB作为Value因子
- 使用过去12个月收益率作为Momentum因子

---

### 3. 相关性矩阵 ⚠️ 重要

**数据内容**:
- 股票间相关系数
- 行业间相关系数
- 时间窗口（如60日、120日、250日）

**数据来源**:
- 历史价格数据计算
- 风险模型提供
- 彭博/Wind等数据终端

**计算方法**:
```python
# 使用历史收益率计算相关性
import pandas as pd
import numpy as np

# 假设已有价格数据
prices = pd.DataFrame({
    '00700': [...],
    '09988': [...],
    '00005': [...]
})

# 计算收益率
returns = prices.pct_change()

# 计算相关性矩阵
correlation_matrix = returns.corr()
```

---

### 4. 波动率数据 ⚠️ 重要

**数据内容**:
- 历史波动率
- 隐含波动率（期权）
- 实现波动率
- 波动率预测

**数据来源**:
- 历史价格计算
- 期权市场数据
- GARCH模型预测

**计算方法**:
```python
# 计算历史波动率
returns = prices.pct_change()
volatility = returns.std() * np.sqrt(252)  # 年化波动率
```

---

### 5. VaR计算数据 ⚠️ 重要

**数据内容**:
- 历史收益率分布
- 协方差矩阵
- 情景分析数据

**数据来源**:
- 历史价格数据
- 蒙特卡洛模拟
- 历史模拟法

**计算方法**:
```python
# 历史模拟法计算VaR
portfolio_returns = ...  # 组合历史收益率
var_95 = np.percentile(portfolio_returns, 5)  # 95% VaR
```

---

### 6. 流动性数据 ⚠️ 可选

**数据内容**:
- 日均成交量
- 日均成交额
- 买卖价差
- 市场深度

**数据来源**:
- 交易所数据
- 券商数据
- 彭博/Wind终端

**理杏仁API可获取**:
```bash
# 获取成交量数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/candlestick" \
  --params '{"stockCode": "00700", "startDate": "2024-01-01", "endDate": "2024-12-31"}' \
  --columns "date,volume,amount"
```

---

### 7. 基准数据 ⚠️ 可选

**数据内容**:
- 基准指数成分
- 基准指数权重
- 基准指数收益率

**数据来源**:
- 指数公司官网
- 理杏仁API（部分可获取）

**理杏仁API可获取**:
```bash
# 获取恒生指数成分股
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/index/constituents" \
  --params '{"indexCode": "HSI"}' \
  --columns "stockCode,name,weight"
```

---

## 数据优先级

### 高优先级（必需）
1. ✅ 组合持仓数据 - 核心输入
2. ✅ 股票价格数据 - 理杏仁API可获取
3. ✅ 行业分类数据 - 理杏仁API可获取

### 中优先级（重要）
4. ⚠️ 风险因子数据 - 需要外部数据源或简化计算
5. ⚠️ 相关性矩阵 - 可从历史价格计算
6. ⚠️ 波动率数据 - 可从历史价格计算

### 低优先级（可选）
7. ℹ️ VaR计算数据 - 可从历史数据计算
8. ℹ️ 流动性数据 - 部分可从理杏仁API获取
9. ℹ️ 基准数据 - 部分可从理杏仁API获取

---

## 数据获取建议

### 最小可行方案
仅使用理杏仁API + 组合持仓数据：
1. 从组合系统导出持仓数据
2. 使用理杏仁API获取价格和行业数据
3. 计算基础集中度指标（权重、HHI等）

### 标准方案
理杏仁API + 组合持仓 + 简化风险计算：
1. 组合持仓数据
2. 理杏仁API数据
3. 从历史价格计算相关性和波动率
4. 简化风险因子（Beta、市值、PB等）

### 完整方案
理杏仁API + 组合持仓 + 专业风险模型：
1. 组合持仓数据
2. 理杏仁API数据
3. Barra/MSCI风险模型数据
4. 完整的风险因子和相关性数据
5. 高级VaR和压力测试

---

## 数据接口建议

### 组合持仓数据接口
```python
# 建议的数据接口格式
def get_portfolio_holdings():
    """
    获取组合持仓数据
    
    Returns:
        dict: {
            'portfolio_name': str,
            'total_value': float,
            'holdings': [
                {
                    'stock_code': str,
                    'shares': int,
                    'weight': float,
                    'market_value': float
                }
            ]
        }
    """
    pass
```

### 风险数据接口
```python
# 建议的风险数据接口
def get_risk_factors(stock_codes):
    """
    获取风险因子数据
    
    Args:
        stock_codes: list of str
        
    Returns:
        dict: {
            'stock_code': {
                'market_beta': float,
                'size_factor': float,
                'value_factor': float,
                ...
            }
        }
    """
    pass
```

---

## 联系方式

如需帮助获取这些数据源，请联系：
- 技术支持：support@example.com
- 数据服务：data@example.com

---

**更新日期**: 2026-02-24  
**版本**: v1.0.0
