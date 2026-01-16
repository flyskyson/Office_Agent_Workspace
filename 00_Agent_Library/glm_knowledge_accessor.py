#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GLM 模型知识库访问器
为 GLM-4.7 模型提供快速访问自身知识库的接口
"""

import sys
import codecs
from pathlib import Path

# Windows 终端编码修复
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# 工作区配置
WORKSPACE_ROOT = Path(r"c:\Users\flyskyson\Office_Agent_Workspace")
KNOWLEDGE_FILE = WORKSPACE_ROOT / "06_Learning_Journal" / "zhipu_glm_knowledge" / "SKILL.md"


class GLMKnowledgeAccessor:
    """GLM 模型知识库访问器"""

    def __init__(self):
        self.knowledge_file = KNOWLEDGE_FILE
        self._cache = None

    def get_full_knowledge(self) -> str:
        """获取完整知识库"""
        if self._cache is None:
            with open(self.knowledge_file, 'r', encoding='utf-8') as f:
                self._cache = f.read()
        return self._cache

    def get_section(self, section_name: str) -> str:
        """获取特定章节"""
        content = self.get_full_knowledge()
        lines = content.split('\n')

        in_section = False
        section_content = []

        for line in lines:
            if line.startswith(f"## {section_name}"):
                in_section = True
                continue
            elif in_section and line.startswith("## "):
                break
            elif in_section:
                section_content.append(line)

        return '\n'.join(section_content).strip()

    def get_quick_reference(self) -> str:
        """获取快速参考"""
        sections = [
            self.get_section("🚀 核心功能"),
            self.get_section("🤖 可用模型"),
            self.get_section("💡 最佳实践")
        ]
        return '\n\n'.join(sections)

    def display_summary(self):
        """显示知识库摘要"""
        print("=" * 70)
        print("📚 GLM-4.7 模型知识库")
        print("=" * 70)
        print(f"📍 位置: {self.knowledge_file}")
        print(f"📄 大小: {self.knowledge_file.stat().st_size / 1024:.2f} KB")
        print()
        print("✅ 知识库已创建并就绪")
        print("=" * 70)


def main():
    """主函数"""
    accessor = GLMKnowledgeAccessor()
    accessor.display_summary()
    return 0


if __name__ == "__main__":
    sys.exit(main())
