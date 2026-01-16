#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能体子技能生成器
为各个智能体项目生成独立的 Claude 技能
"""

import sys
import codecs
import json
import shutil
from pathlib import Path

# Windows 终端编码修复
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# 工作区配置
WORKSPACE_ROOT = Path(r"c:\Users\flyskyson\Office_Agent_Workspace")
OUTPUT_DIR = WORKSPACE_ROOT / "05_Outputs" / "skills"

# 智能体配置
AGENTS = {
    "market-supervision-agent": {
        "path": "01_Active_Projects/market_supervision_agent",
        "name": "市场监管智能体",
        "description": "个体工商户开业申请书自动填写系统，支持OCR识别和Jinja2模板生成",
        "tech_stack": ["Flask", "Jinja2", "百度OCR", "PaddleOCR"],
        "entry": "ui/flask_app.py",
        "features": [
            "OCR识别营业执照",
            "自动填写申请书",
            "PDF生成",
            "模板管理"
        ]
    },
    "memory-agent": {
        "path": "01_Active_Projects/memory_agent",
        "name": "记忆助手",
        "description": "基于向量数据库的语义记忆存储和检索系统",
        "tech_stack": ["Streamlit", "ChromaDB", "sentence-transformers"],
        "entry": "ui/app.py",
        "features": [
            "语义记忆存储",
            "向量搜索",
            "间隔复习",
            "记忆统计"
        ]
    },
    "file-organizer": {
        "path": "01_Active_Projects/file_organizer",
        "name": "文件整理工具",
        "description": "智能文件分类和整理工具",
        "tech_stack": ["Python", "pathlib", "watchdog"],
        "entry": "file_organizer.py",
        "features": [
            "按类型整理",
            "按日期归档",
            "关键词分类",
            "自动监控"
        ]
    },
    "smart-tools": {
        "path": "01_Active_Projects/smart_tools",
        "name": "智能工具集",
        "description": "实用工具集合：新闻助手、工作流启动器、Markdown导出",
        "tech_stack": ["feedparser", "requests", "markdown"],
        "entry": None,
        "features": [
            "智能新闻推荐",
            "工作流模板",
            "Markdown导出"
        ]
    }
}

# 框架技能
FRAMEWORKS = {
    "workflow-engine": {
        "path": "00_Agent_Library/workflow_engine.py",
        "name": "工作流引擎",
        "description": "基于LangGraph的工作流编排引擎",
        "api": ["WorkflowEngine", "State", "workflow"],
        "features": [
            "状态图定义",
            "条件路由",
            "并行执行",
            "错误处理"
        ]
    },
    "agent-toolkit": {
        "path": "00_Agent_Library/agent_toolkit.py",
        "name": "AgentTool工具框架",
        "description": "智能体工具抽象层和装饰器系统",
        "api": ["AgentTool", "tool", "ToolRegistry"],
        "features": [
            "工具注册",
            "参数验证",
            "错误处理",
            "日志记录"
        ]
    },
    "claude-memory": {
        "path": "00_Agent_Library/claude_memory.py",
        "name": "Claude记忆系统",
        "description": "持久化记忆存储和检索系统",
        "api": ["ClaudeMemory", "remember", "recall", "recall_high_priority"],
        "features": [
            "上下文记忆",
            "决策记录",
            "对话历史",
            "优先级管理"
        ]
    }
}


def generate_agent_skill(agent_id: str, agent_config: dict):
    """生成单个智能体技能"""
    agent_dir = OUTPUT_DIR / agent_id
    agent_dir.mkdir(parents=True, exist_ok=True)

    # SKILL.md 内容
    skill_md = f"""# {agent_config['name']}

**类型**: 智能体项目
**技术栈**: {', '.join(agent_config['tech_stack'])}
**位置**: `{agent_config['path']}`

## 技能概述

{agent_config['description']}

## 核心功能
"""

    for feature in agent_config['features']:
        skill_md += f"- **{feature}**\n"

    skill_md += f"""
## 快速开始

"""
    if agent_config.get('entry'):
        skill_md += f"""### 启动服务
```bash
cd {agent_config['path']}
python {agent_config['entry']}
```
"""
    else:
        skill_md += f"""### 使用方式
```bash
cd {agent_config['path']}
python {agent_config['path'].split('/')[-1]}.py
```
"""

    skill_md += """
## 项目结构
"""

    # 扫描实际项目结构
    agent_path = WORKSPACE_ROOT / agent_config['path']
    if agent_path.exists():
        for item in sorted(agent_path.iterdir()):
            if item.is_dir() and not item.name.startswith('.') and item.name != '__pycache__':
                skill_md += f"- `{item.name}/` - 目录\n"
            elif item.is_file() and item.suffix in ['.py', '.md', '.yaml', '.json']:
                skill_md += f"- `{item.name}` - 文件\n"

    skill_md += f"""
## 技术细节

### 技术栈
"""
    for tech in agent_config['tech_stack']:
        skill_md += f"- **{tech}**\n"

    skill_md += """
### 配置文件
"""

    # 查找配置文件
    config_files = list(agent_path.glob("*.json")) + list(agent_path.glob("*.yaml")) + list(agent_path.glob("*.yml"))
    if config_files:
        for cfg in config_files:
            skill_md += f"- `{cfg.name}` - 配置文件\n"

    skill_md += """

## 使用场景

"""

    # 根据智能体类型添加使用场景
    if 'market' in agent_id:
        skill_md += """- 填写个体工商户开业申请书
- OCR识别营业执照信息
- 批量生成申请文档
"""
    elif 'memory' in agent_id:
        skill_md += """- 存储和检索语义记忆
- 间隔复习管理
- 知识库构建
"""
    elif 'file' in agent_id:
        skill_md += """- 自动整理下载文件夹
- 按类型归档文件
- 定期清理临时文件
"""
    elif 'smart' in agent_id:
        skill_md += """- 获取个性化新闻推荐
- 启动预定义工作流
- 导出记忆到Markdown
"""

    skill_md += """
## 相关链接

- [主技能](../office-agent-workspace/)
- [项目文档](../../../../docs/)
- [CLAUDE.md](../../../../CLAUDE.md)
"""

    # 写入 SKILL.md
    skill_file = agent_dir / "SKILL.md"
    with open(skill_file, 'w', encoding='utf-8') as f:
        f.write(skill_md)

    # 复制项目中的文档
    refs_dir = agent_dir / "references"
    refs_dir.mkdir(exist_ok=True)

    for doc_file in agent_path.rglob("*.md"):
        if not any(skip in str(doc_file) for skip in ['node_modules', '.git', '__pycache__', 'venv']):
            rel_path = doc_file.relative_to(agent_path)
            dest_file = refs_dir / rel_path
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(doc_file, dest_file)

    # 复制主要Python文件作为参考
    src_dir = refs_dir / "source"
    src_dir.mkdir(exist_ok=True)

    for py_file in agent_path.rglob("*.py"):
        if not any(skip in str(py_file) for skip in ['node_modules', '.git', '__pycache__', 'venv', 'test']):
            rel_path = py_file.relative_to(agent_path)
            dest_file = src_dir / rel_path
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            try:
                shutil.copy(py_file, dest_file)
            except:
                pass

    print(f"  ✅ {agent_config['name']} - {agent_id}")

    return agent_dir


def generate_framework_skill(fw_id: str, fw_config: dict):
    """生成框架技能"""
    fw_dir = OUTPUT_DIR / fw_id
    fw_dir.mkdir(parents=True, exist_ok=True)

    skill_md = f"""# {fw_config['name']}

**类型**: 核心框架
**位置**: `{fw_config['path']}`

## 技能概述

{fw_config['description']}

## 核心 API

"""

    for api in fw_config['api']:
        skill_md += f"- **{api}**\n"

    skill_md += """
## 主要功能

"""

    for feature in fw_config['features']:
        skill_md += f"- **{feature}**\n"

    skill_md += f"""

## 使用示例

### 导入
```python
from {fw_config['path'].replace('.py', '').replace('/', '.')} import {fw_config['api'][0]}
```

### 基本用法
```python
# 根据具体框架添加示例代码
# TODO: 添加实际使用示例
```

## 技术细节

### 架构设计
- 模块化设计
- 插件式扩展
- 统一接口

### 集成方式
- 可独立使用
- 可组合使用
- 支持自定义扩展

## 相关文档

- [架构设计](../../../../docs/ARCHITECTURE.md)
- [编码规范](../../../../docs/CODING_STANDARDS.md)
- [主技能](../office-agent-workspace/)
"""

    # 写入 SKILL.md
    skill_file = fw_dir / "SKILL.md"
    with open(skill_file, 'w', encoding='utf-8') as f:
        f.write(skill_md)

    # 复制源代码
    src_file = WORKSPACE_ROOT / fw_config['path']
    if src_file.exists():
        refs_dir = fw_dir / "references"
        refs_dir.mkdir(exist_ok=True)
        shutil.copy(src_file, refs_dir / "source.py")

    print(f"  ✅ {fw_config['name']} - {fw_id}")

    return fw_dir


def main():
    """主函数"""
    print("=" * 70)
    print("🤖 智能体子技能生成器")
    print("=" * 70)

    generated_skills = []

    # 生成智能体技能
    print("\n📦 生成智能体技能:")
    for agent_id, agent_config in AGENTS.items():
        try:
            skill_path = generate_agent_skill(agent_id, agent_config)
            generated_skills.append({
                "id": agent_id,
                "name": agent_config['name'],
                "path": str(skill_path),
                "type": "agent"
            })
        except Exception as e:
            print(f"  ❌ {agent_config['name']}: {e}")

    # 生成框架技能
    print("\n🔧 生成框架技能:")
    for fw_id, fw_config in FRAMEWORKS.items():
        try:
            skill_path = generate_framework_skill(fw_id, fw_config)
            generated_skills.append({
                "id": fw_id,
                "name": fw_config['name'],
                "path": str(skill_path),
                "type": "framework"
            })
        except Exception as e:
            print(f"  ❌ {fw_config['name']}: {e}")

    # 生成技能索引
    index = {
        "generated_at": "2026-01-16",
        "total_skills": len(generated_skills),
        "skills": generated_skills
    }

    index_file = OUTPUT_DIR / "skills_index.json"
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 70)
    print(f"✅ 子技能生成完成! 共 {len(generated_skills)} 个技能")
    print(f"📁 输出目录: {OUTPUT_DIR}")
    print(f"📋 技能索引: {index_file}")
    print("=" * 70)

    # 列出所有技能
    print("\n📋 生成的技能:")
    for skill in generated_skills:
        print(f"  - {skill['name']} ({skill['type']})")

    return 0


if __name__ == "__main__":
    sys.exit(main())
