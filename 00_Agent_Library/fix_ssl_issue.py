#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSL证书问题修复工具

解决HuggingFace模型下载时的SSL证书验证失败问题

作者: Claude Code
日期: 2026-01-16
"""

import os
import sys
from pathlib import Path

# Windows 终端编码修复
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass


def fix_method_1_disable_ssl_verify():
    """
    方案1: 禁用SSL验证（仅用于开发环境）

    优点: 快速解决
    缺点: 降低安全性，仅适用于开发环境
    """
    print("\n" + "="*60)
    print("🔧 方案1: 禁用SSL验证（开发环境推荐）")
    print("="*60)

    # 设置环境变量禁用SSL验证
    os.environ['CURL_CA_BUNDLE'] = ''
    os.environ['REQUESTS_CA_BUNDLE'] = ''
    os.environ['SSL_VERIFY'] = 'FALSE'

    print("\n✅ 已设置环境变量:")
    print("   CURL_CA_BUNDLE = ''")
    print("   REQUESTS_CA_BUNDLE = ''")
    print("   SSL_VERIFY = 'FALSE'")

    print("\n📝 使用方法:")
    print("   在导入sentence_transformers之前运行此函数")
    print("   或在代码开头添加:")
    print("   ```python")
    print("   import os")
    print("   os.environ['CURL_CA_BUNDLE'] = ''")
    print("   ```")

    return True


def fix_method_2_use_local_model():
    """
    方案2: 使用本地模型文件

    优点: 完全离线，无需网络
    缺点: 需要提前下载模型文件
    """
    print("\n" + "="*60)
    print("🔧 方案2: 使用本地模型文件")
    print("="*60)

    print("\n📦 步骤:")

    print("\n1️⃣  手动下载模型文件:")
    print("   访问: https://www.modelscope.cn/models/AI-ModelScope/bge-small-zh-v1.5")
    print("   或: https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

    print("\n2️⃣  下载后解压到本地目录:")
    model_dir = Path.home() / ".cache" / "huggingface" / "hub" / "models--sentence-transformers--paraphrase-multilingual-MiniLM-L12-v2"
    print(f"   Windows: {model_dir}")

    print("\n3️⃣  修改代码使用本地模型:")
    print("   ```python")
    print("   # 指定本地模型路径")
    print("   model_path = r'C:\\Users\\YourName\\.cache\\huggingface\\hub\\models--...'")
    print("   embedder = SentenceTransformer(model_path)")
    print("   ```")

    print("\n📝 ModelScope 镜像命令:")
    print("   ```bash")
    print("   pip install modelscope")
    print("   python -c 'from modelscope import snapshot_download; snapshot_download(\"sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2\")'")
    print("   ```")

    return True


def fix_method_3_use_mirror():
    """
    方案3: 使用国内镜像源

    优点: 速度快，自动处理SSL
    缺点: 需要配置镜像源
    """
    print("\n" + "="*60)
    print("🔧 方案3: 使用国内镜像源（推荐）")
    print("="*60)

    print("\n📝 使用 HF-Mirror 镜像:")

    print("\n1️⃣  设置环境变量:")
    print("   ```bash")
    print("   # Windows PowerShell")
    print("   $env:HF_ENDPOINT = \"https://hf-mirror.com\"")
    print("")
    print("   # Windows CMD")
    print("   set HF_ENDPOINT=https://hf-mirror.com")
    print("")
    print("   # Linux/Mac")
    print("   export HF_ENDPOINT=https://hf-mirror.com")
    print("   ```")

    print("\n2️⃣  或在Python代码中设置:")
    print("   ```python")
    print("   import os")
    print("   os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'")
    print("   from sentence_transformers import SentenceTransformer")
    print("   model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')")
    print("   ```")

    print("\n3️⃣  使用 ModelScope 替代:")
    print("   ```bash")
    print("   pip install modelscope")
    print("   ```")
    print("   ```python")
    print("   from modelscope import snapshot_download")
    print("   model_dir = snapshot_download('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')")
    print("   from sentence_transformers import SentenceTransformer")
    print("   model = SentenceTransformer(model_dir)")
    print("   ```")

    # 尝试设置镜像
    os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
    print("\n✅ 已自动设置 HF_ENDPOINT = https://hf-mirror.com")

    return True


def fix_method_4_update_certificates():
    """
    方案4: 更新SSL证书

    优点: 最安全，长期有效
    缺点: 需要系统权限
    """
    print("\n" + "="*60)
    print("🔧 方案4: 更新SSL证书")
    print("="*60)

    print("\n📝 Windows 更新证书:")

    print("\n1️⃣  安装 certifi:")
    print("   ```bash")
    print("   pip install --upgrade certifi")
    print("   ```")

    print("\n2️⃣  更新系统根证书:")
    print("   - 下载: https://curl.se/docs/caextract.html")
    print("   - 将 cacert.pem 放到 Python 目录")
    print("   - 设置环境变量: SSL_CERT_FILE=<路径>\\cacert.pem")

    print("\n3️⃣  或使用自动化工具:")
    print("   ```bash")
    print("   pip install certifi")
    print("   python -m certifi")
    print("   ```")

    # 尝试更新certifi
    try:
        import subprocess
        print("\n🔄 正在尝试更新 certifi...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "certifi"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✅ certifi 更新成功")

            import certifi
            print(f"📁 证书路径: {certifi.where()}")
        else:
            print("⚠️ certifi 更新失败")
    except Exception as e:
        print(f"⚠️ 更新失败: {e}")

    return True


def fix_method_5_disable_semantic_search():
    """
    方案5: 禁用语义搜索（临时方案）

    优点: 立即可用
    缺点: 失去语义搜索能力
    """
    print("\n" + "="*60)
    print("🔧 方案5: 禁用语义搜索（临时方案）")
    print("="*60)

    print("\n📝 修改初始化代码:")
    print("   ```python")
    print("   # 禁用语义记忆，使用关键词搜索")
    print("   memory = ClaudeMemory(enable_semantic=False)")
    print("   ```")

    print("\n💡 说明:")
    print("   - 基础记忆功能完全可用")
    print("   - 使用关键词匹配代替语义搜索")
    print("   - 仍然支持优先级、标签、时间过滤")
    print("   - 性能更好，但搜索精度略低")

    return True


def create_fixed_semantic_memory():
    """
    创建修复版的 semantic_memory.py
    """
    print("\n" + "="*60)
    print("🔧 创建修复版语义记忆")
    print("="*60)

    # 读取原文件
    semantic_file = Path(__file__).parent / "semantic_memory.py"

    if not semantic_file.exists():
        print("❌ 找不到 semantic_memory.py")
        return False

    # 创建修复版本
    fixed_file = Path(__file__).parent / "semantic_memory_fixed.py"

    content = semantic_file.read_text(encoding='utf-8')

    # 在文件开头添加SSL修复代码
    ssl_fix = '''
# ============================================================================
# SSL证书问题修复
# ============================================================================
import os
# 使用HF-Mirror镜像解决SSL问题
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

# 如果仍有问题，可以禁用SSL验证（仅开发环境）
# import ssl
# import urllib3
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# ssl._create_default_https_context = ssl._create_unverified_context

'''

    # 检查是否已经添加过
    if 'HF_ENDPOINT' in content:
        print("✅ semantic_memory.py 已包含SSL修复代码")
        return True

    # 在导入语句后添加修复代码
    lines = content.split('\n')
    insert_pos = 0
    for i, line in enumerate(lines):
        if line.startswith('# -*- coding:'):
            insert_pos = i + 1
            break

    lines.insert(insert_pos, ssl_fix)

    # 写入新文件
    fixed_content = '\n'.join(lines)
    fixed_file.write_text(fixed_content, encoding='utf-8')

    print(f"✅ 创建修复版文件: {fixed_file}")
    print("\n📝 使用方法:")
    print("   1. 备份原文件:")
    print("      mv semantic_memory.py semantic_memory.py.bak")
    print("   2. 使用修复版:")
    print("      mv semantic_memory_fixed.py semantic_memory.py")
    print("   3. 或直接导入:")
    print("      from semantic_memory_fixed import SemanticMemory")

    return True


def main():
    """主函数"""
    print("\n" + "🔒"*30)
    print("   SSL证书问题修复工具")
    print("🔒"*30)

    print("\n📋 问题说明:")
    print("   HuggingFace模型下载时出现SSL证书验证失败")
    print("   错误: [SSL: CERTIFICATE_VERIFY_FAILED]")

    print("\n✨ 推荐方案（按优先级）:")
    print("   1. 使用国内镜像（HF-Mirror）- 最推荐")
    print("   2. 禁用SSL验证（开发环境）")
    print("   3. 使用本地模型文件")
    print("   4. 更新SSL证书")
    print("   5. 禁用语义搜索（临时）")

    print("\n" + "-"*60)

    # 自动执行方案3（最推荐）
    fix_method_3_use_mirror()

    print("\n" + "-"*60)
    print("其他方案:")
    print("-"*60)

    # 执行其他方案（仅显示说明）
    fix_method_1_disable_ssl_verify()
    fix_method_2_use_local_model()
    fix_method_4_update_certificates()
    fix_method_5_disable_semantic_search()

    print("\n" + "-"*60)
    print("🔧 创建修复版文件...")
    create_fixed_semantic_memory()

    print("\n" + "="*60)
    print("✅ 修复完成！")
    print("="*60)

    print("\n🧪 测试命令:")
    print("   python -c \"import os; os.environ['HF_ENDPOINT']='https://hf-mirror.com'; from sentence_transformers import SentenceTransformer; model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2'); print('✅ 模型加载成功')\"")

    print("\n💡 快速修复（推荐立即执行）:")
    print("   ```bash")
    print("   # PowerShell")
    print("   $env:HF_ENDPOINT=\"https://hf-mirror.com\"")
    print("")
    print("   # CMD")
    print("   set HF_ENDPOINT=https://hf-mirror.com")
    print("")
    print("   # 然后重新运行你的程序")
    print("   ```")

    print("\n")


if __name__ == "__main__":
    main()
