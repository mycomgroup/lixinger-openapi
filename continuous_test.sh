#!/bin/bash
# 持续测试直到所有命令通过或遇到新的错误类型

MAX_ITERATIONS=50
iteration=0

while [ $iteration -lt $MAX_ITERATIONS ]; do
    echo "=========================================="
    echo "测试迭代 $((iteration + 1))/$MAX_ITERATIONS"
    echo "=========================================="
    
    # 运行测试
    python3 test_data_queries_examples.py
    exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        echo "✅ 所有测试通过！"
        exit 0
    fi
    
    # 检查是否有新的错误需要修复
    echo ""
    echo "发现错误，请手动修复后继续..."
    exit 1
    
    iteration=$((iteration + 1))
done

echo "⚠️  达到最大迭代次数"
exit 1
