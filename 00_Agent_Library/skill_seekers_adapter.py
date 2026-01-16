#!/usr/bin/env python3
"""
Skill Seekers 适配器

将 Skill Seekers 的功能集成到 Office Agent Workspace 中。

功能:
- 统一的技能构建接口
- 版本兼容性处理
- 错误处理和日志记录
- 质量检查集成

版本: v1.0.0
日期: 2026-01-16
"""

import sys
import json
import subprocess
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

# 本地导入
try:
    from exceptions import (
        WorkspaceError,
        ErrorCode,
        handle_errors,
        ErrorContext
    )
except ImportError:
    # 如果无法导入,使用基础错误类
    class WorkspaceError(Exception):
        pass
    class ErrorCode:
        DEPENDENCY_NOT_FOUND = "DEPENDENCY_NOT_FOUND"
        INVALID_INPUT = "INVALID_INPUT"
        BUILD_FAILED = "BUILD_FAILED"
    def handle_errors(func):
        return func
    class ErrorContext:
        pass

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class Source:
    """技能构建来源"""
    type: str  # "github", "docs", "pdf", "local"
    url: Optional[str] = None
    path: Optional[str] = None
    options: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "type": self.type,
            "url": self.url,
            "path": str(self.path) if self.path else None,
            "options": self.options
        }


@dataclass
class SkillBuildResult:
    """技能构建结果"""
    success: bool
    output_path: Optional[Path] = None
    quality_score: Optional[float] = None
    error: Optional[str] = None
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    build_time: Optional[float] = None  # 构建耗时(秒)

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "success": self.success,
            "output_path": str(self.output_path) if self.output_path else None,
            "quality_score": self.quality_score,
            "error": self.error,
            "warnings": self.warnings,
            "metadata": self.metadata,
            "build_time": self.build_time
        }


class SkillSeekersAdapterError(WorkspaceError):
    """Skill Seekers 适配器错误"""
    pass


class SkillSeekersAdapter:
    """
    Skill Seekers 适配器

    提供统一的接口来调用 Skill Seekers 的功能。
    处理版本兼容性、依赖检查和错误处理。
    """

    def __init__(
        self,
        skill_seekers_path: Optional[Path] = None,
        auto_install: bool = False
    ):
        """
        初始化适配器

        Args:
            skill_seekers_path: Skill Seekers 路径,默认为 external/skill_seekers/
            auto_install: 如果未安装是否自动安装
        """
        if skill_seekers_path is None:
            # 默认路径
            workspace_root = Path(__file__).parent.parent
            skill_seekers_path = workspace_root / "external" / "skill_seekers"

        self.skill_seekers_path = skill_seekers_path
        self.auto_install = auto_install

        # 检查可用性
        self._check_availability()

        # 版本信息
        self.version = self._get_version()

        logger.info(f"SkillSeekersAdapter initialized: v{self.version}")

    def _check_availability(self) -> None:
        """检查 Skill Seekers 是否可用"""
        # 检查路径是否存在
        if not self.skill_seekers_path.exists():
            if self.auto_install:
                logger.warning(f"Skill Seekers not found at {self.skill_seekers_path}")
                logger.info("Attempting to install...")
                self._install_skill_seekers()
            else:
                raise SkillSeekersAdapterError(
                    f"Skill Seekers not found at {self.skill_seekers_path}. "
                    f"Please install it first or set auto_install=True.",
                    code=ErrorCode.DEPENDENCY_NOT_FOUND
                )

        # 检查是否可以导入
        try:
            sys.path.insert(0, str(self.skill_seekers_path))
            import src.skill_seekers as ss
            logger.debug("Skill Seekers module imported successfully")
        except ImportError as e:
            raise SkillSeekersAdapterError(
                f"Failed to import Skill Seekers: {e}",
                code=ErrorCode.DEPENDENCY_NOT_FOUND
            )

    def _install_skill_seekers(self) -> None:
        """安装 Skill Seekers"""
        external_dir = self.skill_seekers_path.parent
        external_dir.mkdir(parents=True, exist_ok=True)

        # 克隆仓库
        subprocess.run(
            ["git", "clone", "https://github.com/yusufkaraaslan/Skill_Seekers.git"],
            cwd=external_dir,
            check=True
        )

        # 安装依赖
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-e", "."],
            cwd=self.skill_seekers_path,
            check=True
        )

        logger.info(f"✅ Skill Seekers installed at {self.skill_seekers_path}")

    def _get_version(self) -> str:
        """获取 Skill Seekers 版本"""
        try:
            version_file = self.skill_seekers_path / "pyproject.toml"
            if version_file.exists():
                import toml
                config = toml.load(version_file)
                return config.get("project", {}).get("version", "unknown")
        except Exception as e:
            logger.debug(f"Failed to get version: {e}")

        return "unknown"

    @handle_errors
    def build_from_github(
        self,
        repo_url: str,
        skill_name: Optional[str] = None,
        output_dir: Optional[Path] = None,
        **options
    ) -> SkillBuildResult:
        """
        从 GitHub 仓库构建技能

        Args:
            repo_url: GitHub 仓库 URL
            skill_name: 技能名称,默认从仓库名提取
            output_dir: 输出目录
            **options: 其他选项 (enhance_with_ai, include_issues, etc.)

        Returns:
            SkillBuildResult: 构建结果
        """
        start_time = datetime.now()

        logger.info(f"Building skill from GitHub: {repo_url}")

        # 提取技能名称
        if skill_name is None:
            skill_name = repo_url.rstrip("/").split("/")[-1]

        # 设置输出目录
        if output_dir is None:
            workspace_root = Path(__file__).parent.parent
            output_dir = workspace_root / "skills" / "auto_generated"

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # 准备配置
        config = {
            "name": skill_name,
            "description": f"Auto-generated skill from {repo_url}",
            "sources": [
                {
                    "type": "github",
                    "url": repo_url,
                    **options
                }
            ]
        }

        # 调用 Skill Seekers 构建
        try:
            result = self._call_unified_builder(config)

            # 移动输出到目标目录
            skill_output = self.skill_seekers_path / "output" / skill_name
            if skill_output.exists():
                import shutil
                target_dir = output_dir / skill_name
                if target_dir.exists():
                    shutil.rmtree(target_dir)
                shutil.move(str(skill_output), str(target_dir))

                build_time = (datetime.now() - start_time).total_seconds()

                return SkillBuildResult(
                    success=True,
                    output_path=target_dir,
                    build_time=build_time,
                    metadata={
                        "source": "github",
                        "repo_url": repo_url,
                        "config": config
                    }
                )
            else:
                return SkillBuildResult(
                    success=False,
                    error="Build completed but output not found",
                    build_time=(datetime.now() - start_time).total_seconds()
                )

        except Exception as e:
            logger.error(f"Build failed: {e}")
            return SkillBuildResult(
                success=False,
                error=str(e),
                build_time=(datetime.now() - start_time).total_seconds()
            )

    @handle_errors
    def build_from_docs(
        self,
        docs_url: str,
        skill_name: Optional[str] = None,
        output_dir: Optional[Path] = None,
        **options
    ) -> SkillBuildResult:
        """从文档网站构建技能"""
        start_time = datetime.now()

        logger.info(f"Building skill from documentation: {docs_url}")

        if skill_name is None:
            from urllib.parse import urlparse
            skill_name = urlparse(docs_url).netloc.replace(".", "-")

        if output_dir is None:
            workspace_root = Path(__file__).parent.parent
            output_dir = workspace_root / "skills" / "auto_generated"

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # 配置
        config = {
            "name": skill_name,
            "description": f"Auto-generated skill from {docs_url}",
            "sources": [
                {
                    "type": "docs",
                    "url": docs_url,
                    **options
                }
            ]
        }

        try:
            result = self._call_unified_builder(config)

            skill_output = self.skill_seekers_path / "output" / skill_name
            if skill_output.exists():
                import shutil
                target_dir = output_dir / skill_name
                if target_dir.exists():
                    shutil.rmtree(target_dir)
                shutil.move(str(skill_output), str(target_dir))

                build_time = (datetime.now() - start_time).total_seconds()

                return SkillBuildResult(
                    success=True,
                    output_path=target_dir,
                    build_time=build_time,
                    metadata={
                        "source": "docs",
                        "docs_url": docs_url,
                        "config": config
                    }
                )

        except Exception as e:
            logger.error(f"Build failed: {e}")
            return SkillBuildResult(
                success=False,
                error=str(e),
                build_time=(datetime.now() - start_time).total_seconds()
            )

    @handle_errors
    def build_multi_source(
        self,
        sources: List[Source],
        skill_name: str,
        output_dir: Optional[Path] = None,
        **options
    ) -> SkillBuildResult:
        """多源组合构建"""
        start_time = datetime.now()

        logger.info(f"Building skill from {len(sources)} sources")

        if output_dir is None:
            workspace_root = Path(__file__).parent.parent
            output_dir = workspace_root / "skills" / "auto_generated"

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # 配置
        config = {
            "name": skill_name,
            "description": f"Auto-generated skill from {len(sources)} sources",
            "sources": [s.to_dict() for s in sources],
            **options
        }

        try:
            result = self._call_unified_builder(config)

            skill_output = self.skill_seekers_path / "output" / skill_name
            if skill_output.exists():
                import shutil
                target_dir = output_dir / skill_name
                if target_dir.exists():
                    shutil.rmtree(target_dir)
                shutil.move(str(skill_output), str(target_dir))

                build_time = (datetime.now() - start_time).total_seconds()

                return SkillBuildResult(
                    success=True,
                    output_path=target_dir,
                    build_time=build_time,
                    metadata={
                        "source": "multi",
                        "source_count": len(sources),
                        "config": config
                    }
                )

        except Exception as e:
            logger.error(f"Build failed: {e}")
            return SkillBuildResult(
                success=False,
                error=str(e),
                build_time=(datetime.now() - start_time).total_seconds()
            )

    def _call_unified_builder(self, config: Dict) -> Dict:
        """调用 Skill Seekers 的统一构建器"""
        # 写入临时配置文件
        import tempfile
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".json",
            delete=False
        ) as f:
            json.dump(config, f, indent=2)
            config_file = f.name

        try:
            # 调用构建脚本
            cli_dir = self.skill_seekers_path / "src" / "skill_seekers" / "cli"
            build_script = cli_dir / "unified_skill_builder.py"

            result = subprocess.run(
                [sys.executable, str(build_script), config_file],
                cwd=self.skill_seekers_path,
                capture_output=True,
                text=True,
                timeout=600  # 10分钟超时
            )

            if result.returncode != 0:
                raise RuntimeError(f"Build failed: {result.stderr}")

            return {"stdout": result.stdout, "stderr": result.stderr}

        finally:
            # 清理临时文件
            try:
                Path(config_file).unlink()
            except:
                pass

    def package_skill(
        self,
        skill_dir: Path,
        output_dir: Optional[Path] = None,
        target: str = "claude"
    ) -> Tuple[bool, Optional[Path]]:
        """
        打包技能为可分发格式

        Args:
            skill_dir: 技能目录
            output_dir: 输出目录
            target: 目标平台 ("claude", "gemini", "openai", "markdown")

        Returns:
            Tuple[成功标志, 包路径]
        """
        logger.info(f"Packaging skill: {skill_dir}")

        if output_dir is None:
            output_dir = skill_dir.parent

        # 调用打包脚本
        cli_dir = self.skill_seekers_path / "src" / "skill_seekers" / "cli"
        package_script = cli_dir / "package_skill.py"

        result = subprocess.run(
            [
                sys.executable,
                str(package_script),
                str(skill_dir),
                "--target", target,
                "--no-open"
            ],
            cwd=self.skill_seekers_path,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            # 查找生成的包文件
            if target == "claude":
                package_file = skill_dir.parent / f"{skill_dir.name}.zip"
            elif target == "gemini":
                package_file = skill_dir.parent / f"{skill_dir.name}-gemini.tar.gz"
            else:
                package_file = skill_dir.parent / f"{skill_dir.name}.zip"

            if package_file.exists():
                return True, package_file

        return False, None


# 导出
__all__ = [
    "SkillSeekersAdapter",
    "Source",
    "SkillBuildResult",
    "SkillSeekersAdapterError"
]


if __name__ == "__main__":
    # 测试代码
    adapter = SkillSeekersAdapter()

    # 测试 GitHub 构建
    result = adapter.build_from_github(
        repo_url="https://github.com/fastapi/fastapi",
        skill_name="fastapi-test"
    )

    print(f"Success: {result.success}")
    print(f"Output: {result.output_path}")
    print(f"Error: {result.error}")
