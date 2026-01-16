#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主动建议系统 (Proactive Advisor)

让Claude能够主动提醒、及时建议、预见问题

用户期望:
- ✅ 做得不对时及时提醒
- ✅ 应该做的时候主动建议
- ✅ 不等询问，主动发言

作者: Claude Code
日期: 2026-01-16
版本: v1.0.0
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict

# Windows 终端编码修复
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    except:
        pass


class ProactiveAdvisor:
    """
    主动建议系统

    功能:
    1. 代码审查 - 实时检查问题
    2. 最佳实践 - 建议改进方向
    3. 风险预警 - 提前发现潜在问题
    4. 优化建议 - 主动提供优化方案
    5. 知识提醒 - 提醒相关知识和经验
    """

    def __init__(self, workspace_root: Path):
        self.workspace_root = Path(workspace_root)
        self.learning_dir = self.workspace_root / "06_Learning_Journal" / "auto_learning"

        # 加载用户画像
        profile_file = self.learning_dir / "user_profile.json"
        if profile_file.exists():
            with open(profile_file, 'r', encoding='utf-8') as f:
                self.user_profile = json.load(f)
        else:
            self.user_profile = {}

        # 建议历史
        self.suggestion_history = []

        # 规则库
        self.rules = self._build_rules()

    def _build_rules(self) -> Dict[str, List[Dict]]:
        """构建建议规则库"""
        return {
            'code_quality': [
                {
                    'name': 'Windows兼容性',
                    'check': self._check_windows_compatibility,
                    'suggestion': '检测到可能存在Windows兼容性问题',
                    'action': '添加编码修复和路径处理',
                    'priority': 'high'
                },
                {
                    'name': '错误处理',
                    'check': self._check_error_handling,
                    'suggestion': '缺少异常处理',
                    'action': '添加 try-except 块',
                    'priority': 'medium'
                },
                {
                    'name': '文档注释',
                    'check': self._check_documentation,
                    'suggestion': '函数缺少文档字符串',
                    'action': '添加 docstring 说明功能和参数',
                    'priority': 'low'
                }
            ],
            'best_practices': [
                {
                    'name': '命名规范',
                    'check': self._check_naming,
                    'suggestion': '变量命名不符合PEP8规范',
                    'action': '使用 snake_case 命名',
                    'priority': 'medium'
                },
                {
                    'name': '代码复用',
                    'check': self._check_duplication,
                    'suggestion': '检测到重复代码',
                    'action': '提取为独立函数',
                    'priority': 'medium'
                },
                {
                    'name': '类型注解',
                    'check': self._check_type_hints,
                    'suggestion': '缺少类型注解',
                    'action': '添加类型提示提高可读性',
                    'priority': 'low'
                }
            ],
            'security': [
                {
                    'name': 'SQL注入',
                    'check': self._check_sql_injection,
                    'suggestion': '可能存在SQL注入风险',
                    'action': '使用参数化查询',
                    'priority': 'critical'
                },
                {
                    'name': '命令注入',
                    'check': self._check_command_injection,
                    'suggestion': '可能存在命令注入风险',
                    'action': '避免直接拼接用户输入到命令',
                    'priority': 'critical'
                },
                {
                    'name': '敏感信息',
                    'check': self._check_sensitive_data,
                    'suggestion': '检测到可能的敏感信息',
                    'action': '使用环境变量或配置文件',
                    'priority': 'high'
                }
            ],
            'performance': [
                {
                    'name': '循环优化',
                    'check': self._check_loop_efficiency,
                    'suggestion': '循环可以优化',
                    'action': '考虑使用列表推导或生成器',
                    'priority': 'low'
                },
                {
                    'name': '资源管理',
                    'check': self._check_resource_cleanup,
                    'suggestion': '资源未正确释放',
                    'action': '使用 with 语句或显式关闭',
                    'priority': 'medium'
                }
            ]
        }

    # ========================================================================
    # 检查方法
    # ========================================================================

    def _check_windows_compatibility(self, code: str, context: Dict) -> bool:
        """检查Windows兼容性"""
        # 检查是否缺少编码修复
        if 'import codecs' not in code and sys.platform in ['win32', 'cygwin']:
            if 'print(' in code or 'open(' in code:
                return True
        return False

    def _check_error_handling(self, code: str, context: Dict) -> bool:
        """检查错误处理"""
        # 检查文件操作是否缺少异常处理
        if 'open(' in code and 'try:' not in code:
            return True
        # 检查网络请求是否缺少异常处理
        if 'requests.' in code or 'urllib.' in code:
            if 'try:' not in code:
                return True
        return False

    def _check_documentation(self, code: str, context: Dict) -> bool:
        """检查文档注释"""
        # 检查是否有函数定义但缺少docstring
        if 'def ' in code:
            lines = code.split('\n')
            for i, line in enumerate(lines):
                if 'def ' in line and '"""' not in line and "'''" not in line:
                    # 检查下一行是否有docstring
                    if i + 1 < len(lines):
                        if '"""' not in lines[i + 1] and "'''" not in lines[i + 1]:
                            return True
        return False

    def _check_naming(self, code: str, context: Dict) -> bool:
        """检查命名规范"""
        # 简单检查：是否有CamelCase变量名（Python应该用snake_case）
        import re
        camel_case = re.findall(r'\b[a-z][a-zA-Z0-9]*[A-Z][a-z]+\b', code)
        # 排除类名（应该用PascalCase）
        for name in camel_case:
            if not name[0].isupper():  # 不是类名
                return True
        return False

    def _check_duplication(self, code: str, context: Dict) -> bool:
        """检查代码重复"""
        lines = code.split('\n')
        # 简单检查：是否有重复的行（忽略空行和注释）
        code_lines = [l.strip() for l in lines if l.strip() and not l.strip().startswith('#')]
        from collections import Counter
        counts = Counter(code_lines)
        for line, count in counts.items():
            if count >= 3 and len(line) > 20:  # 重复3次以上且长度>20
                return True
        return False

    def _check_type_hints(self, code: str, context: Dict) -> bool:
        """检查类型注解"""
        if 'def ' in code:
            # 检查是否有函数定义但缺少类型注解
            import re
            functions = re.findall(r'def\s+(\w+)\s*\((.*?)\):', code)
            for func_name, params in functions:
                if ' -> ' not in code[code.index(f'def {func_name}'):code.index(f'def {func_name}') + 200]:
                    return True
        return False

    def _check_sql_injection(self, code: str, context: Dict) -> bool:
        """检查SQL注入"""
        dangerous_patterns = [
            'SELECT * FROM',
            'DELETE FROM',
            'DROP TABLE',
            'INSERT INTO'
        ]
        for pattern in dangerous_patterns:
            if pattern in code and '%' in code:
                # 可能的字符串拼接SQL
                if 'execute(' in code or 'exec(' in code:
                    return True
        return False

    def _check_command_injection(self, code: str, context: Dict) -> bool:
        """检查命令注入"""
        if 'subprocess.' in code or 'os.system(' in code:
            # 检查是否直接拼接用户输入
            if 'shell=True' in code:
                return True
        return False

    def _check_sensitive_data(self, code: str, context: Dict) -> bool:
        """检查敏感信息"""
        sensitive_patterns = [
            'password',
            'api_key',
            'secret',
            'token',
            'credential'
        ]
        for pattern in sensitive_patterns:
            if f'{pattern} = "' in code or f'{pattern} = "' in code:
                # 硬编码的敏感信息
                return True
        return False

    def _check_loop_efficiency(self, code: str, context: Dict) -> bool:
        """检查循环效率"""
        # 检查是否有可以列表推导的循环
        if 'for ' in code and '.append(' in code:
            return True
        return False

    def _check_resource_cleanup(self, code: str, context: Dict) -> bool:
        """检查资源清理"""
        # 检查文件操作是否使用with语句
        if 'open(' in code and 'with open(' not in code:
            if '.close()' not in code:
                return True
        return False

    # ========================================================================
    # 主动建议
    # ========================================================================

    def analyze_code(self, code: str, file_path: str = None,
                     context: Dict = None) -> List[Dict[str, Any]]:
        """
        分析代码并提供建议

        返回:
            [
                {
                    'category': str,      # 类别
                    'name': str,         # 问题名称
                    'suggestion': str,   # 建议
                    'action': str,       # 行动
                    'priority': str,     # 优先级
                    'line': int          # 行号（如果可能）
                }
            ]
        """
        context = context or {}
        suggestions = []

        # 运行所有检查
        for category, rules in self.rules.items():
            for rule in rules:
                try:
                    if rule['check'](code, context):
                        suggestion = {
                            'category': category,
                            'name': rule['name'],
                            'suggestion': rule['suggestion'],
                            'action': rule['action'],
                            'priority': rule['priority'],
                            'file': file_path,
                            'timestamp': datetime.now().isoformat()
                        }
                        suggestions.append(suggestion)
                except Exception as e:
                    print(f"⚠️ 规则检查失败 ({rule['name']}): {e}")

        # 按优先级排序
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        suggestions.sort(key=lambda x: priority_order.get(x['priority'], 4))

        return suggestions

    def format_suggestions(self, suggestions: List[Dict]) -> str:
        """格式化建议输出"""
        if not suggestions:
            return "✅ 代码检查通过，没有发现问题！"

        output = ["\n🔍 代码审查建议:\n"]

        # 按优先级分组
        by_priority = defaultdict(list)
        for s in suggestions:
            by_priority[s['priority']].append(s)

        priority_order = ['critical', 'high', 'medium', 'low']
        priority_icons = {
            'critical': '🚨',
            'high': '⚠️',
            'medium': '💡',
            'low': 'ℹ️'
        }

        for priority in priority_order:
            if priority in by_priority:
                icon = priority_icons[priority]
                output.append(f"{icon} {priority.upper()} 问题:\n")

                for s in by_priority[priority]:
                    output.append(f"  • {s['name']}")
                    if s.get('file'):
                        output.append(f"    📁 {s['file']}")
                    output.append(f"    💬 {s['suggestion']}")
                    output.append(f"    🔧 {s['action']}")
                    output.append("")

        return "\n".join(output)

    # ========================================================================
    # 上下文感知建议
    # ========================================================================

    def suggest_next_steps(self, context: Dict) -> List[str]:
        """基于上下文建议下一步行动"""
        suggestions = []

        # 基于用户偏好
        if self.user_profile.get('preferences', {}).get('expect_suggestions'):
            # 基于项目状态建议
            if context.get('just_created_file'):
                suggestions.append("💡 建议：为新创建的文件添加单元测试")

            if context.get('just_modified_config'):
                suggestions.append("💡 建议：更新相关文档说明配置变更")

            if context.get('has_errors'):
                suggestions.append("💡 建议：优先修复错误，确保系统稳定性")

        return suggestions

    def remind_best_practices(self, action: str, context: Dict) -> List[str]:
        """提醒最佳实践"""
        reminders = []

        # 基于行动类型提醒
        action_reminders = {
            'create_file': [
                "记得添加文件头注释",
                "考虑是否需要错误处理",
                "Windows兼容性检查"
            ],
            'modify_code': [
                "保持代码风格一致",
                "更新相关注释",
                "考虑向后兼容性"
            ],
            'delete_file': [
                "检查是否有其他文件依赖",
                "更新文档和引用",
                "考虑是否需要迁移数据"
            ]
        }

        if action in action_reminders:
            reminders = action_reminders[action]

        return reminders


# ============================================================================
# 便捷函数
# ============================================================================

def quick_check(code: str, file_path: str = None) -> str:
    """
    快速检查代码

    用法:
    ```python
    from proactive_advisor import quick_check

    code = '''
    def foo(x, y):
        return x + y
    '''

    suggestions = quick_check(code, "foo.py")
    print(suggestions)
    ```
    """
    workspace_root = Path(__file__).parent.parent
    advisor = ProactiveAdvisor(workspace_root)

    suggestions = advisor.analyze_code(code, file_path)
    return advisor.format_suggestions(suggestions)


# ============================================================================
# 主程序（测试）
# ============================================================================

def main():
    """测试主动建议系统"""

    print("="*60)
    print("主动建议系统测试")
    print("="*60)

    workspace_root = Path(__file__).parent.parent
    advisor = ProactiveAdvisor(workspace_root)

    # 测试代码
    test_code = '''
def processUserInput(userData):
    # 处理用户输入
    query = "SELECT * FROM users WHERE name = '" + userData['name'] + "'"
    result = db.execute(query)

    filePath = userData['file']
    f = open(filePath, 'r')
    content = f.read()

    for i in range(100):
        results.append(processData(content))

    password = "admin123"
    return result
'''

    print("\n测试代码:")
    print(test_code)

    print("\n" + "="*60)
    print("分析结果:")
    print("="*60)

    suggestions = advisor.analyze_code(test_code, "test.py")
    print(advisor.format_suggestions(suggestions))

    print("\n" + "="*60)
    print("下一步建议:")
    print("="*60)

    next_steps = advisor.suggest_next_steps({
        'just_created_file': True,
        'has_errors': True
    })

    for step in next_steps:
        print(step)


if __name__ == "__main__":
    main()
