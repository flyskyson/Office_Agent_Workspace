# Skill Seekers 集成指南

**版本**: v1.0.0
**日期**: 2026-01-16
**状态**: 设计文档

---

## 📋 目录

1. [集成概述](#集成概述)
2. [架构设计](#架构设计)
3. [核心组件](#核心组件)
4. [使用指南](#使用指南)
5. [API 参考](#api-参考)
6. [示例代码](#示例代码)
7. [故障排查](#故障排查)

---

## 🎯 集成概述

### 设计目标

将 **Skill Seekers** 的 MCP 技能自动构建能力集成到 Office Agent Workspace 中,实现:

1. **🚀 一键技能生成** - 从任意 GitHub 仓库/文档自动生成 Claude 技能
2. **🔄 工作流集成** - 与现有 `AgentSupervisor` 和 `WorkflowEngine` 无缝集成
3. **📦 标准化输出** - 生成符合 Claude 规范的技能包
4. **🤖 AI 增强** - 利用 Skill Seekers 的 AI 增强能力优化技能质量

### 集成方式

```
Office Agent Workspace (宿主)
    │
    ├─→ 00_Agent_Library/
    │   ├─→ skill_builder_facade.py     ← 统一入口 (新增)
    │   ├─→ skill_seekers_adapter.py    ← Skill Seekers 适配器 (新增)
    │   └─→ skill_quality_checker.py    ← 质量检查器 (新增)
    │
    ├─→ external/                        ← 外部工具目录 (新增)
    │   └─→ skill_seekers/               ← Skill Seekers (Git Submodule)
    │
    └─→ skills/                          ← 技能输出目录
        ├─→ auto_generated/              ← 自动生成的技能 (新增)
        └─→ ...
```

---

## 🏗️ 架构设计

### 分层架构

```
┌─────────────────────────────────────────────────────────────┐
│                    应用层 (Application Layer)                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ 想法落地工作流  │  │ 超级管家模式   │  │ 技能构建命令   │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
└─────────┼──────────────────┼──────────────────┼─────────────┘
          │                  │                  │
┌─────────┼──────────────────┼──────────────────┼─────────────┐
│         ↓                  ↓                  ↓              │
│              ┌─────────────────────────┐                    │
│              │   Skill Builder Facade   │ ← 统一入口         │
│              │   (skill_builder_facade) │                    │
│              └─────────────┬───────────┘                    │
│                            │                                │
│              ┌─────────────┴───────────┐                    │
│              │   Skill Seekers Adapter  │ ← 适配器层         │
│              │  (skill_seekers_adapter) │                    │
│              └─────────────┬───────────┘                    │
│                            │                                │
│         ┌──────────────────┼──────────────────┐            │
│         ↓                  ↓                  ↓            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ 文档抓取     │  │ GitHub 分析  │  │ PDF 处理     │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
                            │
┌───────────────────────────┼───────────────────────────────┐
│                           ↓                                │
│              ┌─────────────────────────┐                   │
│              │   External Skill Seekers│ ← 外部依赖         │
│              │   (Git Submodule)       │                   │
│              └─────────────────────────┘                   │
└────────────────────────────────────────────────────────────┘
```

### 数据流

```
输入源 (Source)
    ├─ GitHub 仓库 URL
    ├─ 文档网站 URL
    ├─ PDF 文件路径
    └─ 本地代码目录
        ↓
┌───────────────────────────┐
│  Skill Builder Facade     │ ← 解析输入、验证参数
└───────────┬───────────────┘
            ↓
┌───────────────────────────┐
│  Skill Seekers Adapter    │ ← 调用 Skill Seekers
└───────────┬───────────────┘
            ↓
┌───────────────────────────┐
│  外部 Skill Seekers       │ ← 执行实际构建
│  - 文档抓取                │
│  - 代码分析                │
│  - AI 增强                │
│  - 技能打包                │
└───────────┬───────────────┘
            ↓
      输出技能包 (Output)
    ├─ SKILL.md
    ├─ references/
    ├─ scripts/
    └─ skill.zip
```

---

## 🔧 核心组件

### 1. Skill Builder Facade (skill_builder_facade.py)

**职责**: 统一入口,提供高层 API

```python
class SkillBuilderFacade:
    """技能构建器外观 - 统一入口"""

    def build_from_github(self, repo_url: str, **options) -> SkillBuildResult
    def build_from_docs(self, docs_url: str, **options) -> SkillBuildResult
    def build_from_pdf(self, pdf_path: str, **options) -> SkillBuildResult
    def build_from_local(self, code_dir: str, **options) -> SkillBuildResult
    def build_multi_source(self, sources: List[Source], **options) -> SkillBuildResult
```

### 2. Skill Seekers Adapter (skill_seekers_adapter.py)

**职责**: 适配 Skill Seekers,处理版本兼容性

```python
class SkillSeekersAdapter:
    """Skill Seekers 适配器"""

    def __init__(self, skill_seekers_path: Path)
    def is_available(self) -> bool
    def get_version(self) -> str
    def call_unified_builder(self, config: dict) -> BuildResult
    def call_packager(self, skill_dir: Path) -> PackageResult
```

### 3. Skill Quality Checker (skill_quality_checker.py)

**职责**: 质量检查,验证生成的技能

```python
class SkillQualityChecker:
    """技能质量检查器"""

    def check_skill_directory(self, skill_dir: Path) -> QualityReport
    def validate_skill_md(self, skill_md_path: Path) -> bool
    def check_references(self, references_dir: Path) -> List[Issue]
    def estimate_quality_score(self, skill_dir: Path) -> float
```

### 4. 集成工作流模板 (workflow_templates/skill_building.py)

**职责**: 可复用的技能构建工作流

```python
SKILL_BUILDING_TEMPLATE = {
    "name": "skill_building",
    "steps": [
        "validate_input",
        "fetch_source",
        "analyze_content",
        "generate_skill",
        "quality_check",
        "package_skill"
    ]
}
```

---

## 📖 使用指南

### 场景 1: 从 GitHub 仓库构建技能

```python
from 00_Agent_Library.skill_builder_facade import SkillBuilderFacade

# 初始化
facade = SkillBuilderFacade()

# 从 GitHub 仓库构建
result = facade.build_from_github(
    repo_url="https://github.com/facebook/react",
    skill_name="react",
    output_dir="skills/auto_generated/"
)

if result.success:
    print(f"✅ 技能已生成: {result.output_path}")
else:
    print(f"❌ 构建失败: {result.error}")
```

### 场景 2: 多源组合构建

```python
from 00_Agent_Library.skill_builder_facade import SkillBuilderFacade, Source

# 定义多个来源
sources = [
    Source(type="github", url="https://github.com/facebook/react"),
    Source(type="docs", url="https://react.dev/"),
    Source(type="pdf", path="docs/react-guide.pdf")
]

# 统一构建
result = facade.build_multi_source(
    sources=sources,
    skill_name="react-complete",
    output_dir="skills/auto_generated/"
)
```

### 场景 3: 与工作流引擎集成

```python
from 00_Agent_Libraries.workflow_engine import WorkflowEngine
from 00_Agent_Libraries.skill_builder_facade import SkillBuilderFacade

# 创建工作流
workflow = WorkflowEngine()

# 添加技能构建步骤
@workflow.step("build_skill")
def build_skill_step(context):
    facade = SkillBuilderFacade()
    result = facade.build_from_github(context["repo_url"])

    return {
        "skill_path": result.output_path,
        "quality_score": result.quality_score
    }

# 执行工作流
result = workflow.execute({
    "repo_url": "https://github.com/fastapi/fastapi"
})
```

### 场景 4: CLI 命令

```bash
# 从 GitHub 仓库构建技能
python -m 00_Agent_Library.skill_builder_facade \
    --source github \
    --url https://github.com/facebook/react \
    --output skills/auto_generated/

# 从文档网站构建
python -m 00_Agent_Library.skill_builder_facade \
    --source docs \
    --url https://docs.python.org/ \
    --output skills/auto_generated/

# 多源构建
python -m 00_Agent_Library.skill_builder_facade \
    --multi-source config/react-multi-source.json \
    --output skills/auto_generated/
```

---

## 📚 API 参考

### SkillBuilderFacade

#### `build_from_github(repo_url: str, **options) -> SkillBuildResult`

从 GitHub 仓库构建 Claude 技能

**参数**:
- `repo_url` (str): GitHub 仓库 URL
- `skill_name` (str, 可选): 技能名称,默认从仓库名提取
- `output_dir` (str, 可选): 输出目录,默认 `skills/auto_generated/`
- `enhance_with_ai` (bool, 可选): 是否使用 AI 增强,默认 True
- `include_issues` (bool, 可选): 是否包含 GitHub Issues,默认 True
- `include_prs` (bool, 可选): 是否包含 PRs,默认 False

**返回**: `SkillBuildResult`
- `success` (bool): 是否成功
- `output_path` (Path): 输出路径
- `quality_score` (float): 质量评分 (0-100)
- `error` (str): 错误信息 (如果失败)

**示例**:
```python
result = facade.build_from_github(
    repo_url="https://github.com/fastapi/fastapi",
    skill_name="fastapi",
    include_issues=True
)
```

#### `build_from_docs(docs_url: str, **options) -> SkillBuildResult`

从文档网站构建 Claude 技能

**参数**:
- `docs_url` (str): 文档网站 URL
- `preset` (str, 可选): 预设配置 (react, vue, django, etc.)
- `max_pages` (int, 可选): 最大页面数,默认 100

#### `build_multi_source(sources: List[Source], **options) -> SkillBuildResult`

多源组合构建

**参数**:
- `sources` (List[Source]): 来源列表
- `resolve_conflicts` (str, 可选): 冲突解决策略 ("rule", "ai", "manual")

### Source 类

```python
@dataclass
class Source:
    type: str  # "github", "docs", "pdf", "local"
    url: Optional[str] = None
    path: Optional[str] = None
    options: Dict[str, Any] = field(default_factory=dict)
```

### SkillBuildResult 类

```python
@dataclass
class SkillBuildResult:
    success: bool
    output_path: Optional[Path] = None
    quality_score: Optional[float] = None
    error: Optional[str] = None
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
```

---

## 💡 示例代码

### 示例 1: 批量构建技能

```python
from pathlib import Path
from 00_Agent_Library.skill_builder_facade import SkillBuilderFacade

# 仓库列表
repos = [
    "https://github.com/facebook/react",
    "https://github.com/vuejs/vue",
    "https://github.com/angular/angular",
    "https://github.com/sveltejs/svelte"
]

# 批量构建
facade = SkillBuilderFacade()
results = []

for repo in repos:
    print(f"Building skill for {repo}...")
    result = facade.build_from_github(
        repo_url=repo,
        output_dir="skills/frontend_frameworks/"
    )
    results.append(result)

# 汇总报告
success_count = sum(1 for r in results if r.success)
print(f"\n✅ 成功: {success_count}/{len(repos)}")
```

### 示例 2: 与 AgentSupervisor 集成

```python
from 00_Agent_Library.agent_supervisor import AgentSupervisor
from 00_Agent_Library.skill_builder_facade import SkillBuilderFacade

# 创建智能体监督者
supervisor = AgentSupervisor()

# 注册技能构建智能体
@supervisor.agent("skill_builder")
def skill_builder_agent(task):
    facade = SkillBuilderFacade()

    if task["type"] == "github":
        return facade.build_from_github(task["url"])
    elif task["type"] == "docs":
        return facade.build_from_docs(task["url"])
    else:
        return {"error": "Unknown task type"}

# 分配任务
task = {
    "type": "github",
    "url": "https://github.com/pallets/flask"
}

result = supervisor.delegate("skill_builder", task)
```

### 示例 3: 自定义后处理

```python
from 00_Agent_Library.skill_builder_facade import SkillBuilderFacade

facade = SkillBuilderFacade()

# 构建技能
result = facade.build_from_github(
    repo_url="https://github.com/tiangolo/fastapi"
)

if result.success:
    # 自定义后处理
    skill_dir = result.output_path

    # 添加自定义配置
    config = {
        "created_by": "Office Agent Workspace",
        "version": "1.0.0",
        "auto_generated": True
    }

    # 保存元数据
    import json
    with open(skill_dir / "metadata.json", "w") as f:
        json.dump(config, f, indent=2)

    print(f"✅ 技能已增强: {skill_dir}")
```

---

## 🔍 故障排查

### 问题 1: Skill Seekers 未安装

**症状**: `SkillSeekersAdapterError: Skill Seekers not found`

**解决方案**:
```bash
cd external/
git clone https://github.com/yusufkaraaslan/Skill_Seekers.git
cd Skill_Seekers
pip install -e .
```

### 问题 2: 依赖冲突

**症状**: `ImportError: cannot import name 'X'`

**解决方案**: 使用虚拟环境隔离
```bash
python -m venv venv_skill_seekers
source venv_skill_seekers/bin/activate  # Linux/Mac
# 或 venv_skill_seekers\Scripts\activate  # Windows
pip install skill-seekers
```

### 问题 3: MCP 配置错误

**症状**: 构建成功但 Claude 无法识别技能

**解决方案**: 检查 `SKILL.md` 格式
```bash
python -m 00_Agent_Library.skill_quality_checker \
    --skill-dir skills/auto_generated/react/
```

---

## 📦 依赖关系

```
Office Agent Workspace
    │
    ├─ Skill Seekers (External)
    │   ├─ FastMCP
    │   ├─ Pydantic
    │   ├─ httpx
    │   └─ ...
    │
    └─ 本地依赖
        ├─ agent_supervisor.py
        ├─ workflow_engine.py
        ├─ config_center.py
        └─ exceptions.py
```

---

## 🚀 未来扩展

- [ ] 支持更多源类型 (视频、音频)
- [ ] 自动化技能更新机制
- [ ] 技能依赖关系分析
- [ ] 技能性能基准测试
- [ ] 技能市场集成

---

**文档版本**: v1.0.0
**最后更新**: 2026-01-16
**维护者**: Claude Code (GLM-4.7)
