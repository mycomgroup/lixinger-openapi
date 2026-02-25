# Skills 改进计划

基于 agent-skill-creator 最佳实践的改进方案

## 📋 改进清单

### 阶段 1：核心文件补充（高优先级）

每个 skill 需要添加以下文件：

- [ ] `.claude-plugin/marketplace.json` - 使 skill 可被 Claude Code 识别
- [ ] `INSTALLATION.md` - 详细的安装指南（中文）
- [ ] `DECISIONS.md` - 记录架构决策
- [ ] `VERSION` - 版本号文件
- [ ] `CHANGELOG.md` - 变更日志

### 阶段 2：文档增强（中优先级）

- [ ] 扩充 `SKILL.md` 到 5000+ 字
  - 添加 5+ 个完整的使用示例（带实际命令）
  - 详细的错误处理说明
  - 完整的工作流程（每一步都有具体命令）
  
- [ ] 增强 `references/` 目录
  - `api-guide.md` (1500+ 字) - API 详细使用指南
  - `troubleshooting.md` (1000+ 字) - 常见问题排查
  - 在 `methodology.md` 中添加数值示例

### 阶段 3：代码质量提升（中优先级）

- [ ] 所有 Python 脚本添加：
  - 完整的类型提示（type hints）
  - 详细的 docstrings（包含 Args, Returns, Raises, Example）
  - 输入验证
  - 错误处理（try-except）
  - 日志记录（logging）

### 阶段 4：配置优化（低优先级）

- [ ] 改进 `assets/config.json`
  - 添加内联注释（使用 `_comment`, `_note` 字段）
  - 提供真实的默认值
  - 添加获取 API key 的说明

## 🚀 快速开始

### 方案 A：手动改进（推荐用于学习）

逐个 skill 手动添加缺失的文件，参考本目录下的模板。

### 方案 B：使用脚本批量生成（快速）

运行改进脚本自动为所有 skills 生成基础文件：

```bash
cd lixinger-openapi/skills
python3 scripts/improve_skills.py
```

## 📁 文件模板

### marketplace.json 模板

```json
{
  "name": "skill-name",
  "version": "1.0.0",
  "plugins": [
    {
      "name": "skill-name-plugin",
      "description": "技能描述",
      "source": "./",
      "skills": ["./SKILL.md"]
    }
  ]
}
```

### VERSION 模板

```
1.0.0
```

### CHANGELOG.md 模板

```markdown
# 更新日志

## [1.0.0] - 2026-02-25

### 新增
- 初始版本发布
- 核心功能实现

### 数据来源
- 理杏仁 API v1.0

### 已知限制
- 仅支持 A股市场
```

## 📊 改进优先级

### 立即执行（今天）
1. 为所有 skills 添加 `.claude-plugin/marketplace.json`
2. 创建 `INSTALLATION.md`（至少一个示例 skill）

### 本周完成
3. 扩充 3-5 个核心 skills 的 SKILL.md
4. 添加 `troubleshooting.md` 到核心 skills

### 本月完成
5. 改进所有 Python 代码质量
6. 完善所有 skills 的文档

## 🎯 示例：改进 high-dividend-strategy

作为示例，我们先完整改进 `high-dividend-strategy` skill：

```bash
cd skills/China-market/high-dividend-strategy

# 1. 创建目录
mkdir -p .claude-plugin

# 2. 创建 marketplace.json
cat > .claude-plugin/marketplace.json << 'EOF'
{
  "name": "high-dividend-strategy",
  "version": "1.0.0",
  "plugins": [
    {
      "name": "high-dividend-strategy-plugin",
      "description": "A股高股息策略分析工具",
      "source": "./",
      "skills": ["./SKILL.md"]
    }
  ]
}
EOF

# 3. 创建 VERSION
echo "1.0.0" > VERSION

# 4. 创建 CHANGELOG.md
cat > CHANGELOG.md << 'EOF'
# 更新日志

## [1.0.0] - 2026-02-25

### 新增
- 初始版本发布
- 支持中证红利指数成分股分析
- 实现 5 年总回报计算
- 分红可持续性评估
- 综合评分排名系统

### 数据来源
- 理杏仁 API v1.0

### 已知限制
- 仅支持 A股市场
- 免费 API 限制：1000 次/天
EOF

# 5. 创建 INSTALLATION.md
# （内容见下方模板）
```

## 📚 参考资源

- agent-skill-creator 项目：`/Users/fengzhi/Downloads/git/agent-skill-creator`
- 质量标准：`agent-skill-creator/references/quality-standards.md`
- 架构指南：`agent-skill-creator/docs/CLAUDE_SKILLS_ARCHITECTURE.md`

## ❓ 需要帮助？

如果在改进过程中遇到问题，可以：
1. 查看 agent-skill-creator 的示例 skills
2. 参考 quality-standards.md 的检查清单
3. 询问 AI 助手获取具体指导
