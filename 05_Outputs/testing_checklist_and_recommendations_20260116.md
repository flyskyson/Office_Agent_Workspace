# Office Agent Workspace 测试清单与建议

**分析时间**: 2026-01-16
**分析范围**: 技能、MCP 服务器、核心组件

---

## 🎯 需要测试的技能 (6个)

| 技能 | 优先级 | 状态 | 测试重点 | 建议 |
|------|--------|------|----------|------|
| **super-butler** | 🔴 高 | 需测试 | 工作区状态、智能任务分配 | 核心技能,优先测试 |
| **idea-to-product** | 🔴 高 | 需测试 | 想法落地全流程 | 新功能,重点验证 |
| **application-generator** | 🟡 中 | 需测试 | 申请书生成、模板填充 | 市场监管智能体相关 |
| **skill-creator** | 🟡 中 | 需测试 | 技能创建流程 | 新功能 |
| **knowledge-indexer** | 🟢 低 | 需测试 | 知识索引、向量搜索 | 验证可用性 |
| **license-organizer** | 🟢 低 | 需测试 | 证照整理、OCR识别 | 验证准确性 |

---

## 🌐 已配置的 MCP 服务器 (3个)

| MCP 服务器 | 状态 | 测试建议 | 优先级 |
|-----------|------|----------|--------|
| **mcp-hot-news** | ✅ 已配置 | 测试多平台新闻获取 | 🔴 高 |
| **wopal-hotnews** | ✅ 已配置 | 测试中文热点新闻 | 🟡 中 |
| **skill-seeker** | ⚠️ 需修复 | 路径指向错误 | 🔴 高 |

### MCP 配置问题

**skill-seeker 配置错误**:
```json
"skill-seeker": {
  "command": "python",
  "args": ["-m", "skill_seekers.mcp.server_fastmcp"],
  "cwd": "c:\\Users\\flyskyson\\Office_Agent_Workspace\\Skill_Seekers",  // ❌ 错误路径
  "description": "Skill Seeker - 文档转Claude技能工具 (FastMCP)"
}
```

**应该改为**:
```json
"skill-seeker": {
  "command": "python",
  "args": ["-m", "skill_seekers.mcp.server_fastmcp"],
  "cwd": "c:\\Users\\flyskyson\\Office_Agent_Workspace\\external\\skill_seekers",  // ✅ 正确路径
  "description": "Skill Seeker - 文档转Claude技能工具 (FastMCP)"
}
```

---

## 🔧 核心组件测试建议

### v2.0 核心组件 (4个)

| 组件 | 文件 | 测试重点 | 优先级 |
|------|------|----------|--------|
| **MCP SQLite** | mcp_sqlite_wrapper.py | 数据库连接、查询性能 | 🔴 高 |
| **ConfigCenter** | config_center.py | 分层配置、热重载 | 🔴 高 |
| **AgentSupervisor** | agent_supervisor.py | 智能体编排、任务路由 | 🔴 高 |
| **Workflow Templates** | workflow_templates.py | 模板复用、执行流程 | 🟡 中 |

### 新增组件 (3个)

| 组件 | 文件 | 测试重点 | 优先级 |
|------|------|----------|--------|
| **Skill Seekers Adapter** | skill_seekers_adapter.py | GitHub 构建、多源组合 | 🔴 高 |
| **Skill Builder Facade** | skill_builder_facade.py | API 易用性、质量检查 | 🔴 高 |
| **Exceptions** | exceptions.py | 错误处理、日志记录 | 🟡 中 |

---

## 🚀 推荐测试顺序

### 第一阶段: 核心验证 (立即测试)

```bash
# 1. 修复 MCP 配置
# 2. 测试核心 v2.0 组件
python -m 00_Agent_Library.test_mcp_sqlite
python -m 00_Agent_Library.config_center
python -m 00_Agent_Library.agent_supervisor

# 3. 测试 Skill Seekers 集成
python 00_Agent_Library\examples\skill_builder_examples.py
```

### 第二阶段: 技能测试 (本周)

```bash
# 4. 测试超级管家技能
# 在 Claude Code 中触发: "管家模式"

# 5. 测试想法落地技能
# 在 Claude Code 中触发: "我有个想法..."

# 6. 测试申请生成技能
# 在 Claude Code 中触发: "生成申请书"
```

### 第三阶段: MCP 测试 (本周)

```bash
# 7. 测试新闻 MCP
# 在 Claude Code 中: "今日新闻"

# 8. 测试 Skill Seeker MCP
# 修复配置后重启 Claude Code
```

---

## 📊 测试脚本建议

### 1. 综合测试脚本

创建 `run_all_tests.py`:

```python
#!/usr/bin/env python3
"""运行所有核心测试"""

import sys
import subprocess
from pathlib import Path

def run_test(name, script):
    """运行单个测试"""
    print(f"\n{'='*60}")
    print(f"测试: {name}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(
            [sys.executable, script],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            print(f"✅ {name} - 通过")
            return True
        else:
            print(f"❌ {name} - 失败")
            print(f"错误: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {name} - 异常: {e}")
        return False

def main():
    """运行所有测试"""
    tests = [
        ("MCP SQLite", "00_Agent_Library/test_mcp_sqlite.py"),
        ("ConfigCenter", "00_Agent_Library/config_center.py"),
        ("AgentSupervisor", "00_Agent_Library/agent_supervisor.py"),
        ("Workflow Engine", "00_Agent_Library/workflow_engine.py"),
        ("Skill Seekers", "00_Agent_Library/skill_builder_facade.py"),
    ]

    results = []
    for name, script in tests:
        if Path(script).exists():
            results.append((name, run_test(name, script)))
        else:
            print(f"⚠️ {name} - 文件不存在")

    # 汇总
    print(f"\n{'='*60}")
    print("测试汇总")
    print(f"{'='*60}")

    passed = sum(1 for _, r in results if r)
    total = len(results)

    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")

    print(f"\n总计: {passed}/{total} 通过")

if __name__ == "__main__":
    main()
```

### 2. MCP 测试脚本

创建 `test_mcps.py`:

```python
#!/usr/bin/env python3
"""测试 MCP 服务器连接"""

import subprocess
import sys

def test_mcp(name, command):
    """测试 MCP 服务器"""
    print(f"\n测试 {name}...")

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )

        if "error" not in result.stderr.lower():
            print(f"✅ {name} - 可用")
            return True
        else:
            print(f"❌ {name} - 错误")
            return False
    except Exception as e:
        print(f"❌ {name} - {e}")
        return False

def main():
    """测试所有 MCP"""
    mcps = [
        ("mcp-hot-news", "npx -y mcp-hot-news"),
        ("wopal-hotnews", "npx -y @wopal/mcp-server-hotnews"),
        ("skill-seeker", "python -m skill_seekers.mcp.server_fastmcp"),
    ]

    results = []
    for name, cmd in mcps:
        results.append((name, test_mcp(name, cmd)))

    print(f"\n总计: {sum(1 for _, r in results if r)}/{len(results)} 可用")

if __name__ == "__main__":
    main()
```

---

## 🎯 本周测试计划

### 周一-周二: 核心组件

- [ ] 修复 skill-seeker MCP 配置
- [ ] 测试 MCP SQLite
- [ ] 测试 ConfigCenter
- [ ] 测试 AgentSupervisor

### 周三-周四: 技能验证

- [ ] 测试 super-butler 技能
- [ ] 测试 idea-to-product 技能
- [ ] 测试 application-generator 技能

### 周五: MCP 集成

- [ ] 测试 mcp-hot-news
- [ ] 测试 wopal-hotnews
- [ ] 测试 skill-seeker (修复后)

---

## 📝 测试检查表

### 技能测试

```markdown
- [ ] super-butler
  - [ ] 工作区状态检查
  - [ ] 智能任务分配
  - [ ] 文件整理功能

- [ ] idea-to-product
  - [ ] 想法澄清
  - [ ] 探索阶段
  - [ ] 设计阶段
  - [ ] 原型生成

- [ ] application-generator
  - [ ] 模板选择
  - [ ] 数据填充
  - [ ] 文档生成

- [ ] skill-creator
  - [ ] 技能创建流程
  - [ ] 配置验证
  - [ ] 打包功能

- [ ] knowledge-indexer
  - [ ] 文档索引
  - [ ] 向量搜索
  - [ ] 结果排序

- [ ] license-organizer
  - [ ] OCR 识别
  - [ ] 证照分类
  - [ ] 文件整理
```

### MCP 测试

```markdown
- [ ] mcp-hot-news
  - [ ] 多平台支持
  - [ ] 新闻获取
  - [ ] 数据格式

- [ ] wopal-hotnews
  - [ ] 中文平台
  - [ ] 热点聚合
  - [ ] 响应速度

- [ ] skill-seeker
  - [ ] 配置修复
  - [ ] GitHub 构建
  - [ ] 文档抓取
```

---

## 🔧 快速修复

### 立即修复: skill-seeker MCP 配置

编辑 `.claude/settings.local.json`:

```json
"skill-seeker": {
  "command": "python",
  "args": ["-m", "skill_seekers.mcp.server_fastmcp"],
  "cwd": "c:\\Users\\flyskyson\\Office_Agent_Workspace\\external\\skill_seekers",
  "description": "Skill Seeker - 文档转Claude技能工具 (FastMCP)"
}
```

### 创建测试脚本

我可以帮您创建:
1. `run_all_tests.py` - 综合测试
2. `test_mcps.py` - MCP 测试
3. `test_skills.py` - 技能测试

---

## 💡 建议

**优先级排序**:
1. 🔴 修复 skill-seeker MCP 配置
2. 🔴 测试 Skill Seekers 集成 (新功能)
3. 🔴 测试 v2.0 核心组件 (基础)
4. 🟡 测试超级管家技能 (核心)
5. 🟡 测试想法落地技能 (新功能)

**时间投入**:
- 核心 MCP 修复: 10 分钟
- 核心组件测试: 30 分钟
- 技能测试: 1 小时
- MCP 测试: 20 分钟

**总计**: 约 2 小时完成全部测试

---

**需要我帮您创建测试脚本或修复配置吗?**
