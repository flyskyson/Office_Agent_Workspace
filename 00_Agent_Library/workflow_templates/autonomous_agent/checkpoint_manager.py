"""
自主代理工作流 - 检查点管理器

基于 WorkflowEngine 的 CheckpointManager 改进，适配自主代理工作流
"""

import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List, Any
from copy import deepcopy
from dataclasses import dataclass, asdict


@dataclass
class CheckpointMetadata:
    """检查点元数据"""
    node_id: str
    node_name: str
    status: str  # "in_progress", "completed", "failed"
    timestamp: str
    tools_created: List[str] = None
    tools_used: List[str] = None
    agent_id: str = ""
    duration_seconds: float = 0
    error_message: str = ""

    def to_dict(self) -> Dict:
        result = asdict(self)
        result['tools_created'] = self.tools_created or []
        result['tools_used'] = self.tools_used or []
        return result


class WorkflowCheckpointManager:
    """
    工作流检查点管理器

    功能：
    1. 在每个节点执行前后保存状态快照
    2. 支持从任意检查点恢复执行
    3. 维护完整的执行历史和时间线
    4. 持久化到文件系统
    5. 支持失败回滚

    用法：
        manager = WorkflowCheckpointManager("project_name", workspace_path)
        checkpoint_id = manager.save_before_node(state, node_config)
        restored_state = manager.restore(checkpoint_id)
    """

    def __init__(self, project_name: str, workspace_path: Path):
        """
        初始化检查点管理器

        Args:
            project_name: 项目名称
            workspace_path: 项目工作空间路径
        """
        self.project_name = project_name
        self.workspace_path = Path(workspace_path)

        # 检查点存储目录
        self.checkpoints_dir = self.workspace_path / "checkpoints"
        self.checkpoints_dir.mkdir(parents=True, exist_ok=True)

        # 索引文件
        self.index_file = self.checkpoints_dir / "index.jsonl"

        # 检查点索引（内存缓存）
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

    def _save_to_index(self, checkpoint: Dict):
        """追加保存到索引"""
        with open(self.index_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(checkpoint, ensure_ascii=False, default=str) + '\n')

    def save_before_node(
        self,
        state: Dict,
        node_id: str,
        node_name: str,
        agent_id: str = ""
    ) -> str:
        """
        在节点执行前保存检查点

        Args:
            state: 项目状态
            node_id: 节点ID
            node_name: 节点名称
            agent_id: 执行的子代理ID

        Returns:
            检查点ID
        """
        checkpoint_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()

        # 深拷贝状态
        state_copy = deepcopy(state)

        metadata = CheckpointMetadata(
            node_id=node_id,
            node_name=node_name,
            status="in_progress",
            timestamp=timestamp,
            agent_id=agent_id
        )

        checkpoint = {
            "id": checkpoint_id,
            "project_name": self.project_name,
            "timestamp": timestamp,
            "type": "before_node",
            "state": state_copy,
            "metadata": metadata.to_dict()
        }

        # 保存到文件
        self._save_checkpoint(checkpoint)

        return checkpoint_id

    def save_after_node(
        self,
        state: Dict,
        node_id: str,
        node_name: str,
        status: str,
        tools_created: List[str] = None,
        tools_used: List[str] = None,
        agent_id: str = "",
        duration_seconds: float = 0,
        error_message: str = ""
    ) -> str:
        """
        在节点执行后保存检查点

        Args:
            state: 项目状态
            node_id: 节点ID
            node_name: 节点名称
            status: 节点状态
            tools_created: 创建的工具列表
            tools_used: 使用的工具列表
            agent_id: 执行的子代理ID
            duration_seconds: 执行时长
            error_message: 错误信息（如果失败）

        Returns:
            检查点ID
        """
        checkpoint_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()

        # 深拷贝状态
        state_copy = deepcopy(state)

        metadata = CheckpointMetadata(
            node_id=node_id,
            node_name=node_name,
            status=status,
            timestamp=timestamp,
            tools_created=tools_created or [],
            tools_used=tools_used or [],
            agent_id=agent_id,
            duration_seconds=duration_seconds,
            error_message=error_message
        )

        checkpoint = {
            "id": checkpoint_id,
            "project_name": self.project_name,
            "timestamp": timestamp,
            "type": "after_node",
            "state": state_copy,
            "metadata": metadata.to_dict()
        }

        # 保存到文件
        self._save_checkpoint(checkpoint)

        return checkpoint_id

    def save_milestone(
        self,
        state: Dict,
        milestone_point: str,
        milestone_description: str
    ) -> str:
        """
        保存暂停点检查点

        Args:
            state: 项目状态
            milestone_point: 暂停点标识（如 "start", "30%", "70%", "pre_final"）
            milestone_description: 暂停点描述

        Returns:
            检查点ID
        """
        checkpoint_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()

        # 深拷贝状态
        state_copy = deepcopy(state)

        metadata = {
            "type": "milestone",
            "point": milestone_point,
            "description": milestone_description,
            "timestamp": timestamp
        }

        checkpoint = {
            "id": checkpoint_id,
            "project_name": self.project_name,
            "timestamp": timestamp,
            "type": "milestone",
            "state": state_copy,
            "metadata": metadata
        }

        # 保存到文件
        self._save_checkpoint(checkpoint)

        return checkpoint_id

    def _save_checkpoint(self, checkpoint: Dict):
        """保存检查点到文件"""
        checkpoint_id = checkpoint['id']

        # 保存完整检查点
        checkpoint_file = self.checkpoints_dir / f"{checkpoint_id}.json"
        with open(checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(checkpoint, f, ensure_ascii=False, indent=2, default=str)

        # 更新索引
        self.checkpoints[checkpoint_id] = checkpoint
        self._save_to_index(checkpoint)

    def restore(self, checkpoint_id: str) -> Optional[Dict]:
        """
        从检查点恢复状态

        Args:
            checkpoint_id: 检查点ID

        Returns:
            检查点数据（包含 state 和 metadata）
        """
        return self.checkpoints.get(checkpoint_id)

    def get_latest_checkpoint(self, node_id: str = None) -> Optional[Dict]:
        """
        获取最新的检查点

        Args:
            node_id: 如果指定，返回该节点最新的检查点

        Returns:
            检查点数据
        """
        if not self.checkpoints:
            return None

        # 过滤指定节点的检查点
        if node_id:
            filtered = [
                cp for cp in self.checkpoints.values()
                if cp.get('metadata', {}).get('node_id') == node_id
            ]
            if not filtered:
                return None
            return max(filtered, key=lambda x: x['timestamp'])

        # 返回所有检查点中最新的
        return max(self.checkpoints.values(), key=lambda x: x['timestamp'])

    def list_checkpoints(
        self,
        node_id: str = None,
        checkpoint_type: str = None
    ) -> List[Dict]:
        """
        列出检查点

        Args:
            node_id: 过滤特定节点
            checkpoint_type: 过滤特定类型（"before_node", "after_node", "milestone"）

        Returns:
            检查点列表（按时间排序）
        """
        checkpoints = list(self.checkpoints.values())

        # 过滤
        if node_id:
            checkpoints = [
                cp for cp in checkpoints
                if cp.get('metadata', {}).get('node_id') == node_id
            ]

        if checkpoint_type:
            checkpoints = [
                cp for cp in checkpoints
                if cp.get('type') == checkpoint_type
            ]

        # 按时间排序
        checkpoints.sort(key=lambda x: x['timestamp'])

        return checkpoints

    def get_execution_timeline(self) -> List[Dict]:
        """
        获取执行时间线

        Returns:
            按时间排序的执行事件列表
        """
        timeline = []

        for cp in self.checkpoints.values():
            event = {
                "timestamp": cp['timestamp'],
                "type": cp['type'],
                "metadata": cp.get('metadata', {})
            }
            timeline.append(event)

        timeline.sort(key=lambda x: x['timestamp'])
        return timeline

    def get_node_history(self, node_id: str) -> Dict:
        """
        获取节点的完整执行历史

        Args:
            node_id: 节点ID

        Returns:
            节点历史信息
        """
        checkpoints = self.list_checkpoints(node_id=node_id)

        if not checkpoints:
            return {
                "node_id": node_id,
                "executions": 0,
                "first_execution": None,
                "last_execution": None,
                "total_duration": 0,
                "status": "not_started"
            }

        # 统计
        after_checkpoints = [cp for cp in checkpoints if cp['type'] == 'after_node']
        completed = [cp for cp in after_checkpoints if cp['metadata']['status'] == 'completed']
        failed = [cp for cp in after_checkpoints if cp['metadata']['status'] == 'failed']

        return {
            "node_id": node_id,
            "node_name": checkpoints[0]['metadata'].get('node_name', node_id),
            "executions": len(after_checkpoints),
            "successful": len(completed),
            "failed": len(failed),
            "first_execution": checkpoints[0]['timestamp'],
            "last_execution": checkpoints[-1]['timestamp'],
            "total_duration": sum(cp['metadata'].get('duration_seconds', 0) for cp in after_checkpoints),
            "tools_created": list(set(
                tool for cp in after_checkpoints
                for tool in cp['metadata'].get('tools_created', [])
            )),
            "status": "completed" if completed else "failed" if failed else "in_progress"
        }

    def cleanup_old_checkpoints(self, keep_last_n: int = 10):
        """
        清理旧的检查点，只保留最近的 N 个

        Args:
            keep_last_n: 保留最近的检查点数量
        """
        if len(self.checkpoints) <= keep_last_n:
            return

        # 按时间排序，删除最旧的
        sorted_checkpoints = sorted(
            self.checkpoints.items(),
            key=lambda x: x[1]['timestamp']
        )

        to_delete = len(sorted_checkpoints) - keep_last_n

        for checkpoint_id, _ in sorted_checkpoints[:to_delete]:
            # 删除文件
            checkpoint_file = self.checkpoints_dir / f"{checkpoint_id}.json"
            if checkpoint_file.exists():
                checkpoint_file.unlink()

            # 从索引删除
            del self.checkpoints[checkpoint_id]

        # 重建索引文件
        with open(self.index_file, 'w', encoding='utf-8') as f:
            for cp in self.checkpoints.values():
                f.write(json.dumps(cp, ensure_ascii=False, default=str) + '\n')
