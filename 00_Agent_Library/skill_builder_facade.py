#!/usr/bin/env python3
"""
Skill Builder Facade - 统一技能构建入口

提供简单易用的 API 来构建 Claude 技能,支持:
- GitHub 仓库
- 文档网站
- PDF 文件
- 本地代码目录
- 多源组合

版本: v1.0.0
日期: 2026-01-16
"""

import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass

# 本地导入
from skill_seekers_adapter import (
    SkillSeekersAdapter,
    Source,
    SkillBuildResult,
    SkillSeekersAdapterError
)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SkillBuilderFacade:
    """
    技能构建器外观 - 统一入口

    简化技能构建流程,提供高层 API。
    内部使用 SkillSeekersAdapter 调用 Skill Seekers。
    """

    def __init__(
        self,
        skill_seekers_path: Optional[Path] = None,
        auto_install: bool = False,
        default_output_dir: Optional[Path] = None
    ):
        """
        初始化外观

        Args:
            skill_seekers_path: Skill Seekers 路径
            auto_install: 自动安装 Skill Seekers
            default_output_dir: 默认输出目录
        """
        # 设置默认输出目录
        if default_output_dir is None:
            workspace_root = Path(__file__).parent.parent
            default_output_dir = workspace_root / "skills" / "auto_generated"

        self.default_output_dir = Path(default_output_dir)

        # 初始化适配器
        self.adapter = SkillSeekersAdapter(
            skill_seekers_path=skill_seekers_path,
            auto_install=auto_install
        )

        logger.info("SkillBuilderFacade initialized")

    def build_from_github(
        self,
        repo_url: str,
        skill_name: Optional[str] = None,
        output_dir: Optional[Path] = None,
        enhance_with_ai: bool = True,
        include_issues: bool = True,
        include_prs: bool = False,
        **options
    ) -> SkillBuildResult:
        """
        从 GitHub 仓库构建 Claude 技能

        Args:
            repo_url: GitHub 仓库 URL
                示例: "https://github.com/fastapi/fastapi"
            skill_name: 技能名称,默认从仓库名提取
            output_dir: 输出目录,默认 skills/auto_generated/
            enhance_with_ai: 是否使用 AI 增强内容
            include_issues: 是否包含 GitHub Issues
            include_prs: 是否包含 Pull Requests
            **options: 其他选项

        Returns:
            SkillBuildResult: 构建结果

        Example:
            >>> facade = SkillBuilderFacade()
            >>> result = facade.build_from_github(
            ...     repo_url="https://github.com/fastapi/fastapi",
            ...     skill_name="fastapi"
            ... )
            >>> if result.success:
            ...     print(f"✅ 技能已生成: {result.output_path}")
        """
        logger.info(f"Building skill from GitHub: {repo_url}")

        # 合并选项
        build_options = {
            "enhance_with_ai": enhance_with_ai,
            "include_issues": include_issues,
            "include_prs": include_prs,
            **options
        }

        # 调用适配器
        result = self.adapter.build_from_github(
            repo_url=repo_url,
            skill_name=skill_name,
            output_dir=output_dir or self.default_output_dir,
            **build_options
        )

        # 质量检查
        if result.success:
            result.quality_score = self._check_quality(result.output_path)

        return result

    def build_from_docs(
        self,
        docs_url: str,
        skill_name: Optional[str] = None,
        output_dir: Optional[Path] = None,
        preset: Optional[str] = None,
        max_pages: int = 100,
        **options
    ) -> SkillBuildResult:
        """
        从文档网站构建 Claude 技能

        Args:
            docs_url: 文档网站 URL
                示例: "https://docs.python.org/"
            skill_name: 技能名称
            output_dir: 输出目录
            preset: 预设配置 (react, vue, django, fastapi, etc.)
            max_pages: 最大抓取页面数
            **options: 其他选项

        Returns:
            SkillBuildResult: 构建结果

        Example:
            >>> result = facade.build_from_docs(
            ...     docs_url="https://docs.python.org/3/",
            ...     skill_name="python-3-docs"
            ... )
        """
        logger.info(f"Building skill from documentation: {docs_url}")

        # 合并选项
        build_options = {
            "max_pages": max_pages,
            **options
        }

        if preset:
            build_options["preset"] = preset

        # 调用适配器
        result = self.adapter.build_from_docs(
            docs_url=docs_url,
            skill_name=skill_name,
            output_dir=output_dir or self.default_output_dir,
            **build_options
        )

        # 质量检查
        if result.success:
            result.quality_score = self._check_quality(result.output_path)

        return result

    def build_from_pdf(
        self,
        pdf_path: str,
        skill_name: Optional[str] = None,
        output_dir: Optional[Path] = None,
        **options
    ) -> SkillBuildResult:
        """
        从 PDF 文件构建 Claude 技能

        Args:
            pdf_path: PDF 文件路径
            skill_name: 技能名称
            output_dir: 输出目录
            **options: 其他选项

        Returns:
            SkillBuildResult: 构建结果

        Example:
            >>> result = facade.build_from_pdf(
            ...     pdf_path="docs/guide.pdf",
            ...     skill_name="user-guide"
            ... )
        """
        logger.info(f"Building skill from PDF: {pdf_path}")

        # 创建 PDF 来源
        source = Source(
            type="pdf",
            path=pdf_path,
            options=options
        )

        # 调用多源构建
        return self.build_multi_source(
            sources=[source],
            skill_name=skill_name or Path(pdf_path).stem,
            output_dir=output_dir or self.default_output_dir
        )

    def build_from_local(
        self,
        code_dir: str,
        skill_name: Optional[str] = None,
        output_dir: Optional[Path] = None,
        **options
    ) -> SkillBuildResult:
        """
        从本地代码目录构建 Claude 技能

        Args:
            code_dir: 本地代码目录路径
            skill_name: 技能名称
            output_dir: 输出目录
            **options: 其他选项

        Returns:
            SkillBuildResult: 构建结果

        Example:
            >>> result = facade.build_from_local(
            ...     code_dir="./my-project",
            ...     skill_name="my-project"
            ... )
        """
        logger.info(f"Building skill from local directory: {code_dir}")

        # 创建本地来源
        source = Source(
            type="local",
            path=code_dir,
            options=options
        )

        # 调用多源构建
        return self.build_multi_source(
            sources=[source],
            skill_name=skill_name or Path(code_dir).name,
            output_dir=output_dir or self.default_output_dir
        )

    def build_multi_source(
        self,
        sources: List[Union[Source, Dict]],
        skill_name: str,
        output_dir: Optional[Path] = None,
        resolve_conflicts: str = "rule",
        **options
    ) -> SkillBuildResult:
        """
        多源组合构建 Claude 技能

        Args:
            sources: 来源列表 (Source 对象或字典)
            skill_name: 技能名称
            output_dir: 输出目录
            resolve_conflicts: 冲突解决策略
                - "rule": 基于规则
                - "ai": AI 驱动
                - "manual": 手动解决
            **options: 其他选项

        Returns:
            SkillBuildResult: 构建结果

        Example:
            >>> sources = [
            ...     Source(type="github", url="https://github.com/facebook/react"),
            ...     Source(type="docs", url="https://react.dev/"),
            ...     Source(type="pdf", path="docs/react-guide.pdf")
            ... ]
            >>> result = facade.build_multi_source(
            ...     sources=sources,
            ...     skill_name="react-complete"
            ... )
        """
        logger.info(f"Building skill from {len(sources)} sources")

        # 标准化来源
        normalized_sources = []
        for source in sources:
            if isinstance(source, dict):
                normalized_sources.append(Source(**source))
            elif isinstance(source, Source):
                normalized_sources.append(source)
            else:
                raise ValueError(f"Invalid source type: {type(source)}")

        # 合并选项
        build_options = {
            "resolve_conflicts": resolve_conflicts,
            **options
        }

        # 调用适配器
        result = self.adapter.build_multi_source(
            sources=normalized_sources,
            skill_name=skill_name,
            output_dir=output_dir or self.default_output_dir,
            **build_options
        )

        # 质量检查
        if result.success:
            result.quality_score = self._check_quality(result.output_path)

        return result

    def package_skill(
        self,
        skill_dir: Union[str, Path],
        output_dir: Optional[Path] = None,
        target: str = "claude"
    ) -> tuple:
        """
        打包技能为可分发格式

        Args:
            skill_dir: 技能目录路径
            output_dir: 输出目录
            target: 目标平台
                - "claude": Claude AI (ZIP + YAML)
                - "gemini": Google Gemini (tar.gz)
                - "openai": OpenAI ChatGPT (ZIP + Vector Store)
                - "markdown": 通用 Markdown (ZIP)

        Returns:
            Tuple[成功标志, 包路径]

        Example:
            >>> success, package_path = facade.package_skill(
            ...     skill_dir="skills/auto_generated/react/",
            ...     target="claude"
            ... )
            >>> if success:
            ...     print(f"✅ 包已创建: {package_path}")
        """
        logger.info(f"Packaging skill: {skill_dir}")

        skill_dir = Path(skill_dir)

        # 调用适配器
        return self.adapter.package_skill(
            skill_dir=skill_dir,
            output_dir=output_dir,
            target=target
        )

    def _check_quality(self, skill_dir: Optional[Path]) -> Optional[float]:
        """检查技能质量并返回评分"""
        if skill_dir is None or not skill_dir.exists():
            return None

        try:
            # 基础质量检查
            score = 0.0

            # 检查 SKILL.md
            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                score += 30.0

                # 检查内容质量
                content = skill_md.read_text(encoding="utf-8")
                if len(content) > 1000:
                    score += 20.0
                if "## " in content:  # 有章节标题
                    score += 10.0

            # 检查 references 目录
            refs_dir = skill_dir / "references"
            if refs_dir.exists():
                ref_files = list(refs_dir.glob("**/*.md"))
                if len(ref_files) >= 3:
                    score += 20.0
                if len(ref_files) >= 10:
                    score += 10.0

            # 检查其他文件
            if (skill_dir / "scripts").exists():
                score += 5.0
            if (skill_dir / "assets").exists():
                score += 5.0

            return min(score, 100.0)

        except Exception as e:
            logger.warning(f"Quality check failed: {e}")
            return None

    def get_adapter_info(self) -> Dict[str, Any]:
        """获取适配器信息"""
        return {
            "skill_seekers_path": str(self.adapter.skill_seekers_path),
            "version": self.adapter.version,
            "available": self.adapter.skill_seekers_path.exists()
        }


# 导出
__all__ = [
    "SkillBuilderFacade",
    "Source",
    "SkillBuildResult",
    "SkillSeekersAdapterError"
]


if __name__ == "__main__":
    # 测试代码
    import sys

    # 创建外观
    facade = SkillBuilderFacade()

    # 显示信息
    info = facade.get_adapter_info()
    print(f"Skill Seekers Path: {info['skill_seekers_path']}")
    print(f"Version: {info['version']}")
    print(f"Available: {info['available']}")

    # 如果有参数,执行构建
    if len(sys.argv) > 1:
        if sys.argv[1] == "--github":
            result = facade.build_from_github(
                repo_url=sys.argv[2],
                skill_name=sys.argv[3] if len(sys.argv) > 3 else None
            )
            print(f"\nSuccess: {result.success}")
            print(f"Output: {result.output_path}")
            print(f"Quality: {result.quality_score}")
            if result.error:
                print(f"Error: {result.error}")
