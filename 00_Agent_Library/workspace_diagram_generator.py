#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工作区架构图生成器
使用 Diagrams 库生成 Office Agent Workspace 的完整架构图
"""

import sys
import codecs
from pathlib import Path

# Windows 终端编码修复
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')


def generate_simple_diagram():
    """生成简化的工作区架构图"""
    try:
        from diagrams import Diagram
        from diagrams.programming.framework import Flask, FastAPI
        from diagrams.programming.language import Python, JavaScript
        from diagrams.aws.storage import S3
        from diagrams.generic.database import SQL
        from diagrams.generic.storage import Storage

        print("🎨 正在生成工作区架构图...")

        # 获取工作区根目录
        workspace_root = Path(__file__).parent.parent
        output_dir = workspace_root / "05_Outputs"
        output_dir.mkdir(exist_ok=True)

        # 创建主架构图
        with Diagram("Office Agent Workspace - 系统架构",
                     direction="TB",
                     show=False,
                     filename=str(output_dir / "workspace_architecture")):

            # 用户交互层
            with Diagram("用户交互层", show=False):
                flask_ui = Flask("Flask Web UI")
                streamlit_ui = FastAPI("Streamlit UI")
                cli_tool = Python("CLI 启动器")

            # 业务逻辑层
            with Diagram("业务逻辑层", show=False):
                # 框架
                agent_toolkit = Python("AgentTool 框架")
                workflow_engine = Python("Workflow Engine")
                skill_system = Python("Skill System")

                # 智能体
                market_agent = Python("市场监管智能体")
                memory_agent = Python("记忆助手")
                file_tool = Python("文件整理工具")

            # 数据存储层
            with Diagram("数据存储层", show=False):
                file_system = Storage("文件系统")
                vector_db = S3("ChromaDB")
                config_files = SQL("YAML 配置")

            # 连接关系
            flask_ui >> agent_toolkit
            streamlit_ui >> workflow_engine
            cli_tool >> skill_system

            agent_toolkit >> market_agent
            workflow_engine >> memory_agent
            skill_system >> file_tool

            market_agent >> [file_system, config_files]
            memory_agent >> vector_db
            file_tool >> file_system

        print("✅ 主架构图已生成")
        print(f"   文件: {output_dir / 'workspace_architecture.gv.png'}")

        # 生成市场监管智能体架构图
        with Diagram("市场监管智能体架构",
                     direction="LR",
                     show=False,
                     filename=str(output_dir / "market_agent_architecture")):

            flask_app = Flask("flask_app.py")
            jinja2_filler = Python("jinja2_filler.py")

            ocr_module = Python("OCR 模块")
            template_engine = Python("Jinja2 模板引擎")
            doc_generator = Python("文档生成器")

            db_schema = SQL("database_schema.yaml")
            templates = Storage("Word 模板")

            flask_app >> jinja2_filler
            jinja2_filler >> [ocr_module, template_engine, doc_generator]
            [ocr_module, template_engine, doc_generator] >> [db_schema, templates]

        print("✅ 市场监管智能体架构图已生成")

        # 生成记忆助手架构图
        with Diagram("记忆助手架构",
                     direction="LR",
                     show=False,
                     filename=str(output_dir / "memory_agent_architecture")):

            streamlit_app = FastAPI("app.py")
            memory_core = Python("memory_agent.py")

            add_note = Python("笔记添加")
            search = Python("语义搜索")
            review = Python("间隔复习")

            chroma = S3("ChromaDB")

            streamlit_app >> memory_core
            memory_core >> [add_note, search, review]
            [add_note, search, review] >> chroma

        print("✅ 记忆助手架构图已生成")

        # 生成技能系统架构图
        with Diagram("技能系统架构",
                     direction="TB",
                     show=False,
                     filename=str(output_dir / "skill_system_architecture")):

            user_input = JavaScript("用户输入")
            trigger = Python("触发器")
            matcher = Python("技能匹配")
            loader = Python("加载器")
            executor = Python("执行器")
            validator = Python("验证器")
            output = JavaScript("返回结果")

            user_input >> trigger >> matcher >> loader >> executor >> validator >> output

        print("✅ 技能系统架构图已生成")

        print("\n" + "=" * 70)
        print("✅ 所有架构图生成完成！")
        print("=" * 70)
        print(f"输出目录: {output_dir}")
        print("\n生成的文件:")
        print(f"  1. workspace_architecture.gv.png")
        print(f"  2. market_agent_architecture.gv.png")
        print(f"  3. memory_agent_architecture.gv.png")
        print(f"  4. skill_system_architecture.gv.png")

        return True

    except ImportError as e:
        print(f"❌ 缺少依赖库: {e}")
        print("请运行: pip install diagrams")
        return False
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def generate_mermaid_summary():
    """生成 Mermaid 流程图总结"""
    mermaid_code = """
## 🎨 Mermaid 流程图总结

本工作区已全面升级为 Mermaid 流程图可视化！

### 已升级文档

#### 技能文档 (Skills)
1. ✅ **idea-to-product** - 想法落地技能
2. ✅ **super-butler** - 超级管家技能
3. ✅ **application-generator** - 申请书生成技能
4. ✅ **license-organizer** - 证照整理技能
5. ✅ **knowledge-indexer** - 知识索引技能
6. ✅ **skill-creator** - 技能创建技能

#### 架构文档 (Architecture)
1. ✅ **ARCHITECTURE.md** - 系统架构设计
   - 三层架构模型
   - 核心组件架构
   - 智能体架构
   - 数据流设计

### 使用方法

#### 在 VSCode 中预览
1. 安装扩展: "Mermaid Chart Preview"
2. 打开包含 Mermaid 代码的 Markdown 文件
3. 实时查看渲染效果

#### 在线预览
访问: https://mermaid.live
将 Mermaid 代码粘贴到编辑器中

#### 命令行渲染
```bash
# 安装工具
npm install -g @mermaid-js/mermaid-cli

# 渲染图片
mmdc -i input.md -o output.png
```

### 升级效果

#### Before (ASCII)
```
┌─────────────┐
│  用户输入   │
└──────┬──────┘
       ↓
```

#### After (Mermaid)
```mermaid
graph LR
    A[用户输入] --> B[处理]
    B --> C[输出]
```

### 颜色主题

所有流程图使用统一的配色方案:
- 🔵 蓝色 (#e1f5ff): 输入/开始
- 🟢 绿色 (#e8f5e9): 成功/完成
- 🟡 黄色 (#fff4e6): 处理中
- 🟠 橙色 (#fce4ec): 检查/验证
- 🟣 紫色 (#f3e5f5): 特殊操作

### 版本信息
- **升级日期**: 2026-01-16
- **Mermaid 版本**: 兼容 Mermaid 10.x
- **文档版本**: v2.0
"""

    print("\n" + "=" * 70)
    print("📚 Mermaid 升级总结")
    print("=" * 70)
    print(mermaid_code)

    workspace_root = Path(__file__).parent.parent
    summary_path = workspace_root / "05_Outputs" / "mermaid_upgrade_summary.md"

    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(mermaid_code)

    print(f"\n✅ 升级总结已保存到: {summary_path}")


if __name__ == "__main__":
    print("🚀 Office Agent Workspace 架构图生成器")
    print("=" * 70)

    # 生成架构图
    result = generate_simple_diagram()

    # 生成 Mermaid 总结
    generate_mermaid_summary()

    if result:
        print("\n" + "=" * 70)
        print("🎉 架构图生成完成！")
        print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print("⚠️  架构图生成失败，但 Mermaid 升级已完成")
        print("=" * 70)
