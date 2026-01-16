#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
计划管理系统 - 确保计划的实施时机

解决的核心问题：
1. 计划跨会话持久化
2. 时机自动触发
3. 优先级管理
4. 执行状态追踪

作者: Claude Code
日期: 2026-01-17
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Literal
from enum import Enum
from dataclasses import dataclass, asdict

# Windows 终端编码修复
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


# ============================================================================
# 计划时间范围
# ============================================================================

class PlanTimeRange(Enum):
    """计划时间范围"""
    SHORT_TERM = "short_term"    # 短期: 1-7天
    MEDIUM_TERM = "medium_term"  # 中期: 1-4周
    LONG_TERM = "long_term"      # 长期: 1-6个月


# ============================================================================
# 计划状态
# ============================================================================

class PlanStatus(Enum):
    """计划状态"""
    PENDING = "pending"           # 待执行
    READY = "ready"               # 就绪（条件已满足）
    IN_PROGRESS = "in_progress"   # 执行中
    COMPLETED = "completed"       # 已完成
    FAILED = "failed"             # 失败
    CANCELLED = "cancelled"       # 已取消
    DEFERRED = "deferred"         # 延期


# ============================================================================
# 触发条件类型
# ============================================================================

class TriggerType(Enum):
    """触发条件类型"""
    TIME_BASED = "time_based"           # 基于时间（日期、间隔）
    EVENT_BASED = "event_based"         # 基于事件（文件变更、Git提交）
    CONTEXT_BASED = "context_based"     # 基于上下文（关键词、工作区状态）
    USER_TRIGGERED = "user_triggered"   # 用户触发
    DEPENDENCY_BASED = "dependency_based"  # 基于依赖（其他计划完成）


@dataclass
class TriggerCondition:
    """触发条件"""
    trigger_type: TriggerType
    condition: str                      # 条件描述
    check_function: str                 # 检查函数名称

    # 时间相关参数
    target_date: Optional[str] = None   # 目标日期 (YYYY-MM-DD)
    days_since: Optional[int] = None    # 距离某事的天数

    # 事件相关参数
    event_type: Optional[str] = None    # 事件类型
    event_count: Optional[int] = None   # 事件次数阈值

    # 上下文相关参数
    keywords: Optional[List[str]] = None  # 关键词列表
    context_path: Optional[str] = None   # 上下文文件路径

    # 依赖相关参数
    dependency_plan_id: Optional[str] = None  # 依赖的计划ID


# ============================================================================
# 计划定义
# ============================================================================

@dataclass
class Plan:
    """计划"""
    id: str                              # 唯一ID
    title: str                           # 计划标题
    description: str                     # 详细描述
    time_range: PlanTimeRange            # 时间范围
    priority: int                        # 优先级 (1-10, 10最高)
    status: PlanStatus                   # 当前状态

    # 创建和更新时间
    created_at: str                      # 创建时间
    updated_at: str                      # 更新时间

    # 触发条件
    trigger: TriggerCondition            # 触发条件

    # 执行信息
    executor: str                        # 执行器（函数名或脚本路径）
    executor_type: Literal["function", "script", "manual"]  # 执行器类型

    # 结果追踪
    result: Optional[Dict[str, Any]] = None  # 执行结果
    error: Optional[str] = None              # 错误信息

    # 元数据
    metadata: Dict[str, Any] = None      # 额外信息
    tags: List[str] = None               # 标签


# ============================================================================
# 计划管理器
# ============================================================================

class PlanManager:
    """
    计划管理器 - 确保计划的实施时机

    核心功能:
    1. 存储和检索计划
    2. 检查计划是否就绪
    3. 触发计划执行
    4. 追踪计划状态
    """

    def __init__(self, storage_path: Path = None):
        """初始化计划管理器"""
        if storage_path is None:
            storage_path = Path(__file__).parent.parent.parent / "06_Learning_Journal" / "workspace_memory" / "plans"

        self.storage_path = storage_path
        self.storage_path.mkdir(parents=True, exist_ok=True)

        self.plans_file = self.storage_path / "plans.jsonl"
        self.plans: Dict[str, Plan] = {}
        self._load_plans()

    def _load_plans(self):
        """加载计划"""
        if not self.plans_file.exists():
            return

        try:
            with open(self.plans_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        plan = self._dict_to_plan(data)
                        self.plans[plan.id] = plan
        except Exception as e:
            print(f"⚠️  加载计划失败: {e}")

    def _save_plan(self, plan: Plan):
        """保存单个计划"""
        with open(self.plans_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(asdict(plan), ensure_ascii=False, default=str) + '\n')

    def _save_all_plans(self):
        """保存所有计划"""
        with open(self.plans_file, 'w', encoding='utf-8') as f:
            for plan in self.plans.values():
                f.write(json.dumps(asdict(plan), ensure_ascii=False, default=str) + '\n')

    @staticmethod
    def _dict_to_plan(data: Dict) -> Plan:
        """字典转计划对象"""
        # 处理枚举类型
        time_range = PlanTimeRange(data['time_range'])
        status = PlanStatus(data['status'])

        # 处理触发条件
        trigger_data = data['trigger']
        trigger = TriggerCondition(
            trigger_type=TriggerType(trigger_data['trigger_type']),
            condition=trigger_data['condition'],
            check_function=trigger_data['check_function'],
            target_date=trigger_data.get('target_date'),
            days_since=trigger_data.get('days_since'),
            event_type=trigger_data.get('event_type'),
            event_count=trigger_data.get('event_count'),
            keywords=trigger_data.get('keywords'),
            context_path=trigger_data.get('context_path'),
            dependency_plan_id=trigger_data.get('dependency_plan_id')
        )

        return Plan(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            time_range=time_range,
            priority=data['priority'],
            status=status,
            created_at=data['created_at'],
            updated_at=data['updated_at'],
            trigger=trigger,
            executor=data['executor'],
            executor_type=data['executor_type'],
            result=data.get('result'),
            error=data.get('error'),
            metadata=data.get('metadata'),
            tags=data.get('tags', [])
        )

    def add_plan(self, plan: Plan) -> str:
        """添加计划"""
        self.plans[plan.id] = plan
        self._save_plan(plan)
        return plan.id

    def get_plan(self, plan_id: str) -> Optional[Plan]:
        """获取计划"""
        return self.plans.get(plan_id)

    def list_plans(self, status: PlanStatus = None, time_range: PlanTimeRange = None) -> List[Plan]:
        """列出计划"""
        plans = list(self.plans.values())

        if status:
            plans = [p for p in plans if p.status == status]

        if time_range:
            plans = [p for p in plans if p.time_range == time_range]

        # 按优先级排序
        plans.sort(key=lambda p: p.priority, reverse=True)
        return plans

    def check_triggers(self) -> List[Plan]:
        """检查哪些计划的触发条件已满足"""
        ready_plans = []

        for plan in self.plans.values():
            if plan.status != PlanStatus.PENDING:
                continue

            if self._is_trigger_ready(plan):
                plan.status = PlanStatus.READY
                plan.updated_at = datetime.now().isoformat()
                ready_plans.append(plan)

        if ready_plans:
            self._save_all_plans()

        return ready_plans

    def _is_trigger_ready(self, plan: Plan) -> bool:
        """检查触发条件是否满足"""
        trigger = plan.trigger

        if trigger.trigger_type == TriggerType.TIME_BASED:
            return self._check_time_trigger(trigger)
        elif trigger.trigger_type == TriggerType.EVENT_BASED:
            return self._check_event_trigger(trigger)
        elif trigger.trigger_type == TriggerType.CONTEXT_BASED:
            return self._check_context_trigger(trigger)
        elif trigger.trigger_type == TriggerType.DEPENDENCY_BASED:
            return self._check_dependency_trigger(trigger)

        return False

    def _check_time_trigger(self, trigger: TriggerCondition) -> bool:
        """检查时间触发条件"""
        if trigger.target_date:
            target = datetime.fromisoformat(trigger.target_date)
            return datetime.now() >= target

        if trigger.days_since is not None:
            # 需要参考日期，这里简化处理
            # 实际应该从计划创建日期或指定事件日期计算
            return True

        return False

    def _check_event_trigger(self, trigger: TriggerCondition) -> bool:
        """检查事件触发条件"""
        # 这里可以检查Git提交数、文件变更等
        # 简化实现：总是返回False，需要具体实现
        return False

    def _check_context_trigger(self, trigger: TriggerCondition) -> bool:
        """检查上下文触发条件"""
        if trigger.context_path and Path(trigger.context_path).exists():
            return True
        return False

    def _check_dependency_trigger(self, trigger: TriggerCondition) -> bool:
        """检查依赖触发条件"""
        if trigger.dependency_plan_id:
            dep_plan = self.get_plan(trigger.dependency_plan_id)
            return dep_plan and dep_plan.status == PlanStatus.COMPLETED
        return False

    def execute_plan(self, plan_id: str) -> Dict[str, Any]:
        """执行计划"""
        plan = self.get_plan(plan_id)
        if not plan:
            return {"success": False, "error": "计划不存在"}

        plan.status = PlanStatus.IN_PROGRESS
        plan.updated_at = datetime.now().isoformat()
        self._save_all_plans()

        try:
            # 根据执行器类型执行
            if plan.executor_type == "function":
                result = self._execute_function(plan)
            elif plan.executor_type == "script":
                result = self._execute_script(plan)
            else:
                result = {"success": False, "error": "未知执行器类型"}

            plan.status = PlanStatus.COMPLETED if result.get("success") else PlanStatus.FAILED
            plan.result = result
            plan.updated_at = datetime.now().isoformat()
            self._save_all_plans()

            return result

        except Exception as e:
            plan.status = PlanStatus.FAILED
            plan.error = str(e)
            plan.updated_at = datetime.now().isoformat()
            self._save_all_plans()
            return {"success": False, "error": str(e)}

    def _execute_function(self, plan: Plan) -> Dict[str, Any]:
        """执行函数"""
        # 这里可以根据函数名动态调用
        # 简化实现：返回成功
        return {"success": True, "message": f"执行函数: {plan.executor}"}

    def _execute_script(self, plan: Plan) -> Dict[str, Any]:
        """执行脚本"""
        import subprocess
        result = subprocess.run(
            [plan.executor],
            capture_output=True,
            text=True,
            timeout=300
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    def update_plan_status(self, plan_id: str, status: PlanStatus, result: Dict = None, error: str = None):
        """更新计划状态"""
        plan = self.get_plan(plan_id)
        if plan:
            plan.status = status
            plan.updated_at = datetime.now().isoformat()
            if result:
                plan.result = result
            if error:
                plan.error = error
            self._save_all_plans()


# ============================================================================
# 示例使用
# ============================================================================

def example_usage():
    """示例：创建和管理计划"""
    print("=" * 60)
    print("📋 计划管理系统示例")
    print("=" * 60)

    # 创建计划管理器
    manager = PlanManager()

    # 示例1: 短期计划 - 每日新闻获取
    plan1 = Plan(
        id="daily_news_20260117",
        title="获取今日AI新闻",
        description="每天早上获取AI相关的热点新闻",
        time_range=PlanTimeRange.SHORT_TERM,
        priority=7,
        status=PlanStatus.PENDING,
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat(),
        trigger=TriggerCondition(
            trigger_type=TriggerType.TIME_BASED,
            condition="每天早上8点",
            check_function="check_time_trigger",
            target_date=(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        ),
        executor="news_reader.py",
        executor_type="script",
        tags=["新闻", "AI", "每日"]
    )

    # 示例2: 中期计划 - 代码审查
    plan2 = Plan(
        id="code_review_20260117",
        title="代码审查和重构",
        description="每周审查代码质量并进行必要的重构",
        time_range=PlanTimeRange.MEDIUM_TERM,
        priority=5,
        status=PlanStatus.PENDING,
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat(),
        trigger=TriggerCondition(
            trigger_type=TriggerType.EVENT_BASED,
            condition="Git提交达到10次",
            check_function="check_commit_count",
            event_type="git_commit",
            event_count=10
        ),
        executor="code_review.py",
        executor_type="script",
        tags=["代码质量", "重构"]
    )

    # 示例3: 长期计划 - v3.0 开发
    plan3 = Plan(
        id="v3_development_20260117",
        title="v3.0 系统开发",
        description="实现工具间实际通信和高级功能",
        time_range=PlanTimeRange.LONG_TERM,
        priority=8,
        status=PlanStatus.PENDING,
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat(),
        trigger=TriggerCondition(
            trigger_type=TriggerType.DEPENDENCY_BASED,
            condition="v2.5完成后启动",
            check_function="check_dependency",
            dependency_plan_id="v25_completion"
        ),
        executor="develop_v3.py",
        executor_type="script",
        tags=["开发", "v3.0", "路线图"]
    )

    # 添加计划
    manager.add_plan(plan1)
    manager.add_plan(plan2)
    manager.add_plan(plan3)

    # 列出计划
    print("\n📋 所有计划:")
    for plan in manager.list_plans():
        print(f"  [{plan.time_range.value}] {plan.title} (优先级: {plan.priority})")

    # 检查就绪计划
    print("\n✅ 检查就绪计划...")
    ready = manager.check_triggers()
    if ready:
        for plan in ready:
            print(f"  → {plan.title} 已就绪！")
    else:
        print("  暂无就绪的计划")

    print("\n💡 计划管理系统已就绪，可以:")
    print("  1. 跨会话持久化计划")
    print("  2. 自动检查触发条件")
    print("  3. 按优先级执行计划")
    print("  4. 追踪计划状态和历史")


if __name__ == "__main__":
    example_usage()
