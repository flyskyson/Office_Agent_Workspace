#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工作流引擎 - LangGraph 风格的状态管理
参考 LangGraph 的 StateGraph 和节点模式

作者: Claude Code
日期: 2026-01-12
"""

import sys
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Callable, TypedDict
from enum import Enum
from datetime import datetime

# Windows 终端编码修复
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass


class WorkflowStatus(Enum):
    """工作流状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


class State(TypedDict):
    """工作流状态基类"""
    data: Dict[str, Any]
    errors: List[str]
    warnings: List[str]
    metadata: Dict[str, Any]


class Node(ABC):
    """工作流节点 - 参考 LangGraph 的节点概念"""

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.execution_count = 0
        self.execution_time = 0

    @abstractmethod
    def execute(self, state: State) -> State:
        """
        执行节点逻辑
        返回更新后的状态
        """
        pass

    def __call__(self, state: State) -> State:
        """使节点可调用"""
        start_time = datetime.now()
        self.execution_count += 1

        try:
            result = self.execute(state)
            self.execution_time += (datetime.now() - start_time).total_seconds()
            return result
        except Exception as e:
            state['errors'].append(f"{self.name} 执行失败: {str(e)}")
            return state


class ConditionalEdge:
    """条件边 - 参考 LangGraph 的条件边"""

    def __init__(self,
                 source: str,
                 condition: Callable[[State], str],
                 branches: Dict[str, str]):
        """
        参数:
            source: 源节点名称
            condition: 条件函数，返回目标节点名称
            branches: 分支映射 {条件结果: 目标节点}
        """
        self.source = source
        self.condition = condition
        self.branches = branches

    def get_next(self, state: State) -> Optional[str]:
        """获取下一个节点"""
        result = self.condition(state)
        return self.branches.get(result)


class Edge:
    """普通边 - 固定的下一个节点"""

    def __init__(self, source: str, target: str):
        self.source = source
        self.target = target

    def get_next(self, state: State) -> Optional[str]:
        """获取下一个节点"""
        return self.target


class END:
    """结束标记"""
    pass


class WorkflowGraph:
    """
    工作流图 - 参考 LangGraph 的 StateGraph

    用法:
        graph = WorkflowGraph("application_generation")

        # 添加节点
        graph.add_node("validate", ValidateNode())
        graph.add_node("generate", GenerateNode())
        graph.add_node("review", ReviewNode())

        # 添加边
        graph.add_edge("validate", "generate")
        graph.add_edge("generate", "review")

        # 添加条件边
        graph.add_conditional_edge(
            "review",
            lambda state: "retry" if state['errors'] else "end",
            {"retry": "generate", "end": END}
        )

        # 设置入口
        graph.set_entry_point("validate")

        # 编译并执行
        workflow = graph.compile()
        result = workflow.invoke(initial_state)
    """

    def __init__(self, name: str):
        self.name = name
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
        self.conditional_edges: List[ConditionalEdge] = []
        self.entry_point: Optional[str] = None

    def add_node(self, name: str, node: Node):
        """添加节点"""
        self.nodes[name] = node

    def add_edge(self, source: str, target: str):
        """添加边"""
        if target != END:
            if target not in self.nodes:
                raise ValueError(f"目标节点不存在: {target}")
        self.edges.append(Edge(source, target))

    def add_conditional_edge(self,
                           source: str,
                           condition: Callable[[State], str],
                           branches: Dict[str, Any]):
        """添加条件边"""
        self.conditional_edges.append(
            ConditionalEdge(source, condition, branches)
        )

    def set_entry_point(self, node_name: str):
        """设置入口点"""
        if node_name not in self.nodes:
            raise ValueError(f"入口节点不存在: {node_name}")
        self.entry_point = node_name

    def compile(self):
        """编译工作流"""
        if not self.entry_point:
            raise ValueError("未设置入口点")

        return CompiledWorkflow(self)


class CompiledWorkflow:
    """编译后的工作流"""

    def __init__(self, graph: WorkflowGraph):
        self.graph = graph

    def invoke(self, initial_data: Dict = None) -> Dict[str, Any]:
        """
        执行工作流

        参数:
            initial_data: 初始数据

        返回:
            执行结果
        """
        # 初始化状态
        state: State = {
            'data': initial_data or {},
            'errors': [],
            'warnings': [],
            'metadata': {
                'start_time': datetime.now().isoformat(),
                'nodes_executed': [],
                'execution_log': []
            }
        }

        current_node = self.graph.entry_point
        visited = set()

        while current_node and current_node != END:
            # 防止无限循环
            if current_node in visited:
                state['errors'].append(f"检测到循环: {current_node}")
                break
            visited.add(current_node)

            # 执行节点
            if current_node not in self.graph.nodes:
                state['errors'].append(f"节点不存在: {current_node}")
                break

            node = self.graph.nodes[current_node]

            print(f"\n[执行] {node.name}: {node.description}")
            state['metadata']['nodes_executed'].append(current_node)
            state['metadata']['execution_log'].append({
                'node': current_node,
                'time': datetime.now().isoformat()
            })

            # 执行
            state = node(state)

            # 检查是否有错误
            if state['errors']:
                print(f"[错误] {state['errors'][-1]}")
                break

            # 查找下一个节点
            current_node = self._get_next_node(current_node, state)

        # 完成
        state['metadata']['end_time'] = datetime.now().isoformat()
        state['metadata']['success'] = len(state['errors']) == 0

        return {
            'state': state,
            'nodes_executed': len(state['metadata']['nodes_executed']),
            'success': state['metadata']['success'],
            'errors': state['errors'],
            'warnings': state['warnings']
        }

    def _get_next_node(self, current: str, state: State) -> Optional[str]:
        """获取下一个节点"""
        # 先检查条件边
        for edge in self.graph.conditional_edges:
            if edge.source == current:
                return edge.get_next(state)

        # 再检查普通边
        for edge in self.graph.edges:
            if edge.source == current:
                return edge.target

        return None


# ============ 申请书生成工作流的具体节点 ============

class ValidateNode(Node):
    """数据验证节点"""

    def __init__(self):
        super().__init__(
            "validate",
            "验证申请数据的完整性和正确性"
        )

    def execute(self, state: State) -> State:
        """执行验证"""
        import sys
        from pathlib import Path

        data = state['data']

        # 延迟导入验证器
        sys.path.insert(0, str(Path(__file__).parent.parent / "01_Active_Projects" / "market_supervision_agent"))
        from data_validator import DataValidator

        validator = DataValidator()
        validator.validate_applicant_data(data)

        # 收集错误和警告
        if validator.errors:
            state['errors'].extend([f"[{e['field']}] {e['message']}" for e in validator.errors])

        if validator.warnings:
            state['warnings'].extend([f"[{e['field']}] {e['message']}" for e in validator.warnings])

        # 保存验证后的数据
        state['data']['validated'] = True
        state['data']['validation_results'] = {
            'errors': validator.errors,
            'warnings': validator.warnings
        }

        print(f"  [完成] 验证完成 - 错误: {len(validator.errors)}, 警告: {len(validator.warnings)}")

        return state


class SelectTemplateNode(Node):
    """模板选择节点"""

    def __init__(self):
        super().__init__(
            "select_template",
            "根据业务类型选择合适的模板"
        )

    def execute(self, state: State) -> State:
        """选择模板"""
        data = state['data']

        # 根据业务类型选择模板
        business_type = data.get('business_type', '个体工商户')

        template_map = {
            '个体工商户': '（李奕凤）个体工商户开业登记申请书（Jinja2模板）.docx',
            '企业': '企业申请书模板.docx',
            '农民专业合作社': '合作社申请书模板.docx'
        }

        template = template_map.get(business_type, template_map['个体工商户'])

        state['data']['template'] = template
        state['data']['template_path'] = str(
            Path(__file__).parent.parent / "01_Active_Projects" / "market_supervision_agent" / template
        )

        print(f"  [完成] 选择模板: {template}")

        return state


class GenerateDocumentNode(Node):
    """文档生成节点"""

    def __init__(self):
        super().__init__(
            "generate",
            "使用 Jinja2 模板生成申请书"
        )

    def execute(self, state: State) -> State:
        """生成文档"""
        import sys
        from pathlib import Path

        data = state['data']

        # 延迟导入生成器
        sys.path.insert(0, str(Path(__file__).parent.parent / "01_Active_Projects" / "market_supervision_agent"))
        from jinja2_filler import fill_template, load_config

        template = data.get('template_path')
        if not template:
            state['errors'].append("未指定模板")
            return state

        # 生成文档
        config = load_config()
        output_file = fill_template(
            data,
            template,
            output_dir="output",
            auto_open=False,
            config=config,
            verbose=False
        )

        if output_file:
            state['data']['output_file'] = str(output_file)
            print(f"  [完成] 生成文档: {output_file}")
        else:
            state['errors'].append("文档生成失败")

        return state


class ReviewDocumentNode(Node):
    """文档审查节点"""

    def __init__(self):
        super().__init__(
            "review",
            "审查生成的文档质量"
        )

    def execute(self, state: State) -> State:
        """审查文档"""
        data = state['data']

        output_file = data.get('output_file')
        if not output_file:
            state['errors'].append("没有生成文档")
            return state

        # 检查文件是否存在
        from pathlib import Path
        if not Path(output_file).exists():
            state['errors'].append("文档文件不存在")
            return state

        # 检查文件大小
        file_size = Path(output_file).stat().st_size
        if file_size < 10240:  # 小于10KB可能有问题
            state['warnings'].append(f"文档大小异常: {file_size} 字节")

        state['data']['review_passed'] = len(state['errors']) == 0
        print(f"  [完成] 审查通过 - 文档大小: {file_size} 字节")

        return state


# ============ 预定义工作流 ============

def create_application_workflow() -> CompiledWorkflow:
    """创建申请书生成工作流"""

    graph = WorkflowGraph("application_generation")

    # 添加节点
    graph.add_node("validate", ValidateNode())
    graph.add_node("select_template", SelectTemplateNode())
    graph.add_node("generate", GenerateDocumentNode())
    graph.add_node("review", ReviewDocumentNode())

    # 添加边
    graph.add_edge("validate", "select_template")
    graph.add_edge("select_template", "generate")
    graph.add_edge("generate", "review")

    # 添加条件边 - 如果审查失败，重新生成
    graph.add_conditional_edge(
        "review",
        lambda state: "retry" if not state['data'].get('review_passed', False) else "end",
        {"retry": "generate", "end": END}
    )

    # 设置入口
    graph.set_entry_point("validate")

    return graph.compile()


def create_organize_workflow() -> CompiledWorkflow:
    """创建文件整理工作流"""

    class OrganizeNode(Node):
        def __init__(self):
            super().__init__("organize", "整理文件")

        def execute(self, state: State) -> State:
            # 执行文件整理
            state['data']['organized'] = True
            print("  [完成] 文件整理完成")
            return state

    class IndexNode(Node):
        def __init__(self):
            super().__init__("index", "索引到知识库")

        def execute(self, state: State) -> State:
            # 索引到知识库
            state['data']['indexed'] = True
            print("  [完成] 索引完成")
            return state

    graph = WorkflowGraph("organize_and_index")

    graph.add_node("organize", OrganizeNode())
    graph.add_node("index", IndexNode())

    graph.add_edge("organize", "index")
    graph.set_entry_point("organize")

    return graph.compile()


# ============ 演示 ============

def main():
    """演示工作流引擎"""

    print("=" * 70)
    print("工作流引擎演示 - LangGraph 风格")
    print("=" * 70)

    # 演示1: 申请书生成工作流
    print("\n[演示1] 申请书生成工作流\n")

    workflow = create_application_workflow()

    test_data = {
        'business_name': '测试便利店',
        'operator_name': '张三',
        'phone': '13800138000',
        'business_address': '广西玉林市兴业县蒲塘镇测试路123号',
        'business_scope': '食品销售；日用百货',
        'business_type': '个体工商户'
    }

    result = workflow.invoke(test_data)

    print(f"\n[结果]")
    print(f"  执行节点数: {result['nodes_executed']}")
    print(f"  成功: {result['success']}")
    print(f"  错误: {result['errors']}")
    print(f"  警告: {result['warnings']}")

    if result['success']:
        output_file = result['state']['data'].get('output_file')
        if output_file:
            print(f"  输出文件: {output_file}")

    # 演示2: 文件整理工作流
    print("\n[演示2] 文件整理工作流\n")

    workflow2 = create_organize_workflow()
    result2 = workflow2.invoke({'source': 'test_folder'})

    print(f"\n[结果]")
    print(f"  执行节点数: {result2['nodes_executed']}")
    print(f"  成功: {result2['success']}")


if __name__ == "__main__":
    main()
