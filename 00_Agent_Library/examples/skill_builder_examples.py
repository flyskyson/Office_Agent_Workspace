#!/usr/bin/env python3
"""
Skill Builder 使用示例

展示如何使用 SkillBuilderFacade 构建各种类型的 Claude 技能。

版本: v1.0.0
日期: 2026-01-16
"""

import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from skill_builder_facade import SkillBuilderFacade, Source


def example_1_github_simple():
    """示例 1: 从 GitHub 仓库简单构建"""
    print("\n" + "=" * 60)
    print("示例 1: 从 GitHub 仓库构建技能")
    print("=" * 60)

    facade = SkillBuilderFacade()

    result = facade.build_from_github(
        repo_url="https://github.com/pallets/flask",
        skill_name="flask"
    )

    if result.success:
        print(f"✅ 技能已生成: {result.output_path}")
        print(f"📊 质量评分: {result.quality_score:.1f}/100")
        print(f"⏱️ 构建耗时: {result.build_time:.1f}秒")
    else:
        print(f"❌ 构建失败: {result.error}")


def example_2_github_with_options():
    """示例 2: 带选项的 GitHub 构建"""
    print("\n" + "=" * 60)
    print("示例 2: 带完整选项的 GitHub 构建")
    print("=" * 60)

    facade = SkillBuilderFacade()

    result = facade.build_from_github(
        repo_url="https://github.com/tiangolo/fastapi",
        skill_name="fastapi-complete",
        enhance_with_ai=True,
        include_issues=True,
        include_prs=True
    )

    if result.success:
        print(f"✅ 技能已生成: {result.output_path}")
        print(f"📊 质量评分: {result.quality_score:.1f}/100")

        # 打包技能
        success, package_path = facade.package_skill(
            skill_dir=result.output_path,
            target="claude"
        )
        if success:
            print(f"📦 包已创建: {package_path}")


def example_3_documentation():
    """示例 3: 从文档网站构建"""
    print("\n" + "=" * 60)
    print("示例 3: 从文档网站构建技能")
    print("=" * 60)

    facade = SkillBuilderFacade()

    result = facade.build_from_docs(
        docs_url="https://docs.python.org/3/",
        skill_name="python-3-docs",
        preset="python",
        max_pages=50
    )

    if result.success:
        print(f"✅ 技能已生成: {result.output_path}")
        print(f"📊 质量评分: {result.quality_score:.1f}/100")


def example_4_multi_source():
    """示例 4: 多源组合构建"""
    print("\n" + "=" * 60)
    print("示例 4: 多源组合构建")
    print("=" * 60)

    facade = SkillBuilderFacade()

    # 定义多个来源
    sources = [
        Source(type="github", url="https://github.com/facebook/react"),
        Source(type="docs", url="https://react.dev/"),
    ]

    result = facade.build_multi_source(
        sources=sources,
        skill_name="react-complete",
        resolve_conflicts="rule"
    )

    if result.success:
        print(f"✅ 技能已生成: {result.output_path}")
        print(f"📊 质量评分: {result.quality_score:.1f}/100")
        print(f"📝 元数据: {result.metadata}")


def example_5_batch_build():
    """示例 5: 批量构建技能"""
    print("\n" + "=" * 60)
    print("示例 5: 批量构建多个框架的技能")
    print("=" * 60)

    # 要构建的仓库列表
    repos = [
        ("https://github.com/django/django", "django"),
        ("https://github.com/pallets/flask", "flask"),
        ("https://github.com/tornadoweb/tornado", "tornado"),
    ]

    facade = SkillBuilderFacade()
    results = []

    for repo_url, skill_name in repos:
        print(f"\n🔨 构建 {skill_name}...")

        result = facade.build_from_github(
            repo_url=repo_url,
            skill_name=skill_name,
            enhance_with_ai=True
        )

        results.append((skill_name, result))

    # 汇总结果
    print("\n" + "=" * 60)
    print("构建结果汇总")
    print("=" * 60)

    success_count = sum(1 for _, r in results if r.success)

    for skill_name, result in results:
        status = "✅" if result.success else "❌"
        quality = f"{result.quality_score:.1f}/100" if result.quality_score else "N/A"
        print(f"{status} {skill_name:20s} - 质量: {quality}")

    print(f"\n总计: {success_count}/{len(repos)} 成功")


def example_6_workflow_integration():
    """示例 6: 与工作流引擎集成"""
    print("\n" + "=" * 60)
    print("示例 6: 与工作流引擎集成")
    print("=" * 60)

    try:
        from workflow_engine import WorkflowEngine

        # 创建工作流
        workflow = WorkflowEngine(name="skill_building_workflow")

        # 定义技能构建步骤
        def build_skill_step(context):
            facade = SkillBuilderFacade()

            result = facade.build_from_github(
                repo_url=context["repo_url"],
                skill_name=context["skill_name"]
            )

            return {
                "skill_path": str(result.output_path),
                "quality_score": result.quality_score,
                "success": result.success
            }

        # 添加步骤
        workflow.add_step("build_skill", build_skill_step)

        # 执行工作流
        result = workflow.execute({
            "repo_url": "https://github.com/sveltejs/svelte",
            "skill_name": "svelte"
        })

        print(f"✅ 工作流执行完成")
        print(f"结果: {result}")

    except ImportError:
        print("⚠️ workflow_engine 未找到,跳过此示例")


def example_7_custom_post_processing():
    """示例 7: 自定义后处理"""
    print("\n" + "=" * 60)
    print("示例 7: 自定义后处理")
    print("=" * 60)

    import json
    from datetime import datetime

    facade = SkillBuilderFacade()

    result = facade.build_from_github(
        repo_url="https://github.com/psf/requests",
        skill_name="requests"
    )

    if result.success:
        # 添加自定义元数据
        metadata = {
            "created_by": "Office Agent Workspace",
            "created_at": datetime.now().isoformat(),
            "version": "1.0.0",
            "auto_generated": True,
            "quality_score": result.quality_score
        }

        metadata_file = result.output_path / "metadata.json"
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        print(f"✅ 技能已生成并增强: {result.output_path}")
        print(f"📝 元数据已添加: {metadata_file}")


def example_8_quality_check():
    """示例 8: 质量检查和验证"""
    print("\n" + "=" * 60)
    print("示例 8: 质量检查和验证")
    print("=" * 60)

    facade = SkillBuilderFacade()

    # 构建技能
    result = facade.build_from_github(
        repo_url="https://github.com/scikit-learn/scikit-learn",
        skill_name="scikit-learn"
    )

    if result.success:
        print(f"✅ 技能已生成: {result.output_path}")
        print(f"📊 质量评分: {result.quality_score:.1f}/100")

        # 详细质量检查
        skill_dir = result.output_path

        # 检查必需文件
        required_files = ["SKILL.md"]
        for file in required_files:
            path = skill_dir / file
            if path.exists():
                size = path.stat().st_size
                print(f"  ✅ {file}: {size} bytes")
            else:
                print(f"  ❌ {file}: 缺失")

        # 检查目录
        directories = ["references", "scripts", "assets"]
        for dir_name in directories:
            path = skill_dir / dir_name
            if path.exists():
                file_count = len(list(path.rglob("*")))
                print(f"  ✅ {dir_name}/: {file_count} files")
            else:
                print(f"  ⚠️ {dir_name}/: 不存在")


def main():
    """运行所有示例"""
    print("\n" + "=" * 70)
    print(" " * 15 + "Skill Builder 使用示例")
    print("=" * 70)

    examples = [
        ("GitHub 简单构建", example_1_github_simple),
        ("GitHub 完整选项", example_2_github_with_options),
        ("文档网站构建", example_3_documentation),
        ("多源组合构建", example_4_multi_source),
        ("批量构建", example_5_batch_build),
        ("工作流集成", example_6_workflow_integration),
        ("自定义后处理", example_7_custom_post_processing),
        ("质量检查", example_8_quality_check),
    ]

    print("\n可用示例:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")

    print("\n选择要运行的示例 (1-8, 或 'all' 运行所有):")
    choice = input("> ").strip()

    if choice.lower() == "all":
        for name, func in examples:
            try:
                func()
            except Exception as e:
                print(f"\n❌ 示例 '{name}' 执行失败: {e}")
    elif choice.isdigit() and 1 <= int(choice) <= len(examples):
        idx = int(choice) - 1
        name, func = examples[idx]
        try:
            func()
        except Exception as e:
            print(f"\n❌ 示例 '{name}' 执行失败: {e}")
    else:
        print("❌ 无效选择")


if __name__ == "__main__":
    main()
