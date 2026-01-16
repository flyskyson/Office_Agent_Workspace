#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记忆系统效率监控

监控记忆系统的性能指标：
1. 加载时间
2. 搜索时间
3. 记忆大小
4. 记录数量

当指标超过阈值时发出警告，并提供优化建议。

作者: Claude Code
日期: 2026-01-15
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Windows 终端编码修复
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass

# 添加路径
sys.path.insert(0, str(Path(__file__).parent))

from claude_memory import ClaudeMemory


# ============================================================================
# 效率监控器
# ============================================================================

class MemoryMonitor:
    """记忆系统效率监控器"""

    # 性能阈值
    THRESHOLDS = {
        'load_time_ms': 100,        # 加载时间阈值（毫秒）
        'search_time_ms': 50,       # 搜索时间阈值（毫秒）
        'memory_size_mb': 1.0,      # 记忆大小阈值（MB）
        'total_records': 100,       # 总记录数阈值
        'high_priority_ratio': 0.3  # 高优先级记录比例阈值
    }

    def __init__(self, workspace_root: Path = None):
        self.memory = ClaudeMemory(workspace_root)
        self.workspace_root = workspace_root or Path.cwd()
        self.memory_dir = self.workspace_root / "06_Learning_Journal" / "claude_memory"

    def monitor_all(self) -> Dict[str, Any]:
        """监控所有指标"""
        results = {}

        # 1. 加载时间测试
        results['load_time'] = self._test_load_performance()

        # 2. 搜索时间测试
        results['search_time'] = self._test_search_performance()

        # 3. 记忆大小统计
        results['memory_size'] = self._get_memory_size()

        # 4. 记录数量统计
        results['record_count'] = self._get_record_count()

        # 5. 生成报告
        results['report'] = self._generate_report(results)

        # 6. 优化建议
        results['recommendations'] = self._get_recommendations(results)

        return results

    def _test_load_performance(self) -> Dict[str, Any]:
        """测试加载性能"""
        start = time.time()

        # 模拟加载所有记忆文件
        for file in self.memory_dir.glob("*.json"):
            with open(file, 'r', encoding='utf-8') as f:
                json.load(f)

        load_time = time.time() - start
        load_time_ms = load_time * 1000

        return {
            'time_ms': round(load_time_ms, 2),
            'time_seconds': round(load_time, 4),
            'status': 'OK' if load_time_ms < self.THRESHOLDS['load_time_ms'] else 'WARNING',
            'threshold_ms': self.THRESHOLDS['load_time_ms']
        }

    def _test_search_performance(self) -> Dict[str, Any]:
        """测试搜索性能"""
        # 测试不同搜索方式的性能
        search_tests = []

        # 测试1: 主题搜索
        start = time.time()
        contexts = self.memory.recall("角色定义")
        search_time = (time.time() - start) * 1000
        search_tests.append({
            'type': 'topic_search',
            'query': '角色定义',
            'time_ms': round(search_time, 2),
            'results': len(contexts)
        })

        # 测试2: 全局搜索
        start = time.time()
        results = self.memory.store.search_all_contexts("记忆", limit=10)
        search_time = (time.time() - start) * 1000
        search_tests.append({
            'type': 'global_search',
            'query': '记忆',
            'time_ms': round(search_time, 2),
            'results': len(results)
        })

        # 测试3: 高优先级检索
        start = time.time()
        high_priority = self.memory.recall_high_priority()
        search_time = (time.time() - start) * 1000
        search_tests.append({
            'type': 'high_priority',
            'query': 'N/A',
            'time_ms': round(search_time, 2),
            'results': len(high_priority)
        })

        # 计算平均搜索时间
        avg_time = sum(t['time_ms'] for t in search_tests) / len(search_tests)

        return {
            'tests': search_tests,
            'avg_time_ms': round(avg_time, 2),
            'status': 'OK' if avg_time < self.THRESHOLDS['search_time_ms'] else 'WARNING',
            'threshold_ms': self.THRESHOLDS['search_time_ms']
        }

    def _get_memory_size(self) -> Dict[str, Any]:
        """获取记忆大小"""
        total_size = 0
        file_sizes = {}

        for file in self.memory_dir.glob("*.json"):
            size = file.stat().st_size
            total_size += size
            file_sizes[file.name] = {
                'bytes': size,
                'kb': round(size / 1024, 2)
            }

        total_size_mb = total_size / (1024 * 1024)

        return {
            'total_bytes': total_size,
            'total_kb': round(total_size / 1024, 2),
            'total_mb': round(total_size_mb, 3),
            'file_sizes': file_sizes,
            'status': 'OK' if total_size_mb < self.THRESHOLDS['memory_size_mb'] else 'WARNING',
            'threshold_mb': self.THRESHOLDS['memory_size_mb']
        }

    def _get_record_count(self) -> Dict[str, Any]:
        """获取记录数量"""
        stats = self.memory.get_memory_stats()

        total = (
            stats['total_contexts'] +
            stats['total_decisions'] +
            stats['total_conversations']
        )

        high_priority_count = len(self.memory.recall_high_priority())
        high_priority_ratio = high_priority_count / max(total, 1)

        return {
            'contexts': stats['total_contexts'],
            'decisions': stats['total_decisions'],
            'conversations': stats['total_conversations'],
            'total': total,
            'high_priority_count': high_priority_count,
            'high_priority_ratio': round(high_priority_ratio, 2),
            'status': 'OK' if total < self.THRESHOLDS['total_records'] else 'WARNING',
            'threshold': self.THRESHOLDS['total_records']
        }

    def _generate_report(self, results: Dict[str, Any]) -> str:
        """生成性能报告"""
        report_lines = [
            "\n" + "=" * 70,
            "📊 记忆系统效率监控报告",
            "=" * 70,
            f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            ""
        ]

        # 加载性能
        load = results['load_time']
        status_icon = "✅" if load['status'] == 'OK' else "⚠️"
        report_lines.extend([
            f"⚡ 加载性能",
            f"   时间: {load['time_ms']} ms / {load['threshold_ms']} ms {status_icon}",
            f"   状态: {load['status']}",
            ""
        ])

        # 搜索性能
        search = results['search_time']
        status_icon = "✅" if search['status'] == 'OK' else "⚠️"
        report_lines.extend([
            f"🔍 搜索性能",
            f"   平均时间: {search['avg_time_ms']} ms / {search['threshold_ms']} ms {status_icon}",
            ""
        ])
        for test in search['tests']:
            report_lines.append(
                f"   - {test['type']}: {test['time_ms']} ms ({test['results']} 结果)"
            )
        report_lines.append("")

        # 记忆大小
        size = results['memory_size']
        status_icon = "✅" if size['status'] == 'OK' else "⚠️"
        report_lines.extend([
            f"💾 记忆大小",
            f"   总大小: {size['total_kb']} KB ({size['total_mb']} MB) {status_icon}",
            f"   阈值: {size['threshold_mb']} MB",
            ""
        ])

        # 记录数量
        count = results['record_count']
        status_icon = "✅" if count['status'] == 'OK' else "⚠️"
        report_lines.extend([
            f"📝 记录数量",
            f"   总记录: {count['total']} / {count['threshold']} {status_icon}",
            f"   - 上下文: {count['contexts']}",
            f"   - 决策: {count['decisions']}",
            f"   - 对话: {count['conversations']}",
            f"   - 高优先级: {count['high_priority_count']} ({count['high_priority_ratio']*100:.0f}%)",
            ""
        ])

        # 总体评估
        warnings = [
            results['load_time']['status'],
            results['search_time']['status'],
            results['memory_size']['status'],
            results['record_count']['status']
        ]

        if all(w == 'OK' for w in warnings):
            report_lines.extend([
                "🎉 总体评估: ✅ 所有指标正常",
                "   记忆系统运行良好，无需优化。"
            ])
        else:
            warning_count = sum(1 for w in warnings if w == 'WARNING')
            report_lines.extend([
                f"⚠️ 总体评估: {warning_count} 个指标需要关注",
                "   建议查看优化建议部分。"
            ])

        report_lines.append("=" * 70)

        return "\n".join(report_lines)

    def _get_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """获取优化建议"""
        recommendations = []

        # 检查加载时间
        if results['load_time']['status'] == 'WARNING':
            recommendations.append(
                "⚠️ 加载时间过长，建议:\n"
                "   1. 添加记忆索引系统\n"
                "   2. 归档旧记忆到单独文件\n"
                "   3. 考虑使用二进制格式（如pickle）"
            )

        # 检查搜索时间
        if results['search_time']['status'] == 'WARNING':
            recommendations.append(
                "⚠️ 搜索时间过长，建议:\n"
                "   1. 实现记忆索引（按主题、标签、优先级）\n"
                "   2. 使用字典查找替代线性搜索\n"
                "   3. 限制搜索结果数量"
            )

        # 检查记忆大小
        if results['memory_size']['status'] == 'WARNING':
            recommendations.append(
                "⚠️ 记忆大小过大，建议:\n"
                "   1. 清理过期记忆（90天以上）\n"
                "   2. 归档旧记忆到 02_Project_Archive\n"
                "   3. 只保留高优先级和最近记忆"
            )

        # 检查记录数量
        if results['record_count']['status'] == 'WARNING':
            recommendations.append(
                "⚠️ 记录数量过多，建议:\n"
                "   1. 设置记忆优先级，只保留重要的\n"
                "   2. 定期清理低优先级记录\n"
                "   3. 实现记忆分级存储系统"
            )

        # 检查高优先级比例
        if results['record_count']['high_priority_ratio'] < 0.1:
            recommendations.append(
                "💡 高优先级记忆较少，建议:\n"
                "   1. 将重要的角色定义、用户偏好标记为高优先级\n"
                "   2. 定期审查记忆优先级\n"
                "   3. 确保关键信息不会丢失"
            )

        if not recommendations:
            recommendations.append("✅ 所有指标正常，暂无优化建议。")

        return recommendations

    def save_performance_history(self, results: Dict[str, Any]):
        """保存性能历史"""
        history_file = self.memory_dir / "performance_history.jsonl"

        # 记录本次性能数据
        record = {
            'timestamp': datetime.now().isoformat(),
            'load_time_ms': results['load_time']['time_ms'],
            'search_time_ms': results['search_time']['avg_time_ms'],
            'memory_size_kb': results['memory_size']['total_kb'],
            'total_records': results['record_count']['total'],
            'warnings': [
                results['load_time']['status'],
                results['search_time']['status'],
                results['memory_size']['status'],
                results['record_count']['status']
            ]
        }

        # 追加到历史文件
        with open(history_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')

        return history_file

    def plot_performance_trend(self):
        """绘制性能趋势图（需要matplotlib）"""
        try:
            import matplotlib.pyplot as plt
            import matplotlib.dates as mdates
        except ImportError:
            print("⚠️ 需要安装 matplotlib: pip install matplotlib")
            return

        history_file = self.memory_dir / "performance_history.jsonl"

        if not history_file.exists():
            print("⚠️ 暂无历史数据")
            return

        # 读取历史数据
        records = []
        with open(history_file, 'r', encoding='utf-8') as f:
            for line in f:
                records.append(json.loads(line))

        if len(records) < 2:
            print("⚠️ 数据不足，无法绘制趋势图")
            return

        # 准备数据
        timestamps = [datetime.fromisoformat(r['timestamp']) for r in records]
        load_times = [r['load_time_ms'] for r in records]
        search_times = [r['search_time_ms'] for r in records]
        memory_sizes = [r['memory_size_kb'] for r in records]

        # 创建图表
        fig, axes = plt.subplots(3, 1, figsize=(12, 10))
        fig.suptitle('记忆系统性能趋势', fontsize=16)

        # 加载时间趋势
        axes[0].plot(timestamps, load_times, 'b-o', label='加载时间')
        axes[0].axhline(y=self.THRESHOLDS['load_time_ms'], color='r', linestyle='--', label='阈值')
        axes[0].set_ylabel('时间 (ms)')
        axes[0].set_title('加载性能')
        axes[0].legend()
        axes[0].grid(True)

        # 搜索时间趋势
        axes[1].plot(timestamps, search_times, 'g-o', label='搜索时间')
        axes[1].axhline(y=self.THRESHOLDS['search_time_ms'], color='r', linestyle='--', label='阈值')
        axes[1].set_ylabel('时间 (ms)')
        axes[1].set_title('搜索性能')
        axes[1].legend()
        axes[1].grid(True)

        # 记忆大小趋势
        axes[2].plot(timestamps, memory_sizes, 'm-o', label='记忆大小')
        axes[2].axhline(y=self.THRESHOLDS['memory_size_mb'] * 1024, color='r', linestyle='--', label='阈值')
        axes[2].set_ylabel('大小 (KB)')
        axes[2].set_xlabel('时间')
        axes[2].set_title('记忆大小')
        axes[2].legend()
        axes[2].grid(True)

        # 格式化x轴
        for ax in axes:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

        plt.tight_layout()

        # 保存图表
        output_file = self.memory_dir / "performance_trend.png"
        plt.savefig(output_file, dpi=100, bbox_inches='tight')
        print(f"✅ 趋势图已保存: {output_file}")

        plt.close()


# ============================================================================
# 便捷函数
# ============================================================================

def monitor_performance(show_recommendations: bool = True) -> Dict[str, Any]:
    """监控性能（便捷函数）"""
    monitor = MemoryMonitor()
    results = monitor.monitor_all()

    # 打印报告
    print(results['report'])

    # 打印建议
    if show_recommendations:
        if any(w == 'WARNING' for w in [
            results['load_time']['status'],
            results['search_time']['status'],
            results['memory_size']['status'],
            results['record_count']['status']
        ]):
            print("\n💡 优化建议:")
            print("-" * 70)
            for i, rec in enumerate(results['recommendations'], 1):
                print(f"\n{i}. {rec}")
        else:
            print("\n✅ 系统运行良好，无需优化。")

    # 保存历史
    monitor.save_performance_history(results)

    return results


# ============================================================================
# 命令行入口
# ============================================================================

def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description='记忆系统效率监控')
    parser.add_argument('--plot', '-p', action='store_true',
                       help='绘制性能趋势图')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='安静模式')

    args = parser.parse_args()

    # 监控性能
    results = monitor_performance(show_recommendations=not args.quiet)

    # 绘制趋势图
    if args.plot:
        monitor = MemoryMonitor()
        monitor.plot_performance_trend()

    return 0


if __name__ == "__main__":
    sys.exit(main())
