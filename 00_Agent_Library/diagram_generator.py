#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
流程图生成工具 - 演示版本
使用 Mermaid 生成精美流程图
"""

import sys
import codecs

# Windows 终端编码修复
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

def generate_mermaid_diagram():
    """生成 Mermaid 流程图"""
    mermaid_code = '''
graph TD
    A[用户输入] --> B{意图识别}

    B -->|触发技能| C[加载技能文档]
    B -->|无技能| D[智能推荐引擎]

    C --> E{执行技能步骤}
    D --> F[显示推荐工具]

    E --> G[完成任务]
    F --> G[启动工具]

    G --> H[记录到记忆系统]
    H --> I[更新用户偏好]

    I --> J[生成输出]

    style A fill:#e1f5ff
    style B fill:#fff4e6
    style C fill:#e8f5e9
    style D fill:#fff3e0
    style E fill:#ffe0b2
    style F fill:#e3f2fd
    style G fill:#e0f2f1
    style H fill:#fce4ec
    style I fill:#f3e5f1
    style J fill:#e8f6f3

    classDef success fill:#4caf50,stroke:#2e7d32
    classDef warning fill:#ff9800,stroke:#f57c00
    classDef info fill:#2196f3,stroke:#0d47a1

    class G,J success
    class A,B,C,D,E,F,H,I info
'''

    print("🎨 Mermaid 流程图代码:")
    print("=" * 70)
    print(mermaid_code)
    print("=" * 70)

    print("\n💡 使用方法:")
    print("1. 在 Markdown 文件中使用")
    print("2. 在 VSCode 中使用 Mermaid 预览")
    print("3. 在线渲染: https://mermaid.live")
    print("4. 本地渲染: pip install mmdc && mmdc render input.mmd")

    return mermaid_code

def generate_diagrams_example():
    """展示 Diagrams 库的使用"""
    try:
        from diagrams import Diagram
        from diagrams.programming.framework import FastAPI
        from diagrams.aws.storage import S3

        print("\n🎨 Diagrams 流程图示例:")
        print("=" * 70)

        # 生成架构图
        graph = Diagram("Office Agent Workspace", show=False)

        with graph:
            s3 = S3("工作区数据")
            fastapi = FastAPI("市场监管智能体")

            s3 >> fastapi

        print("✅ Diagrams 架构图已生成")
        print("   文件: office_agent_workspace.gv")
        print("   命令: dot -Tpng office_agent_workspace.gv -o output.png")

    except ImportError:
        print("\n⚠️  Diagrams 库未安装")
        print("   安装: pip install diagrams")

if __name__ == "__main__":
    generate_mermaid_diagram()
    generate_diagrams_example()
    print("\n" + "=" * 70)
    print("✅ 流程图生成演示完成！")
    print("=" * 70)