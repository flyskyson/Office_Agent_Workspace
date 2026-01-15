# -*- coding: utf-8 -*-
"""
Idea Workflow Engine - 想法落地工作流引擎
===========================================

从模糊想法到可用产品的系统化流程

Author: Office Agent Workspace
Version: 1.0.0
Created: 2025-01-14

核心特性:
- 结构化的5阶段流程
- 智能对话引导
- 自动代码探索
- 多方案生成
- 快速原型验证
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod


# ============================================================================
# 数据模型
# ============================================================================

@dataclass
class IdeaInput:
    """想法输入"""
    original_text: str           # 原始想法描述
    idea_type: str = ""          # 想法类型: feature/bug/refactor/new_project
    context: str = ""            # 上下文信息
    priority: str = "medium"     # 优先级: high/medium/low
    tags: List[str] = None       # 标签

    def __post_init__(self):
        if self.tags is None:
            self.tags = []


@dataclass
class ClarifiedIdea:
    """澄清后的想法"""
    problem_statement: str       # 问题陈述
    target_users: List[str]      # 目标用户
    pain_points: List[str]       # 痛点列表
    success_criteria: List[str]  # 成功标准
    constraints: List[str]       # 约束条件
    assumptions: List[str]       # 假设


@dataclass
class ExplorationResult:
    """探索结果"""
    technical_feasibility: str   # 技术可行性: high/medium/low
    estimated_effort: str        # 预估工作量: hours/days/weeks
    existing_solutions: List[str] # 现有解决方案
    dependencies: List[str]      # 依赖项
    risks: List[str]             # 风险列表
    opportunities: List[str]     # 机会列表


@dataclass
class SolutionDesign:
    """方案设计"""
    approach: str                # 方法名称
    description: str             # 描述
    architecture: str            # 架构说明
    files_to_modify: List[str]   # 需要修改的文件
    files_to_create: List[str]   # 需要创建的文件
    estimated_time: str          # 预估时间
    pros: List[str]              # 优点
    cons: List[str]              # 缺点
    implementation_steps: List[str] # 实施步骤


@dataclass
class PrototypeResult:
    """原型结果"""
    mvp_implemented: bool        # MVP是否实现
    demo_files: List[str]        # 演示文件
    test_results: Dict[str, Any] # 测试结果
    user_feedback: str           # 用户反馈
    next_steps: List[str]        # 下一步行动


@dataclass
class WorkflowSession:
    """工作流会话"""
    session_id: str              # 会话ID
    created_at: str              # 创建时间
    phase: str                   # 当前阶段
    idea_input: IdeaInput        # 想法输入
    clarified_idea: Optional[ClarifiedIdea] = None
    exploration_result: Optional[ExplorationResult] = None
    selected_solution: Optional[SolutionDesign] = None
    prototype_result: Optional[PrototypeResult] = None
    metadata: Dict[str, Any] = None  # 元数据

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


# ============================================================================
# 工作流阶段基类
# ============================================================================

class WorkflowPhase(ABC):
    """工作流阶段基类"""

    phase_name = "base"
    phase_description = "基础阶段"

    @abstractmethod
    def execute(self, session: WorkflowSession) -> Tuple[bool, str, Any]:
        """
        执行阶段

        Args:
            session: 工作流会话

        Returns:
            (success, message, result)
            - success: 是否成功
            - message: 状态消息
            - result: 阶段结果对象
        """
        pass

    @abstractmethod
    def get_guiding_questions(self) -> List[str]:
        """获取引导问题列表"""
        pass


# ============================================================================
# Phase 1: 理解与澄清
# ============================================================================

class Phase1_Clarification(WorkflowPhase):
    """阶段1: 理解与澄清"""

    phase_name = "clarification"
    phase_description = "理解与澄清 - 将模糊想法转化为清晰的需求定义"

    def get_guiding_questions(self) -> List[str]:
        return [
            "您能描述一个具体的使用场景吗?",
            "现在的问题是什麽?最困扰您的是什麽?",
            "这个问题影响了谁?影响程度如何?",
            "理想情况下,您希望如何解决这个问题?",
            "有没有类似的系统或功能可以参考?",
            "成功的标准是什么?如何知道问题已经解决?",
        ]

    def execute(self, session: WorkflowSession) -> Tuple[bool, str, Any]:
        """
        执行澄清阶段

        这个阶段主要通过对话引导,由Claude和用户交互完成
        这里提供一个结构化的输出格式
        """
        print(f"\n{'='*60}")
        print(f"🎯 Phase 1: 理解与澄清")
        print(f"{'='*60}\n")

        print("📝 引导问题:")
        for i, question in enumerate(self.get_guiding_questions(), 1):
            print(f"   {i}. {question}")

        print("\n💡 通过对话回答这些问题,生成清晰的需求定义...")

        # 返回需要通过对话填充的结构
        clarified = ClarifiedIdea(
            problem_statement="[通过对话生成]",
            target_users=[],
            pain_points=[],
            success_criteria=[],
            constraints=[],
            assumptions=[]
        )

        return True, "澄清阶段初始化,请通过对话完善需求", clarified


# ============================================================================
# Phase 2: 探索与分析
# ============================================================================

class Phase2_Exploration(WorkflowPhase):
    """阶段2: 探索与分析"""

    phase_name = "exploration"
    phase_description = "探索与分析 - 自动代码探索和可行性评估"

    def get_guiding_questions(self) -> List[str]:
        return [
            "这个功能与现有系统如何集成?",
            "需要修改哪些现有代码?",
            "有没有可以复用的现有组件?",
            "技术实现上有什么限制或约束?",
            "数据从哪里来?存储到哪里?",
        ]

    def execute(self, session: WorkflowSession) -> Tuple[bool, str, Any]:
        """
        执行探索阶段

        Claude会自动:
        1. 搜索相关代码
        2. 分析现有实现
        3. 评估技术可行性
        4. 识别依赖和风险
        """
        print(f"\n{'='*60}")
        print(f"🔍 Phase 2: 探索与分析")
        print(f"{'='*60}\n")

        print("🔬 自动探索任务:")
        tasks = [
            "扫描代码库查找相关模块",
            "分析现有架构和设计模式",
            "识别可复用的组件",
            "评估技术可行性",
            "识别潜在风险和依赖",
        ]

        for i, task in enumerate(tasks, 1):
            print(f"   {i}. {task}")

        print("\n⏳ 正在执行自动探索...")

        # 返回探索结果结构
        result = ExplorationResult(
            technical_feasibility="[待评估]",
            estimated_effort="[待评估]",
            existing_solutions=[],
            dependencies=[],
            risks=[],
            opportunities=[]
        )

        return True, "探索阶段准备就绪,等待执行代码分析", result


# ============================================================================
# Phase 3: 方案设计
# ============================================================================

class Phase3_Design(WorkflowPhase):
    """阶段3: 方案设计"""

    phase_name = "design"
    phase_description = "方案设计 - 生成多个可选方案并对比分析"

    def get_guiding_questions(self) -> List[str]:
        return [
            "简单快速 vs 完整智能,您倾向哪个?",
            "优先考虑开发速度还是运行性能?",
            "可以接受的技术复杂度?",
            "需要考虑向后兼容吗?",
            "是否需要预留扩展空间?",
        ]

    def execute(self, session: WorkflowSession) -> Tuple[bool, str, Any]:
        """
        执行设计阶段

        Claude会自动生成多个方案并对比:
        1. 方案A: 最小可行方案(MVP)
        2. 方案B: 推荐方案(平衡)
        3. 方案C: 完整方案(旗舰)
        """
        print(f"\n{'='*60}")
        print(f"📐 Phase 3: 方案设计")
        print(f"{'='*60}\n")

        print("🎨 设计策略:")
        strategies = [
            "方案A - 快速原型(MVP): 最小功能,快速验证",
            "方案B - 推荐方案: 平衡功能和开发成本",
            "方案C - 完整方案: 功能全面,可扩展性强",
        ]

        for strategy in strategies:
            print(f"   • {strategy}")

        print("\n⚙️  正在生成多个设计方案...")

        # 返回方案模板
        solution = SolutionDesign(
            approach="[方案名称]",
            description="[方案描述]",
            architecture="[架构说明]",
            files_to_modify=[],
            files_to_create=[],
            estimated_time="[预估时间]",
            pros=[],
            cons=[],
            implementation_steps=[]
        )

        return True, "设计阶段准备就绪,等待生成方案", solution


# ============================================================================
# Phase 4: 快速原型
# ============================================================================

class Phase4_Prototyping(WorkflowPhase):
    """阶段4: 快速原型"""

    phase_name = "prototyping"
    phase_description = "快速原型 - 实现最小可行版本并演示"

    def get_guiding_questions(self) -> List[str]:
        return [
            "先看一个简单版本可以吗?",
            "哪些功能是必须有的?",
            "哪些功能可以后续添加?",
            "需要准备什么样的测试数据?",
        ]

    def execute(self, session: WorkflowSession) -> Tuple[bool, str, Any]:
        """
        执行原型阶段

        Claude会自动:
        1. 实现MVP版本代码
        2. 准备测试数据
        3. 运行演示
        """
        print(f"\n{'='*60}")
        print(f"⚡ Phase 4: 快速原型")
        print(f"{'='*60}\n")

        print("🔨 原型开发任务:")
        tasks = [
            "实现核心功能(MVP)",
            "准备测试数据和样例",
            "创建可交互的Demo",
            "编写快速验证脚本",
        ]

        for i, task in enumerate(tasks, 1):
            print(f"   {i}. {task}")

        print("\n💻 正在实现MVP...")

        result = PrototypeResult(
            mvp_implemented=False,
            demo_files=[],
            test_results={},
            user_feedback="",
            next_steps=[]
        )

        return True, "原型阶段准备就绪,等待实现MVP", result


# ============================================================================
# Phase 5: 验证与迭代
# ============================================================================

class Phase5_Validation(WorkflowPhase):
    """阶段5: 验证与迭代"""

    phase_name = "validation"
    phase_description = "验证与迭代 - 收集反馈并持续优化"

    def get_guiding_questions(self) -> List[str]:
        return [
            "这个方向对吗?",
            "还有什么需要调整的?",
            "继续完善还是换个方向?",
            "是否满足您的期望?",
            "下一步做什么?",
        ]

    def execute(self, session: WorkflowSession) -> Tuple[bool, str, Any]:
        """
        执行验证阶段

        1. 用户测试MVP
        2. 收集反馈
        3. 快速调整
        4. 决定下一步
        """
        print(f"\n{'='*60}")
        print(f"✅ Phase 5: 验证与迭代")
        print(f"{'='*60}\n")

        print("🔄 迭代循环:")
        cycle = [
            "用户测试MVP",
            "收集反馈意见",
            "快速调整优化",
            "决定下一步行动",
        ]

        for i, step in enumerate(cycle, 1):
            print(f"   {i}. {step}")

        print("\n📊 等待您的反馈...")

        return True, "验证阶段准备就绪,等待测试反馈", None


# ============================================================================
# 工作流引擎
# ============================================================================

class IdeaWorkflowEngine:
    """
    想法落地工作流引擎

    使用方式:
        engine = IdeaWorkflowEngine()
        session = engine.create_session("我想添加一个智能推荐功能")
        engine.run_phase(session, "clarification")
    """

    def __init__(self, workspace_root: Optional[Path] = None):
        """
        初始化工作流引擎

        Args:
            workspace_root: 工作区根路径
        """
        if workspace_root is None:
            workspace_root = Path(__file__).parent.parent

        self.workspace_root = Path(workspace_root)
        self.sessions: Dict[str, WorkflowSession] = {}
        self.phases = {
            "clarification": Phase1_Clarification(),
            "exploration": Phase2_Exploration(),
            "design": Phase3_Design(),
            "prototyping": Phase4_Prototyping(),
            "validation": Phase5_Validation(),
        }

        # 确保会话存储目录存在
        self.sessions_dir = self.workspace_root / "06_Learning_Journal" / "idea_sessions"
        self.sessions_dir.mkdir(parents=True, exist_ok=True)

    def create_session(self, idea_text: str, **kwargs) -> WorkflowSession:
        """
        创建新的工作流会话

        Args:
            idea_text: 想法描述
            **kwargs: 其他参数

        Returns:
            WorkflowSession对象
        """
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        idea_input = IdeaInput(
            original_text=idea_text,
            **kwargs
        )

        session = WorkflowSession(
            session_id=session_id,
            created_at=datetime.now().isoformat(),
            phase="initialized",
            idea_input=idea_input
        )

        self.sessions[session_id] = session
        self._save_session(session)

        return session

    def run_phase(self, session: WorkflowSession,
                  phase_name: str) -> Tuple[bool, str, Any]:
        """
        运行指定阶段

        Args:
            session: 工作流会话
            phase_name: 阶段名称

        Returns:
            (success, message, result)
        """
        if phase_name not in self.phases:
            return False, f"未知阶段: {phase_name}", None

        phase = self.phases[phase_name]

        # 更新会话阶段
        session.phase = phase_name

        # 执行阶段
        success, message, result = phase.execute(session)

        # 保存会话
        self._save_session(session)

        return success, message, result

    def get_next_phase(self, current_phase: str) -> Optional[str]:
        """获取下一个阶段"""
        phase_order = [
            "clarification",
            "exploration",
            "design",
            "prototyping",
            "validation"
        ]

        try:
            index = phase_order.index(current_phase)
            if index < len(phase_order) - 1:
                return phase_order[index + 1]
        except ValueError:
            pass

        return None

    def get_guiding_questions(self, phase_name: str) -> List[str]:
        """获取指定阶段的引导问题"""
        if phase_name in self.phases:
            return self.phases[phase_name].get_guiding_questions()
        return []

    def print_session_summary(self, session: WorkflowSession):
        """打印会话摘要"""
        print(f"\n{'='*60}")
        print(f"📋 会话摘要")
        print(f"{'='*60}")
        print(f"会话ID: {session.session_id}")
        print(f"创建时间: {session.created_at}")
        print(f"当前阶段: {session.phase}")
        print(f"\n原始想法:")
        print(f"  {session.idea_input.original_text}")
        print(f"{'='*60}\n")

    def _save_session(self, session: WorkflowSession):
        """保存会话到文件"""
        session_file = self.sessions_dir / f"session_{session.session_id}.json"

        # 转换为可序列化的字典
        session_dict = {
            "session_id": session.session_id,
            "created_at": session.created_at,
            "phase": session.phase,
            "idea_input": asdict(session.idea_input),
            "metadata": session.metadata,
        }

        # 添加可选字段
        if session.clarified_idea:
            session_dict["clarified_idea"] = asdict(session.clarified_idea)
        if session.exploration_result:
            session_dict["exploration_result"] = asdict(session.exploration_result)
        if session.selected_solution:
            session_dict["selected_solution"] = asdict(session.selected_solution)
        if session.prototype_result:
            session_dict["prototype_result"] = asdict(session.prototype_result)

        # 写入文件
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session_dict, f, ensure_ascii=False, indent=2)

    def load_session(self, session_id: str) -> Optional[WorkflowSession]:
        """从文件加载会话"""
        session_file = self.sessions_dir / f"session_{session_id}.json"

        if not session_file.exists():
            return None

        with open(session_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 重建会话对象
        session = WorkflowSession(
            session_id=data["session_id"],
            created_at=data["created_at"],
            phase=data["phase"],
            idea_input=IdeaInput(**data["idea_input"]),
            metadata=data.get("metadata", {})
        )

        # 恢复可选字段
        if "clarified_idea" in data:
            session.clarified_idea = ClarifiedIdea(**data["clarified_idea"])
        if "exploration_result" in data:
            session.exploration_result = ExplorationResult(**data["exploration_result"])
        if "selected_solution" in data:
            session.selected_solution = SolutionDesign(**data["selected_solution"])
        if "prototype_result" in data:
            session.prototype_result = PrototypeResult(**data["prototype_result"])

        self.sessions[session_id] = session
        return session

    def list_sessions(self) -> List[str]:
        """列出所有会话"""
        session_files = self.sessions_dir.glob("session_*.json")
        return [f.stem.replace("session_", "") for f in session_files]


# ============================================================================
# 便捷函数
# ============================================================================

def quick_start(idea_text: str) -> WorkflowSession:
    """
    快速启动一个想法会话

    Args:
        idea_text: 想法描述

    Returns:
        WorkflowSession对象
    """
    engine = IdeaWorkflowEngine()
    session = engine.create_session(idea_text)

    print(f"\n✨ 想法会话已创建!")
    print(f"   会话ID: {session.session_id}")
    print(f"   想法: {idea_text[:50]}...")

    return session


# ============================================================================
# 命令行接口
# ============================================================================

def main():
    """命令行入口"""
    if sys.platform == 'win32':
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stdin.reconfigure(encoding='utf-8')

    print("\n" + "="*60)
    print("🚀 Idea Workflow Engine - 想法落地工作流引擎")
    print("="*60 + "\n")

    # 创建引擎
    engine = IdeaWorkflowEngine()

    # 列出选项
    print("请选择操作:")
    print("  1. 创建新想法会话")
    print("  2. 查看现有会话")
    print("  3. 查看工作流说明")

    choice = input("\n请输入选项 (1-3): ").strip()

    if choice == "1":
        idea = input("\n请描述您的想法: ").strip()
        if idea:
            session = engine.create_session(idea)
            engine.print_session_summary(session)

            # 自动启动第一阶段
            print("\n🎯 启动 Phase 1: 理解与澄清")
            engine.run_phase(session, "clarification")

    elif choice == "2":
        sessions = engine.list_sessions()
        if sessions:
            print(f"\n📁 现有会话 ({len(sessions)}个):")
            for sid in sessions[-5:]:  # 显示最近5个
                print(f"  - {sid}")
        else:
            print("\n暂无会话")

    elif choice == "3":
        print("\n📖 工作流阶段说明:")
        for phase_name, phase in engine.phases.items():
            print(f"\n  {phase.phase_name.upper()}")
            print(f"  └─ {phase.phase_description}")

    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()
