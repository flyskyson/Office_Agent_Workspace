#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
向量语义搜索系统 - 一键安装脚本

自动安装必要的依赖并验证安装。

作者: Claude Code
日期: 2026-01-16
"""

import sys
import subprocess
from pathlib import Path

# Windows 终端编码修复
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass


def print_header(text):
    """打印标题"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def install_package(package_name, import_name=None):
    """安装Python包"""
    if import_name is None:
        import_name = package_name

    # 检查是否已安装
    try:
        __import__(import_name)
        print(f"✅ {package_name} 已安装")
        return True
    except ImportError:
        pass

    # 安装包
    print(f"📦 正在安装 {package_name}...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", package_name
        ])
        print(f"✅ {package_name} 安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {package_name} 安装失败: {e}")
        return False


def verify_installation():
    """验证安装"""
    print_header("验证安装")

    try:
        import chromadb
        print("✅ chromadb 已安装")

        from sentence_transformers import SentenceTransformer
        print("✅ sentence-transformers 已安装")

        # 测试基本功能
        print("\n🔄 测试语义记忆系统...")
        from semantic_memory import SemanticMemory

        semantic = SemanticMemory()
        print("✅ 语义记忆系统初始化成功")

        # 测试添加和搜索
        semantic.add_memory(
            memory_id="test_install",
            text="安装测试：向量语义搜索系统",
            metadata={"type": "test"}
        )

        results = semantic.search("测试", top_k=1)
        if len(results) > 0:
            print("✅ 搜索功能正常")
        else:
            print("⚠️ 搜索未返回结果")

        return True

    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def main():
    """主函数"""
    print("""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║        向量语义搜索系统 - 一键安装 (v2.0)                          ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
    """)

    print_header("开始安装")

    # 安装依赖
    packages = [
        ("chromadb", "chromadb"),
        ("sentence-transformers", "sentence_transformers"),
    ]

    results = {}
    for package, import_name in packages:
        results[package] = install_package(package, import_name)

    # 检查结果
    print_header("安装结果")

    all_success = all(results.values())
    for package, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {package}")

    if all_success:
        print("\n🎉 所有依赖安装成功！")

        # 验证安装
        if verify_installation():
            print_header("安装完成")
            print("\n📚 下一步:")
            print("   1. 运行测试: python 00_Agent_Library/test_semantic_memory.py")
            print("   2. 查看文档: docs/guides/SEMANTIC_MEMORY_GUIDE.md")
            print("   3. 开始使用: from semantic_memory import SemanticMemory")
            print("\n" + "=" * 70)
            return 0
        else:
            print("\n⚠️ 安装验证失败，请检查错误信息")
            return 1
    else:
        print("\n❌ 部分依赖安装失败，请手动安装:")
        for package, success in results.items():
            if not success:
                print(f"   pip install {package}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
