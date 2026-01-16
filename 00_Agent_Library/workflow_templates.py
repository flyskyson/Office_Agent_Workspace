#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工作流模板系统 - Workflow Templates
为 Office Agent Workspace 提供可复用的工作流模板

作者: Claude Code
日期: 2026-01-16
版本: 1.0.0
"""

import sys
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
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


# ============================================================================
# 工作流模板定义
# ============================================================================

class WorkflowTemplate:
    """工作流模板基类"""

    def __init__(
        self,
        name: str,
        description: str,
        category: str,
        version: str = "1.0.0"
    ):
        self.name = name
        self.description = description
        self.category = category
        self.version = version
        self.steps: List[Dict[str, Any]] = []
        self.parameters: Dict[str, Any] = {}
        self.created_at = datetime.now()

    def add_step(
        self,
        agent: str,
        action: str,
        params: Dict[str, Any] = None,
        condition: str = None
    ):
        """
        添加工作流步骤

        参数:
            agent: 智能体名称
            action: 操作名称
            params: 参数
            condition: 执行条件（可选）
        """
        step = {
            "agent": agent,
            "action": action,
            "params": params or {},
            "condition": condition
        }
        self.steps.append(step)
        return self

    def add_parameter(
        self,
        name: str,
        type: str,
        default: Any = None,
        required: bool = False,
        description: str = ""
    ):
        """
        添加参数定义

        参数:
            name: 参数名
            type: 参数类型
            default: 默认值
            required: 是否必需
            description: 描述
        """
        self.parameters[name] = {
            "type": type,
            "default": default,
            "required": required,
            "description": description
        }
        return self

    def to_dict(self) -> Dict[str, Any]:
        """导出为字典"""
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "version": self.version,
            "steps": self.steps,
            "parameters": self.parameters,
            "created_at": self.created_at.isoformat()
        }

    def save(self, directory: Path) -> Path:
        """保存到文件"""
        directory.mkdir(parents=True, exist_ok=True)
        filename = f"{self.name.lower().replace(' ', '_')}.yaml"
        filepath = directory / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(self.to_dict(), f, allow_unicode=True, default_flow_style=False)

        return filepath


# ============================================================================
# 预定义工作流模板
# ============================================================================

class LicenseApplicationTemplate(WorkflowTemplate):
    """证照申请完整流程模板"""

    def __init__(self):
        super().__init__(
            name="证照申请完整流程",
            description="从材料扫描到申请表生成的完整流程",
            category="证照管理",
            version="1.0.0"
        )

        # 参数定义
        self.add_parameter("operator_name", "string", required=True, description="经营者姓名")
        self.add_parameter("id_card", "string", required=True, description="身份证号")
        self.add_parameter("material_path", "string", default=".", description="材料目录路径")
        self.add_parameter("business_name", "string", default="", description="商铺名称")
        self.add_parameter("business_address", "string", default="", description="经营地址")

        # 工作流步骤
        self.add_step(
            agent="file_organizer",
            action="scan",
            params={"path": "${material_path}"}
        ).add_step(
            agent="memory",
            action="search",
            params={"keyword": "${operator_name}"}
        ).add_step(
            agent="market_supervision",
            action="generate_application",
            params={
                "operator_name": "${operator_name}",
                "id_card": "${id_card}",
                "business_name": "${business_name}",
                "business_address": "${business_address}"
            }
        ).add_step(
            agent="memory",
            action="add_note",
            params={
                "title": "申请记录: ${operator_name}",
                "content": "身份证: ${id_card}, 商铺: ${business_name}",
                "category": "证照申请"
            }
        )


class DailyNewsSummaryTemplate(WorkflowTemplate):
    """每日新闻摘要模板"""

    def __init__(self):
        super().__init__(
            name="每日新闻摘要",
            description="获取热点新闻并生成日报",
            category="资讯管理",
            version="1.0.0"
        )

        # 参数定义
        self.add_parameter("platforms", "list", default=["weibo", "zhihu", "bilibili"], description="新闻平台")
        self.add_parameter("count", "integer", default=20, description="获取数量")
        self.add_parameter("keywords", "list", default=[], description="关键词过滤")

        # 工作流步骤
        self.add_step(
            agent="news_scraper",
            action="fetch",
            params={
                "platforms": "${platforms}",
                "count": "${count}"
            }
        ).add_step(
            agent="memory",
            action="search",
            params={"keyword": "${keywords[0] if keywords else ''}"}
        ).add_step(
            agent="memory",
            action="add_note",
            params={
                "title": "新闻日报 ${datetime.now().strftime('%Y-%m-%d')}",
                "content": "今日热点新闻摘要",
                "category": "新闻"
            }
        )


class FileOrganizeTemplate(WorkflowTemplate):
    """文件整理模板"""

    def __init__(self):
        super().__init__(
            name="智能文件整理",
            description="按类型和日期整理文件",
            category="文件管理",
            version="1.0.0"
        )

        # 参数定义
        self.add_parameter("source_path", "string", required=True, description="源目录")
        self.add_parameter("target_path", "string", required=True, description="目标目录")
        self.add_parameter("rules", "dict", default={}, description="整理规则")
        self.add_parameter("create_backup", "boolean", default=True, description="是否创建备份")

        # 工作流步骤
        self.add_step(
            agent="file_organizer",
            action="scan",
            params={"path": "${source_path}"}
        ).add_step(
            agent="file_organizer",
            action="organize",
            params={
                "source": "${source_path}",
                "target": "${target_path}",
                "rules": "${rules}"
            }
        ).add_step(
            agent="memory",
            action="add_note",
            params={
                "title": "文件整理记录 ${datetime.now().strftime('%Y-%m-%d')}",
                "content": "整理了 ${source_path} 到 ${target_path}",
                "category": "文件管理"
            }
        )


class KnowledgeIndexTemplate(WorkflowTemplate):
    """知识索引模板"""

    def __init__(self):
        super().__init__(
            name="知识库索引更新",
            description="扫描笔记并更新向量索引",
            category="知识管理",
            version="1.0.0"
        )

        # 参数定义
        self.add_parameter("notes_path", "string", required=True, description="笔记目录")
        self.add_parameter("index_type", "string", default="vector", description="索引类型")

        # 工作流步骤
        self.add_step(
            agent="file_organizer",
            action="scan",
            params={"path": "${notes_path}"}
        ).add_step(
            agent="memory",
            action="batch_add_notes",
            params={"source": "${notes_path}"}
        ).add_step(
            agent="memory",
            action="rebuild_index",
            params={"type": "${index_type}"}
        )


# ============================================================================
# 工作流模板管理器
# ============================================================================

class WorkflowTemplateManager:
    """
    工作流模板管理器

    功能:
    1. 模板注册和发现
    2. 模板参数验证
    3. 模板实例化
    4. 模板导出和导入
    """

    def __init__(self, templates_dir: Path = None):
        """
        初始化模板管理器

        参数:
            templates_dir: 模板目录
        """
        if templates_dir is None:
            workspace_root = Path(__file__).parent.parent
            templates_dir = workspace_root / "00_Agent_Library" / "workflow_templates"

        self.templates_dir = Path(templates_dir)
        self.templates_dir.mkdir(parents=True, exist_ok=True)

        # 模板注册表
        self.templates: Dict[str, WorkflowTemplate] = {}

        # 注册内置模板
        self._register_builtin_templates()

        # 加载用户模板
        self._load_user_templates()

        print(f"[INFO] 工作流模板管理器初始化完成")
        print(f"[INFO] 模板目录: {self.templates_dir}")
        print(f"[INFO] 已加载 {len(self.templates)} 个模板")

    def _register_builtin_templates(self):
        """注册内置模板"""
        builtin_templates = [
            LicenseApplicationTemplate(),
            DailyNewsSummaryTemplate(),
            FileOrganizeTemplate(),
            KnowledgeIndexTemplate()
        ]

        for template in builtin_templates:
            self.register(template)

    def _load_user_templates(self):
        """加载用户自定义模板"""
        if not self.templates_dir.exists():
            return

        for template_file in self.templates_dir.glob("*.yaml"):
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)

                # 创建模板对象
                template = WorkflowTemplate(
                    name=data["name"],
                    description=data["description"],
                    category=data["category"],
                    version=data.get("version", "1.0.0")
                )
                template.steps = data.get("steps", [])
                template.parameters = data.get("parameters", {})

                self.register(template)

            except Exception as e:
                print(f"[WARN] 加载模板失败 {template_file}: {e}")

    def register(self, template: WorkflowTemplate):
        """注册模板"""
        self.templates[template.name] = template
        print(f"[INFO] 注册模板: {template.name}")

    def get(self, name: str) -> Optional[WorkflowTemplate]:
        """获取模板"""
        return self.templates.get(name)

    def list_templates(
        self,
        category: str = None
    ) -> List[WorkflowTemplate]:
        """
        列出模板

        参数:
            category: 分类过滤（可选）

        返回:
            模板列表
        """
        templates = list(self.templates.values())

        if category:
            templates = [t for t in templates if t.category == category]

        return sorted(templates, key=lambda t: t.name)

    def list_categories(self) -> List[str]:
        """列出所有分类"""
        categories = set(t.category for t in self.templates.values())
        return sorted(categories)

    def instantiate(
        self,
        template_name: str,
        parameters: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        实例化模板（替换参数）

        参数:
            template_name: 模板名称
            parameters: 参数值

        返回:
            实例化后的工作流步骤
        """
        template = self.get(template_name)
        if not template:
            raise ValueError(f"模板不存在: {template_name}")

        # 验证参数
        self._validate_parameters(template, parameters)

        # 替换参数
        steps = []
        for step in template.steps:
            instantiated_step = deepcopy(step)

            # 替换 params 中的参数引用
            for key, value in instantiated_step["params"].items():
                instantiated_step["params"][key] = self._substitute_params(
                    value,
                    parameters
                )

            steps.append(instantiated_step)

        return steps

    def _validate_parameters(
        self,
        template: WorkflowTemplate,
        parameters: Dict[str, Any]
    ):
        """验证参数"""
        for param_name, param_def in template.parameters.items():
            if param_def.get("required") and param_name not in parameters:
                raise ValueError(f"缺少必需参数: {param_name}")

    def _substitute_params(
        self,
        value: Any,
        parameters: Dict[str, Any]
    ) -> Any:
        """替换参数引用"""
        if isinstance(value, str):
            # 简单的 ${param} 替换
            if value.startswith("${") and value.endswith("}"):
                param_name = value[2:-1]
                # 支持嵌套访问（如 datetime.now()）
                if "." in param_name and not param_name.startswith("parameters"):
                    # 处理特殊表达式
                    if param_name.startswith("datetime.now()"):
                        return eval(param_name)
                return parameters.get(param_name, value)
            return value
        elif isinstance(value, list):
            return [self._substitute_params(v, parameters) for v in value]
        elif isinstance(value, dict):
            return {k: self._substitute_params(v, parameters) for k, v in value.items()}
        else:
            return value

    def export_template(
        self,
        template_name: str,
        output_path: Path = None
    ) -> Path:
        """导出模板"""
        template = self.get(template_name)
        if not template:
            raise ValueError(f"模板不存在: {template_name}")

        if output_path is None:
            output_path = self.templates_dir / f"{template_name.lower().replace(' ', '_')}.yaml"

        return template.save(self.templates_dir)

    def save_all_templates(self):
        """保存所有模板"""
        for template in self.templates.values():
            template.save(self.templates_dir)
        print(f"[INFO] 已保存 {len(self.templates)} 个模板")


# ============================================================================
# 命令行接口
# ============================================================================

def main():
    """命令行接口"""
    print("=" * 60)
    print("工作流模板管理器")
    print("=" * 60)

    manager = WorkflowTemplateManager()

    # 显示分类
    print("\n[模板分类]")
    for category in manager.list_categories():
        print(f"  - {category}")

    # 显示所有模板
    print("\n[所有模板]")
    for template in manager.list_templates():
        print(f"\n  📋 {template.name}")
        print(f"     描述: {template.description}")
        print(f"     分类: {template.category}")
        print(f"     版本: {template.version}")
        print(f"     步骤数: {len(template.steps)}")
        if template.parameters:
            print(f"     参数:")
            for param_name, param_def in template.parameters.items():
                required = "必需" if param_def.get("required") else "可选"
                default = f" (默认: {param_def['default']})" if param_def.get('default') else ""
                print(f"       - {param_name}: {required}{default}")

    # 示例：实例化模板
    print("\n[示例] 实例化 '证照申请完整流程' 模板")
    try:
        steps = manager.instantiate(
            "证照申请完整流程",
            {
                "operator_name": "张三",
                "id_card": "123456789012345678",
                "business_name": "张三商铺",
                "business_address": "北京市朝阳区xxx"
            }
        )

        print(f"\n  生成了 {len(steps)} 步工作流:")
        for i, step in enumerate(steps, 1):
            print(f"    [{i}] {step['agent']}.{step['action']}")
            print(f"        参数: {json.dumps(step['params'], ensure_ascii=False)}")

    except Exception as e:
        print(f"  ❌ 错误: {e}")

    # 保存所有模板
    print("\n[保存模板]")
    manager.save_all_templates()

    print("\n" + "=" * 60)
    print("✅ 工作流模板管理器测试完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
