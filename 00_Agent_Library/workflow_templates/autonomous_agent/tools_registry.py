"""
工具注册表管理

实现工具的注册、查询、生命周期管理
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from enum import Enum


class ToolStatus(Enum):
    """工具状态"""
    EXPERIMENTAL = "experimental"  # 实验阶段：仅创建者使用
    TESTING = "testing"  # 试用阶段：需要2个以上其他代理使用
    STABLE = "stable"  # 稳定阶段：推荐使用
    DEPRECATED = "deprecated"  # 废弃阶段：标记但不删除


@dataclass
class ToolInfo:
    """工具信息"""
    name: str
    version: str
    creator: str
    created_at: str
    status: str
    purpose: str
    usage_count: int = 0
    success_rate: float = 1.0
    file_path: str = ""
    dependencies: List[str] = field(default_factory=list)
    last_used: Optional[str] = None
    feedback: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ToolInfo":
        """从字典创建"""
        return cls(**data)


class ToolsRegistry:
    """工具注册表"""

    def __init__(self, registry_path: str):
        """
        初始化工具注册表

        Args:
            registry_path: 注册表文件路径
        """
        self.registry_path = Path(registry_path)
        self.tools: Dict[str, ToolInfo] = {}
        self._load()

    def _load(self):
        """加载注册表"""
        if self.registry_path.exists():
            with open(self.registry_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for tool_data in data.get("tools", []):
                    tool_info = ToolInfo.from_dict(tool_data)
                    self.tools[tool_info.name] = tool_info

    def _save(self):
        """保存注册表"""
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "tools": [tool.to_dict() for tool in self.tools.values()],
            "last_updated": datetime.now().isoformat()
        }
        with open(self.registry_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def register(
        self,
        name: str,
        creator: str,
        purpose: str,
        file_path: str,
        dependencies: List[str] = None
    ) -> ToolInfo:
        """
        注册新工具

        Args:
            name: 工具名称
            creator: 创建者
            purpose: 工具用途
            file_path: 工具文件路径
            dependencies: 依赖列表

        Returns:
            工具信息
        """
        if name in self.tools:
            raise ValueError(f"工具已存在: {name}")

        tool_info = ToolInfo(
            name=name,
            version="1.0.0",
            creator=creator,
            created_at=datetime.now().isoformat(),
            status=ToolStatus.EXPERIMENTAL.value,
            purpose=purpose,
            file_path=file_path,
            dependencies=dependencies or []
        )

        self.tools[name] = tool_info
        self._save()
        return tool_info

    def query(self, purpose_keywords: List[str] = None) -> List[ToolInfo]:
        """
        查询工具

        Args:
            purpose_keywords: 用途关键词列表

        Returns:
            匹配的工具列表
        """
        results = []
        for tool in self.tools.values():
            # 跳过废弃工具
            if tool.status == ToolStatus.DEPRECATED.value:
                continue

            # 如果没有关键词，返回所有稳定工具
            if not purpose_keywords:
                if tool.status in [ToolStatus.STABLE.value, ToolStatus.TESTING.value]:
                    results.append(tool)
                continue

            # 匹配关键词
            purpose_lower = tool.purpose.lower()
            if any(keyword.lower() in purpose_lower for keyword in purpose_keywords):
                results.append(tool)

        # 按成功率和使用次数排序
        results.sort(key=lambda t: (t.success_rate, t.usage_count), reverse=True)
        return results

    def get_tool(self, name: str) -> Optional[ToolInfo]:
        """获取工具信息"""
        return self.tools.get(name)

    def record_usage(self, name: str, success: bool, feedback: str = None):
        """
        记录工具使用

        Args:
            name: 工具名称
            success: 是否成功
            feedback: 反馈信息
        """
        tool = self.tools.get(name)
        if not tool:
            return

        tool.usage_count += 1
        tool.last_used = datetime.now().isoformat()

        # 更新成功率
        if success:
            # 简单的移动平均
            tool.success_rate = (tool.success_rate * 0.9 + 1.0 * 0.1)
        else:
            tool.success_rate = (tool.success_rate * 0.9 + 0.0 * 0.1)

        # 添加反馈
        if feedback:
            tool.feedback.append(feedback)

        # 更新工具状态
        self._update_tool_status(tool)

        self._save()

    def _update_tool_status(self, tool: ToolInfo):
        """
        根据使用情况更新工具状态

        状态转换规则：
        - experimental -> testing: 至少2个其他代理使用过
        - testing -> stable: 成功率>0.8 且使用次数>5
        - stable -> deprecated: 30天未使用或成功率<0.5
        """
        # 实验阶段 -> 试用阶段
        if tool.status == ToolStatus.EXPERIMENTAL.value:
            # 检查是否有至少2个其他代理使用过（通过反馈列表）
            other_users = set()
            for fb in tool.feedback:
                # 假设反馈格式为 "agent_X: feedback"
                if ":" in fb:
                    user = fb.split(":")[0].strip()
                    if user != tool.creator:
                        other_users.add(user)

            if len(other_users) >= 2:
                tool.status = ToolStatus.TESTING.value

        # 试用阶段 -> 稳定阶段
        elif tool.status == ToolStatus.TESTING.value:
            if tool.usage_count >= 5 and tool.success_rate >= 0.8:
                tool.status = ToolStatus.STABLE.value

        # 稳定阶段 -> 废弃阶段
        elif tool.status == ToolStatus.STABLE.value:
            # 检查是否30天未使用
            if tool.last_used:
                last_used = datetime.fromisoformat(tool.last_used)
                days_unused = (datetime.now() - last_used).days
                if days_unused > 30 or tool.success_rate < 0.5:
                    tool.status = ToolStatus.DEPRECATED.value

    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        total = len(self.tools)
        by_status = {}
        for status in ToolStatus:
            count = sum(1 for t in self.tools.values() if t.status == status.value)
            by_status[status.value] = count

        total_usage = sum(t.usage_count for t in self.tools.values())
        avg_success_rate = sum(t.success_rate for t in self.tools.values()) / total if total > 0 else 0

        return {
            "total_tools": total,
            "by_status": by_status,
            "total_usage": total_usage,
            "average_success_rate": avg_success_rate
        }

    def cleanup_deprecated(self, older_than_days: int = 90):
        """
        清理长期废弃的工具

        Args:
            older_than_days: 废弃多少天后清理
        """
        to_remove = []
        for name, tool in self.tools.items():
            if tool.status == ToolStatus.DEPRECATED.value and tool.last_used:
                last_used = datetime.fromisoformat(tool.last_used)
                days_since_used = (datetime.now() - last_used).days
                if days_since_used > older_than_days:
                    to_remove.append(name)

        for name in to_remove:
            del self.tools[name]

        if to_remove:
            self._save()

        return to_remove
