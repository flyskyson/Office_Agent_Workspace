#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工作流引擎 - LangGraph 风格的状态管理
参考 LangGraph 的 StateGraph 和节点模式

作者: Claude Code
日期: 2026-01-12
"""

import sys
import json
import uuid
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable, TypedDict
from enum import Enum
from datetime import datetime
from copy import deepcopy

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


# ============================================================================
# 检查点管理器 - LangGraph 风格的状态快照
# ============================================================================

class CheckpointManager:
    """
    检查点管理器 - 保存和恢复工作流状态

    功能:
    1. 在每个节点执行后保存状态快照
    2. 支持从任意检查点恢复执行
    3. 维护执行历史和时间线
    4. 持久化到文件系统

    用法:
        manager = CheckpointManager("my_workflow")
        checkpoint_id = manager.save(state, current_node="process")
        restored_state = manager.load(checkpoint_id)
        history = manager.list_history()
    """

    def __init__(self, workflow_id: str, storage_path: Path = None):
        """
        初始化检查点管理器

        参数:
            workflow_id: 工作流唯一标识
            storage_path: 存储路径，默认为工作区记忆目录
        """
        self.workflow_id = workflow_id

        if storage_path is None:
            # 默认存储到工作区记忆目录
            storage_path = Path(__file__).parent.parent / "06_Learning_Journal" / "workspace_memory" / "checkpoints"

        self.storage_path = storage_path / workflow_id
        self.storage_path.mkdir(parents=True, exist_ok=True)

        # 检查点索引
        self.index_file = self.storage_path / "index.jsonl"
        self.checkpoints: Dict[str, Dict] = {}
        self._load_index()

    def _load_index(self):
        """加载检查点索引"""
        if self.index_file.exists():
            try:
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            cp = json.loads(line)
                            self.checkpoints[cp['id']] = cp
            except Exception as e:
                print(f"⚠️  加载检查点索引失败: {e}")

    def _save_index(self):
        """保存检查点索引（追加模式）"""
        # 索引是追加写入的，不需要每次重写
        pass

    def save(self, state: State, current_node: str, metadata: Dict = None) -> str:
        """
        保存检查点

        参数:
            state: 当前工作流状态
            current_node: 当前执行的节点
            metadata: 额外的元数据

        返回:
            检查点ID
        """
        checkpoint_id = str(uuid.uuid4())

        # 深拷贝状态，避免后续修改影响检查点
        state_copy = deepcopy(state)

        checkpoint = {
            "id": checkpoint_id,
            "workflow_id": self.workflow_id,
            "timestamp": datetime.now().isoformat(),
            "current_node": current_node,
            "state": state_copy,
            "metadata": metadata or {}
        }

        # 保存到文件
        checkpoint_file = self.storage_path / f"{checkpoint_id}.json"
        with open(checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(checkpoint, f, ensure_ascii=False, indent=2, default=str)

        # 更新索引
        self.checkpoints[checkpoint_id] = checkpoint
        with open(self.index_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(checkpoint, ensure_ascii=False, default=str) + '\n')

        return checkpoint_id

    def load(self, checkpoint_id: str) -> Optional[Dict]:
        """
        加载检查点

        参数:
            checkpoint_id: 检查点ID

        返回:
            检查点数据，如果不存在返回None
        """
        if checkpoint_id not in self.checkpoints:
            return None

        return self.checkpoints[checkpoint_id]

    def list_history(self, limit: int = None) -> List[Dict]:
        """
        列出检查点历史

        参数:
            limit: 限制返回数量

        返回:
            检查点列表（按时间倒序）
        """
        checkpoints = list(self.checkpoints.values())
        checkpoints.sort(key=lambda x: x['timestamp'], reverse=True)

        if limit:
            checkpoints = checkpoints[:limit]

        return checkpoints

    def get_latest(self) -> Optional[Dict]:
        """获取最新的检查点"""
        history = self.list_history(limit=1)
        return history[0] if history else None

    def get_state_at(self, checkpoint_id: str) -> Optional[State]:
        """获取指定检查点的状态"""
        checkpoint = self.load(checkpoint_id)
        return checkpoint['state'] if checkpoint else None

    def clear_old_checkpoints(self, keep_last: int = 10):
        """
        清理旧检查点，只保留最近的N个

        参数:
            keep_last: 保留最近多少个检查点
        """
        history = self.list_history()

        if len(history) <= keep_last:
            return

        # 删除旧检查点
        to_delete = history[keep_last:]
        for checkpoint in to_delete:
            checkpoint_id = checkpoint['id']
            checkpoint_file = self.storage_path / f"{checkpoint_id}.json"

            if checkpoint_file.exists():
                checkpoint_file.unlink()

            del self.checkpoints[checkpoint_id]

        # 重建索引
        with open(self.index_file, 'w', encoding='utf-8') as f:
            for checkpoint in self.checkpoints.values():
                f.write(json.dumps(checkpoint, ensure_ascii=False, default=str) + '\n')

    def get_stats(self) -> Dict:
        """获取检查点统计信息"""
        history = self.list_history()

        total_size = 0
        for checkpoint_file in self.storage_path.glob("*.json"):
            if checkpoint_file.name != "index.jsonl":
                total_size += checkpoint_file.stat().st_size

        return {
            "workflow_id": self.workflow_id,
            "total_checkpoints": len(history),
            "storage_path": str(self.storage_path),
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / 1024 / 1024, 2),
            "oldest": history[-1]['timestamp'] if history else None,
            "newest": history[0]['timestamp'] if history else None
        }


# ============================================================================
# 工作流可视化器 - 生成流程图
# ============================================================================

class WorkflowVisualizer:
    """
    工作流可视化器 - 生成多种格式的流程图

    支持格式:
    1. Mermaid - Markdown友好的图表语法
    2. Graphviz DOT - 专业图表工具
    3. ASCII - 终端直接显示
    4. HTML - 交互式SVG图表

    用法:
        visualizer = WorkflowVisualizer(graph)
        print(visualizer.to_mermaid())
        print(visualizer.to_ascii())
        visualizer.save_html("workflow.html")
    """

    def __init__(self, graph: 'WorkflowGraph'):
        """
        初始化可视化器

        参数:
            graph: WorkflowGraph 实例
        """
        self.graph = graph

    def to_mermaid(self, direction: str = "TD") -> str:
        """
        生成 Mermaid 图表

        参数:
            direction: 图表方向 (TD=自上而下, LR=自左向右)

        返回:
            Mermaid 代码字符串
        """
        lines = []
        lines.append(f"graph {direction}")
        lines.append("")

        # 添加节点
        for node_name, node in self.graph.nodes.items():
            label = node.name
            # 使用圆角矩形表示节点
            lines.append(f"    {node_name}[{label}]")

        # 添加开始/结束标记
        if self.graph.entry_point:
            lines.append(f"    START([开始]) --> {self.graph.entry_point}")

        # 添加普通边
        for edge in self.graph.edges:
            if edge.target == END:
                lines.append(f"    {edge.source} --> END([结束])")
            else:
                lines.append(f"    {edge.source} --> {edge.target}")

        # 添加条件边
        for edge in self.graph.conditional_edges:
            # 添加条件标签
            for condition_result, target in edge.branches.items():
                if target == END:
                    lines.append(f"    {edge.source} -->|{condition_result}| END([结束])")
                else:
                    lines.append(f"    {edge.source} -->|{condition_result}| {target}")

        return "\n".join(lines)

    def to_graphviz(self, direction: str = "TD") -> str:
        """
        生成 Graphviz DOT 代码

        参数:
            direction: 图表方向

        返回:
            DOT 代码字符串
        """
        dir_map = {"TD": "TB", "LR": "LR"}
        dot_direction = dir_map.get(direction, "TB")

        lines = []
        lines.append("digraph Workflow {")
        lines.append(f"    rankdir={dot_direction};")
        lines.append("    node [shape=box, style=rounded];")
        lines.append("")

        # 添加节点
        for node_name, node in self.graph.nodes.items():
            label = node.name
            lines.append(f'    {node_name} [label="{label}"];')

        # 添加开始/结束
        lines.append('    START [shape=ellipse, label="开始"];')
        lines.append('    END [shape=ellipse, label="结束"];')
        lines.append("")

        # 添加边
        if self.graph.entry_point:
            lines.append(f"    START -> {self.graph.entry_point};")

        for edge in self.graph.edges:
            if edge.target == END:
                lines.append(f"    {edge.source} -> END;")
            else:
                lines.append(f"    {edge.source} -> {edge.target};")

        # 添加条件边（带标签）
        for edge in self.graph.conditional_edges:
            for condition_result, target in edge.branches.items():
                if target == END:
                    lines.append(f'    {edge.source} -> END [label="{condition_result}"];')
                else:
                    lines.append(f'    {edge.source} -> {target} [label="{condition_result}"];')

        lines.append("}")

        return "\n".join(lines)

    def to_ascii(self) -> str:
        """
        生成 ASCII 艺术流程图

        返回:
            ASCII 图表字符串
        """
        lines = []
        lines.append("工作流: " + self.graph.name)
        lines.append("=" * 50)

        # 构建节点映射
        node_map = {}
        for node_name, node in self.graph.nodes.items():
            node_map[node_name] = node.name

        # 显示流程
        if self.graph.entry_point:
            current = self.graph.entry_point
            lines.append(f"\n[开始]")

            visited = set()
            while current and current not in visited:
                if current == END:
                    lines.append("[结束]")
                    break

                visited.add(current)

                if current in node_map:
                    lines.append(f"  ↓")
                    lines.append(f"[{node_map[current]}]")

                # 查找下一个节点
                next_node = None
                for edge in self.graph.edges:
                    if edge.source == current:
                        next_node = edge.target
                        break

                if not next_node:
                    # 检查条件边
                    for edge in self.graph.conditional_edges:
                        if edge.source == current:
                            conditions = ", ".join(edge.branches.keys())
                            lines.append(f"  ↓ (条件: {conditions})")
                            # 只显示第一个分支
                            for target in edge.branches.values():
                                next_node = target
                                break

                current = next_node if current != visited else None

        return "\n".join(lines)

    def save_html(self, filename: str, direction: str = "TD"):
        """
        保存为交互式HTML文件

        参数:
            filename: 输出文件名
            direction: 图表方向
        """
        mermaid_code = self.to_mermaid(direction)

        html_template = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>工作流: {self.graph.name}</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        body {{
            font-family: 'Microsoft YaHei', sans-serif;
            margin: 20px;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid #4CAF50;
            padding-bottom: 10px;
        }}
        .mermaid {{
            background: #fafafa;
            padding: 20px;
            border-radius: 4px;
            margin: 20px 0;
        }}
        .info {{
            background: #e3f2fd;
            padding: 15px;
            border-radius: 4px;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 工作流: {self.graph.name}</h1>
        <div class="info">
            <strong>节点数量:</strong> {len(self.graph.nodes)} |
            <strong>边数量:</strong> {len(self.graph.edges) + len(self.graph.conditional_edges)} |
            <strong>入口:</strong> {self.graph.entry_point or "未设置"}
        </div>
        <h2>流程图</h2>
        <div class="mermaid">
{mermaid_code}
        </div>
    </div>
    <script>
        mermaid.initialize({{startOnLoad: true}});
    </script>
</body>
</html>"""

        output_path = Path(filename)
        output_path.write_text(html_template, encoding='utf-8')
        return str(output_path)

    def print_summary(self):
        """打印工作流摘要"""
        print(f"\n{'='*60}")
        print(f"工作流摘要: {self.graph.name}")
        print(f"{'='*60}")
        print(f"节点数量: {len(self.graph.nodes)}")
        print(f"边数量: {len(self.graph.edges)}")
        print(f"条件边数量: {len(self.graph.conditional_edges)}")
        print(f"入口节点: {self.graph.entry_point or '未设置'}")
        print(f"\n节点列表:")
        for name, node in self.graph.nodes.items():
            print(f"  - {name}: {node.description}")
        print(f"{'='*60}\n")


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

    def __init__(self, name: str, enable_checkpoints: bool = False, enable_visualization: bool = False):
        """
        初始化工作流图

        参数:
            name: 工作流名称
            enable_checkpoints: 是否启用检查点功能
            enable_visualization: 是否启用可视化功能
        """
        self.name = name
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
        self.conditional_edges: List[ConditionalEdge] = []
        self.entry_point: Optional[str] = None

        # 新增功能
        self.enable_checkpoints = enable_checkpoints
        self.enable_visualization = enable_visualization

        # 检查点管理器
        self.checkpoint_manager: Optional[CheckpointManager] = None
        if enable_checkpoints:
            self.checkpoint_manager = CheckpointManager(workflow_id=name)

        # 可视化器
        self.visualizer: Optional[WorkflowVisualizer] = None
        if enable_visualization:
            self.visualizer = WorkflowVisualizer(self)

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

    # ========== 新增：便捷方法 ==========

    def visualize(self, format: str = "mermaid", direction: str = "TD") -> str:
        """
        生成工作流可视化图

        参数:
            format: 格式类型 (mermaid, graphviz, ascii)
            direction: 图表方向 (TD=自上而下, LR=自左向右)

        返回:
            图表字符串
        """
        if not self.visualizer:
            self.visualizer = WorkflowVisualizer(self)

        if format == "mermaid":
            return self.visualizer.to_mermaid(direction)
        elif format == "graphviz":
            return self.visualizer.to_graphviz(direction)
        elif format == "ascii":
            return self.visualizer.to_ascii()
        else:
            raise ValueError(f"不支持的格式: {format}")

    def save_visualization(self, filename: str, format: str = "html"):
        """
        保存可视化图表到文件

        参数:
            filename: 输出文件名
            format: 文件格式 (html, mermaid, dot)
        """
        if not self.visualizer:
            self.visualizer = WorkflowVisualizer(self)

        if format == "html":
            return self.visualizer.save_html(filename)
        elif format == "mermaid":
            mermaid_code = self.visualizer.to_mermaid()
            Path(filename).write_text(mermaid_code, encoding='utf-8')
            return str(Path(filename))
        elif format == "dot":
            dot_code = self.visualizer.to_graphviz()
            Path(filename).write_text(dot_code, encoding='utf-8')
            return str(Path(filename))
        else:
            raise ValueError(f"不支持的格式: {format}")

    def print_summary(self):
        """打印工作流摘要"""
        if not self.visualizer:
            self.visualizer = WorkflowVisualizer(self)
        self.visualizer.print_summary()

    def get_checkpoint_stats(self) -> Dict:
        """获取检查点统计信息"""
        if not self.checkpoint_manager:
            return {"error": "检查点功能未启用"}
        return self.checkpoint_manager.get_stats()

    def list_checkpoints(self, limit: int = None) -> List[Dict]:
        """列出检查点历史"""
        if not self.checkpoint_manager:
            raise RuntimeError("检查点功能未启用")
        return self.checkpoint_manager.list_history(limit)

    def clear_old_checkpoints(self, keep_last: int = 10):
        """清理旧检查点"""
        if not self.checkpoint_manager:
            raise RuntimeError("检查点功能未启用")
        self.checkpoint_manager.clear_old_checkpoints(keep_last)


class CompiledWorkflow:
    """编译后的工作流"""

    def __init__(self, graph: WorkflowGraph):
        self.graph = graph

    def invoke(self, initial_data: Dict = None, save_checkpoints: bool = True) -> Dict[str, Any]:
        """
        执行工作流

        参数:
            initial_data: 初始数据
            save_checkpoints: 是否自动保存检查点（需在WorkflowGraph中启用）

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
                'execution_log': [],
                'checkpoints': []  # 记录检查点ID
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

            # ========== 新增：保存检查点 ==========
            if save_checkpoints and self.graph.checkpoint_manager:
                checkpoint_id = self.graph.checkpoint_manager.save(
                    state=state,
                    current_node=current_node,
                    metadata={
                        'node_name': node.name,
                        'execution_count': node.execution_count
                    }
                )
                state['metadata']['checkpoints'].append(checkpoint_id)
                print(f"  [检查点] 已保存: {checkpoint_id[:8]}...")

            # 检查是否有错误
            if state['errors']:
                print(f"[错误] {state['errors'][-1]}")
                break

            # 查找下一个节点
            current_node = self._get_next_node(current_node, state)

        # 完成
        state['metadata']['end_time'] = datetime.now().isoformat()
        state['metadata']['success'] = len(state['errors']) == 0

        # 最终检查点
        if save_checkpoints and self.graph.checkpoint_manager:
            final_checkpoint_id = self.graph.checkpoint_manager.save(
                state=state,
                current_node="END",
                metadata={'completed': True}
            )
            state['metadata']['checkpoints'].append(final_checkpoint_id)

        return {
            'state': state,
            'nodes_executed': len(state['metadata']['nodes_executed']),
            'success': state['metadata']['success'],
            'errors': state['errors'],
            'warnings': state['warnings'],
            'checkpoints_created': len(state['metadata']['checkpoints'])
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
