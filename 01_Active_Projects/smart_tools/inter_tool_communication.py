#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具间实际通信演示 - 实现高优先级任务

场景：用户提交个体工商户开业申请
流程：
1. file_organizer 整理上传的材料
2. application_generator 识别并生成申请书
3. memory_agent 存储本次记录供后续查询

作者: Claude Code
日期: 2026-01-17
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, List

# Windows 终端编码修复
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# 添加路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "00_Agent_Library"))
from workflow_engine import WorkflowGraph, Node, State, END

# ============================================================================
# 工作流节点实现
# ============================================================================

class FileOrganizerNode(Node):
    """文件整理节点"""

    def __init__(self):
        super().__init__("organize", "智能整理证照材料")

    def execute(self, state: State) -> State:
        """执行文件整理"""
        files = state['data'].get('files', [])
        print(f"  [FileOrganizer] 收到 {len(files)} 个文件")

        # 模拟文件整理
        organized = {
            'license': [f for f in files if '营业执照' in f],
            'id_card': [f for f in files if '身份证' in f],
            'photos': [f for f in files if '照片' in f],
            'other': []
        }

        print(f"  [FileOrganizer] 整理完成:")
        print(f"    - 营业执照: {len(organized['license'])} 个")
        print(f"    - 身份证: {len(organized['id_card'])} 个")
        print(f"    - 照片: {len(organized['photos'])} 个")

        # 传递给下一个节点
        state['data']['organized_files'] = organized
        return state


class ApplicationGeneratorNode(Node):
    """申请书生成节点"""

    def __init__(self):
        super().__init__("generate", "OCR识别 + Word模板填充")

    def execute(self, state: State) -> State:
        """执行申请书生成"""
        organized_files = state['data'].get('organized_files', {})

        print(f"  [ApplicationGenerator] 收到整理后的文件")

        # 模拟 OCR 识别和申请书生成
        license_info = {
            'name': '张三',
            'shop_name': '示例便利店',
            'address': '示例街道123号',
            'business_scope': '日用百货销售'
        }

        print(f"  [ApplicationGenerator] OCR识别完成:")
        print(f"    - 经营者: {license_info['name']}")
        print(f"    - 店铺名称: {license_info['shop_name']}")
        print(f"    - 经营地址: {license_info['address']}")

        # 生成申请书
        application = {
            'type': '个体工商户开业申请书',
            'content': license_info,
            'generated_at': '2026-01-17'
        }

        print(f"  [ApplicationGenerator] 申请书生成完成")

        # 传递给下一个节点
        state['data']['application'] = application
        state['data']['license_info'] = license_info
        return state


class MemoryAgentNode(Node):
    """记忆存储节点"""

    def __init__(self):
        super().__init__("memory", "知识管理 + 语义搜索")

    def execute(self, state: State) -> State:
        """执行记忆存储"""
        application = state['data'].get('application', {})
        license_info = state['data'].get('license_info', {})

        print(f"  [MemoryAgent] 存储本次申请记录")

        # 构建记忆内容
        memory = {
            'topic': f'个体工商户申请 - {license_info.get("shop_name", "未知")}',
            'summary': f'经营者 {license_info.get("name", "未知")} 申请开设 {license_info.get("shop_name", "未知")}',
            'key_points': [
                f'店铺名称: {license_info.get("shop_name")}',
                f'经营地址: {license_info.get("address")}',
                f'经营范围: {license_info.get("business_scope")}'
            ],
            'timestamp': '2026-01-17',
            'tags': ['个体工商户', '申请', '市场监管']
        }

        print(f"  [MemoryAgent] 记忆已存储:")
        print(f"    - 主题: {memory['topic']}")
        print(f"    - 标签: {', '.join(memory['tags'])}")

        # 保存结果
        state['data']['memory'] = memory
        return state


# ============================================================================
# 工作流编排
# ============================================================================

class InterToolWorkflow:
    """工具间通信工作流"""

    def __init__(self):
        # 创建节点
        self.organize_node = FileOrganizerNode()
        self.generate_node = ApplicationGeneratorNode()
        self.memory_node = MemoryAgentNode()

        # 创建工作流
        self.workflow = self._build_workflow()

    def _build_workflow(self) -> WorkflowGraph:
        """构建工作流图"""
        wf = WorkflowGraph("inter_tool_communication", enable_checkpoints=True)

        # 添加节点 (name, node)
        wf.add_node("organize", self.organize_node)
        wf.add_node("generate", self.generate_node)
        wf.add_node("memory", self.memory_node)

        # 设置入口
        wf.set_entry_point("organize")

        # 定义边（工具间通信路径）
        # organize → generate → memory → END
        wf.add_edge("organize", "generate")
        wf.add_edge("generate", "memory")
        wf.add_edge("memory", END)

        return wf

    def run(self, files: List[str]) -> Dict:
        """运行工作流"""
        print("\n" + "=" * 60)
        print("🔗 工具间实际通信演示")
        print("=" * 60)
        print(f"📋 输入文件: {len(files)} 个")
        for f in files:
            print(f"   - {f}")

        print("\n🚀 开始执行工作流...\n")

        # 初始数据（State 结构）
        initial_data = {'files': files}

        # 编译并执行工作流
        compiled = self.workflow.compile()
        final_state = compiled.invoke(initial_data)

        print("\n" + "=" * 60)
        print("📊 执行结果")
        print("=" * 60)
        print(f"✅ 工作流完成")

        # 安全访问状态
        data = final_state.get('data', {})
        if 'memory' in data:
            print(f"💾 已存储记忆: {data['memory']['topic']}")
        if 'application' in data:
            print(f"📄 已生成申请: {data['application']['type']}")
        if 'organized_files' in data:
            organized = data['organized_files']
            print(f"📁 整理结果: 营业执照({len(organized['license'])}) 身份证({len(organized['id_card'])}) 照片({len(organized['photos'])})")

        # 显示检查点统计
        if self.workflow.checkpoint_manager:
            stats = self.workflow.checkpoint_manager.get_stats()
            print(f"\n📈 检查点统计: {stats['total_checkpoints']} 个, {stats['total_size_mb']} MB")

        return final_state


# ============================================================================
# 主程序
# ============================================================================

def main():
    """主函数"""
    # 模拟用户上传的文件
    test_files = [
        "营业执照.jpg",
        "身份证正面.jpg",
        "身份证反面.jpg",
        "经营者照片.jpg"
    ]

    # 创建并运行工作流
    workflow = InterToolWorkflow()
    result = workflow.run(test_files)

    print("\n" + "=" * 60)
    print("🎯 工具间通信演示完成！")
    print("=" * 60)
    print("\n✅ 实现的功能:")
    print("   1. file_organizer → application_generator (文件传递)")
    print("   2. application_generator → memory_agent (数据传递)")
    print("   3. 完整的三工具协作工作流")
    print("\n💡 下一步:")
    print("   - 集成真实的工具实现")
    print("   - 添加错误处理和重试")
    print("   - 实现异步通信")
    print("   - 添加工作流可视化")

if __name__ == "__main__":
    main()
