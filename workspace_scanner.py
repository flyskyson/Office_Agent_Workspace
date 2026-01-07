#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工作区全貌扫描工具 - 智能管家的"眼睛"
深度扫描工作区，记录每一个文件、项目、工具的详细信息
为AI助手提供完整的工作区记忆
"""

import os
import json
from datetime import datetime
from pathlib import Path
import hashlib


class WorkspaceScanner:
    """工作区全貌扫描器"""

    def __init__(self, workspace_root=None):
        """初始化扫描器

        Args:
            workspace_root: 工作区根目录
        """
        if workspace_root is None:
            workspace_root = Path(__file__).parent
        else:
            workspace_root = Path(workspace_root)

        self.workspace_root = workspace_root
        self.memory_dir = workspace_root / "06_Learning_Journal" / "workspace_memory"
        self.memory_dir.mkdir(exist_ok=True)

        # 需要忽略的目录
        self.ignore_dirs = {
            'venv', '.venv', '__pycache__', 'node_modules',
            '.git', '.vscode', '.claude', 'dist', 'build',
            'pytest_cache', '.mypy_cache'
        }

        # 需要深度扫描的目录
        self.deep_scan_dirs = {
            '00_Agent_Library', '01_Active_Projects',
            '03_Code_Templates', '06_Learning_Journal'
        }

    def calculate_file_hash(self, filepath):
        """计算文件的MD5哈希值（用于版本检测）"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()[:8]
        except:
            return None

    def scan_file(self, filepath):
        """扫描单个文件

        Args:
            filepath: 文件路径

        Returns:
            dict: 文件信息
        """
        try:
            stat = filepath.stat()
            file_info = {
                'path': str(filepath.relative_to(self.workspace_root)),
                'name': filepath.name,
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                'extension': filepath.suffix,
                'type': self._get_file_type(filepath)
            }

            # 对代码文件计算哈希值
            if filepath.suffix in ['.py', '.js', '.bat', '.ps1', '.md']:
                file_info['hash'] = self.calculate_file_hash(filepath)

            return file_info
        except Exception as e:
            return {
                'path': str(filepath.relative_to(self.workspace_root)),
                'error': str(e)
            }

    def _get_file_type(self, filepath):
        """获取文件类型分类"""
        suffix = filepath.suffix.lower()

        if suffix in ['.py']:
            return 'Python脚本'
        elif suffix in ['.js', '.ts']:
            return 'JavaScript/TypeScript'
        elif suffix in ['.bat', '.ps1']:
            return '脚本工具'
        elif suffix in ['.md']:
            return 'Markdown文档'
        elif suffix in ['.txt']:
            return '文本文件'
        elif suffix in ['.json']:
            return 'JSON配置'
        elif suffix in ['.csv', '.xlsx', '.xls']:
            return '数据文件'
        else:
            return '其他文件'

    def scan_directory(self, directory, deep=False):
        """扫描目录

        Args:
            directory: 目录路径
            deep: 是否深度扫描

        Returns:
            dict: 目录扫描结果
        """
        result = {
            'path': str(directory.relative_to(self.workspace_root)),
            'type': 'directory',
            'files': [],
            'subdirs': []
        }

        try:
            for item in directory.iterdir():
                # 跳过隐藏文件和忽略目录
                if item.name.startswith('.') or item.name in self.ignore_dirs:
                    continue

                if item.is_dir():
                    # 判断是否需要深度扫描
                    should_deep_scan = deep or item.name in self.deep_scan_dirs
                    subdir_result = self.scan_directory(item, deep=should_deep_scan)
                    result['subdirs'].append(subdir_result)
                else:
                    file_info = self.scan_file(item)
                    result['files'].append(file_info)

        except PermissionError:
            result['error'] = 'Permission denied'

        return result

    def analyze_projects(self):
        """分析所有项目

        Returns:
            list: 项目信息列表
        """
        projects_dir = self.workspace_root / "01_Active_Projects"
        archive_dir = self.workspace_root / "02_Project_Archive"

        projects = []

        # 扫描活跃项目
        if projects_dir.exists():
            for project_dir in projects_dir.iterdir():
                if project_dir.is_dir() and not project_dir.name.startswith('.'):
                    project_info = self._analyze_project(project_dir, 'active')
                    if project_info:
                        projects.append(project_info)

        # 扫描归档项目
        if archive_dir.exists():
            for project_dir in archive_dir.iterdir():
                if project_dir.is_dir() and not project_dir.name.startswith('.'):
                    project_info = self._analyze_project(project_dir, 'archived')
                    if project_info:
                        projects.append(project_info)

        return projects

    def _analyze_project(self, project_dir, status):
        """分析单个项目

        Args:
            project_dir: 项目目录
            status: 项目状态 (active/archived)

        Returns:
            dict: 项目信息
        """
        try:
            # 查找README
            readme_file = None
            for name in ['README.md', 'readme.md', 'README.txt']:
                potential_readme = project_dir / name
                if potential_readme.exists():
                    readme_file = potential_readme
                    break

            # 扫描项目文件
            py_files = list(project_dir.rglob('*.py'))
            js_files = list(project_dir.rglob('*.js'))
            md_files = list(project_dir.rglob('*.md'))

            # 获取主要Python脚本
            main_scripts = []
            for py_file in py_files:
                if not any(ignored in str(py_file) for ignored in ['venv', '__pycache__']):
                    file_info = self.scan_file(py_file)
                    main_scripts.append(file_info)

            project_info = {
                'name': project_dir.name,
                'status': status,
                'path': str(project_dir.relative_to(self.workspace_root)),
                'has_readme': readme_file is not None,
                'readme_path': str(readme_file.relative_to(self.workspace_root)) if readme_file else None,
                'py_files_count': len(py_files),
                'js_files_count': len(js_files),
                'doc_files_count': len(md_files),
                'main_scripts': main_scripts[:5],  # 最多5个主要脚本
                'last_modified': datetime.fromtimestamp(
                    project_dir.stat().st_mtime
                ).strftime('%Y-%m-%d %H:%M:%S')
            }

            return project_info

        except Exception as e:
            print(f"分析项目 {project_dir.name} 时出错: {e}")
            return None

    def analyze_code_library(self):
        """分析代码库

        Returns:
            dict: 代码库信息
        """
        library_dir = self.workspace_root / "00_Agent_Library"

        if not library_dir.exists():
            return {}

        library_info = {
            'snippets': {},
            'prompts': {},
            'templates': {},
            'tools': {}
        }

        # 扫描代码片段
        snippets_dir = library_dir / "02_Code_Snippets"
        if snippets_dir.exists():
            for category_dir in snippets_dir.iterdir():
                if category_dir.is_dir():
                    snippets = []
                    for snippet_file in category_dir.glob('*.py'):
                        snippets.append({
                            'name': snippet_file.stem,
                            'path': str(snippet_file.relative_to(self.workspace_root)),
                            'category': category_dir.name
                        })
                    library_info['snippets'][category_dir.name] = snippets

        # 扫描Prompt库
        prompts_dir = library_dir / "01_Prompt_Library"
        if prompts_dir.exists():
            for category_dir in prompts_dir.iterdir():
                if category_dir.is_dir():
                    prompts = []
                    for prompt_file in category_dir.glob('*.md'):
                        prompts.append({
                            'name': prompt_file.stem,
                            'path': str(prompt_file.relative_to(self.workspace_root))
                        })
                    library_info['prompts'][category_dir.name] = prompts

        return library_info

    def analyze_tools(self):
        """分析工作区工具

        Returns:
            list: 工具列表
        """
        tools = []

        # 扫描根目录的工具脚本
        for pattern in ['*.py', '*.bat', '*.ps1']:
            for tool_file in self.workspace_root.glob(pattern):
                if tool_file.name.startswith('workspace_') or \
                   tool_file.name.startswith('check_') or \
                   tool_file.name.startswith('setup_') or \
                   tool_file.name.startswith('run_') or \
                   tool_file.name.startswith('create_') or \
                   tool_file.name.startswith('generate_') or \
                   tool_file.name == 'start_new_session.bat':
                    tool_info = self.scan_file(tool_file)
                    tool_info['description'] = self._get_tool_description(tool_file.name)
                    tools.append(tool_info)

        # 扫描Agent_Library中的工具
        tools_dir = self.workspace_root / "00_Agent_Library" / "99_Scripts_Tools"
        if tools_dir.exists():
            for tool_file in tools_dir.glob('*.*'):
                tool_info = self.scan_file(tool_file)
                tools.append(tool_info)

        return tools

    def _get_tool_description(self, tool_name):
        """获取工具描述"""
        descriptions = {
            'workspace_report.py': '生成工作区健康报告，分析项目状态、缓存文件等',
            'workspace_cleaner.py': '清理工作区，删除Python缓存、临时文件',
            'workspace_maintenance.py': '定期维护脚本，检查磁盘空间、大文件等',
            'start_new_session.bat': '一键启动菜单，快速访问工作区功能',
            'project_planner.py': '项目规划助手，基于技能水平推荐项目',
            'learning_logger.py': '学习日志工具，记录学习内容和问题',
            'workspace_scanner.py': '工作区扫描器，建立完整工作区索引'
        }
        return descriptions.get(tool_name, '工作区工具')

    def generate_memory_index(self):
        """生成工作区记忆索引

        Returns:
            dict: 完整的记忆索引
        """
        print("正在扫描工作区...")

        memory_index = {
            'scan_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'workspace_root': str(self.workspace_root),
            'projects': self.analyze_projects(),
            'code_library': self.analyze_code_library(),
            'tools': self.analyze_tools(),
            'statistics': {}
        }

        # 统计信息
        active_projects = [p for p in memory_index['projects'] if p['status'] == 'active']
        archived_projects = [p for p in memory_index['projects'] if p['status'] == 'archived']

        memory_index['statistics'] = {
            'total_projects': len(memory_index['projects']),
            'active_projects': len(active_projects),
            'archived_projects': len(archived_projects),
            'total_tools': len(memory_index['tools']),
            'code_snippets': sum(len(v) for v in memory_index['code_library'].get('snippets', {}).values()),
            'prompt_templates': sum(len(v) for v in memory_index['code_library'].get('prompts', {}).values())
        }

        return memory_index

    def save_memory_index(self, memory_index):
        """保存记忆索引到文件

        Args:
            memory_index: 记忆索引数据
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        json_file = self.memory_dir / f"workspace_index_{timestamp}.json"
        markdown_file = self.memory_dir / f"workspace_index_{timestamp}.md"

        # 保存JSON格式（机器可读）
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(memory_index, f, ensure_ascii=False, indent=2)

        # 保存Markdown格式（人类可读）
        self._save_markdown_index(memory_index, markdown_file)

        # 保存最新的索引
        latest_json = self.memory_dir / "workspace_index_latest.json"
        latest_md = self.memory_dir / "workspace_index_latest.md"

        with open(latest_json, 'w', encoding='utf-8') as f:
            json.dump(memory_index, f, ensure_ascii=False, indent=2)

        self._save_markdown_index(memory_index, latest_md)

        print(f"\n[OK] 记忆索引已保存:")
        print(f"  - JSON格式: {json_file}")
        print(f"  - Markdown格式: {markdown_file}")
        print(f"  - 最新索引: {latest_json} 和 {latest_md}")

        return json_file, markdown_file

    def _save_markdown_index(self, memory_index, filepath):
        """保存Markdown格式的索引"""
        content = f"""# 工作区记忆索引

**扫描时间**: {memory_index['scan_time']}
**工作区路径**: {memory_index['workspace_root']}

---

## 📊 统计概览

| 项目类型 | 数量 |
|---------|------|
| 活跃项目 | {memory_index['statistics']['active_projects']} |
| 归档项目 | {memory_index['statistics']['archived_projects']} |
| 工具脚本 | {memory_index['statistics']['total_tools']} |
| 代码片段 | {memory_index['statistics']['code_snippets']} |
| Prompt模板 | {memory_index['statistics']['prompt_templates']} |

---

## 🚀 活跃项目

"""

        # 活跃项目
        active_projects = [p for p in memory_index['projects'] if p['status'] == 'active']
        for project in active_projects:
            content += f"""
### {project['name']}

- **路径**: `{project['path']}`
- **最后修改**: {project['last_modified']}
- **Python文件**: {project['py_files_count']} 个
- **文档文件**: {project['doc_files_count']} 个
- **有README**: {'✅' if project['has_readme'] else '❌'}
- **README路径**: `{project['readme_path']}` if project['has_readme'] else '无'

**主要脚本**:
"""
            for script in project['main_scripts']:
                content += f"- `{script['name']}` ({script['type']})\n"

            content += "\n"

        # 归档项目
        content += "\n## 📦 归档项目\n\n"
        archived_projects = [p for p in memory_index['projects'] if p['status'] == 'archived']
        for project in archived_projects:
            content += f"- **{project['name']}** - {project['last_modified']}\n"

        # 工具脚本
        content += "\n\n## 🛠️ 工具脚本\n\n"
        for tool in memory_index['tools']:
            content += f"- **{tool['name']}**\n"
            content += f"  - 路径: `{tool['path']}`\n"
            if 'description' in tool:
                content += f"  - 说明: {tool['description']}\n"
            content += f"  - 大小: {tool['size']} bytes\n"
            content += f"  - 修改时间: {tool['modified']}\n\n"

        # 代码库
        code_lib = memory_index.get('code_library', {})

        content += "\n## 📚 代码片段库\n\n"
        for category, snippets in code_lib.get('snippets', {}).items():
            content += f"### {category}\n\n"
            for snippet in snippets:
                content += f"- `{snippet['name']}` - `{snippet['path']}`\n"

        content += "\n## 💬 Prompt模板库\n\n"
        for category, prompts in code_lib.get('prompts', {}).items():
            content += f"### {category}\n\n"
            for prompt in prompts:
                content += f"- `{prompt['name']}` - `{prompt['path']}`\n"

        content += "\n---\n\n"
        content += "**注意**: 此索引由 `workspace_scanner.py` 自动生成\n"

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)


def main():
    """主程序"""
    import sys
    import io

    # 设置UTF-8编码输出
    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print("="*70)
    print("工作区全貌扫描工具 - 智能管家系统")
    print("="*70)

    scanner = WorkspaceScanner()

    # 生成记忆索引
    memory_index = scanner.generate_memory_index()

    # 显示统计信息
    stats = memory_index['statistics']
    print("\n扫描完成!")
    print(f"\n统计信息:")
    print(f"  活跃项目: {stats['active_projects']} 个")
    print(f"  归档项目: {stats['archived_projects']} 个")
    print(f"  工具脚本: {stats['total_tools']} 个")
    print(f"  代码片段: {stats['code_snippets']} 个")
    print(f"  Prompt模板: {stats['prompt_templates']} 个")

    # 保存索引
    scanner.save_memory_index(memory_index)

    print("\n" + "="*70)
    print("工作区记忆索引已建立!")
    print("AI助手现在可以全面了解工作区的状态了。")
    print("="*70)


if __name__ == "__main__":
    main()
