#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境监控器 - 让我主动感知工作区状态

目标：
1. 监控文件变更
2. 检测Git提交
3. 追踪工作区活跃度
4. 预测用户需求

作者: Claude Code
日期: 2026-01-17
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import subprocess
import os

# Windows 终端编码修复
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer)
    except:
        pass


class WorkspaceMonitor:
    """
    工作区环境监控器

    功能：
    1. 检测文件变更
    2. 监控Git活动
    3. 分析工作区活跃度
    4. 预测用户需求
    """

    def __init__(self, workspace_root: Path = None):
        """初始化监控器"""
        if workspace_root is None:
            workspace_root = Path(__file__).parent.parent.parent

        self.workspace_root = workspace_root
        self.state_file = workspace_root / "06_Learning_Journal/workspace_memory" / "monitor_state.json"
        self.state_file.parent.mkdir(parents=True, exist_ok=True)

        self.state = self._load_state()

    def _load_state(self) -> Dict:
        """加载监控状态"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass

        # 初始状态
        return {
            'last_check': None,
            'file_snapshots': {},
            'git_commits': [],
            'activity_log': []
        }

    def _save_state(self):
        """保存监控状态"""
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2, default=str)

    def check_environment(self) -> Dict[str, Any]:
        """检查环境状态"""
        print("\n" + "=" * 60)
        print("🔍 工作区环境监控")
        print("=" * 60)

        now = datetime.now()

        # 1. 检测Git活动
        git_status = self._check_git_activity()
        print(f"\n📊 Git状态:")
        print(f"  未提交文件: {git_status['uncommitted_count']}")
        print(f"  最近提交: {git_status['last_commit']}")

        # 2. 检测文件变更
        file_changes = self._detect_file_changes()
        print(f"\n📁 文件变更:")
        if file_changes['new_files']:
            print(f"  新增文件: {len(file_changes['new_files'])} 个")
        if file_changes['modified_files']:
            print(f"  修改文件: {len(file_changes['modified_files'])} 个")

        # 3. 工作区活跃度
        activity = self._analyze_activity()
        print(f"\n📈 活跃度:")
        print(f"  今日活跃度: {activity['today_score']}")
        print(f"  趋势: {activity['trend']}")

        # 4. 预测用户需求
        predictions = self._predict_needs(git_status, file_changes, activity)
        print(f"\n💡 需求预测:")
        for prediction in predictions:
            print(f"  • [{prediction['priority']}] {prediction['need']}")

        # 更新状态
        self.state['last_check'] = now.isoformat()
        self._save_state()

        return {
            'git_status': git_status,
            'file_changes': file_changes,
            'activity': activity,
            'predictions': predictions
        }

    def _check_git_activity(self) -> Dict[str, Any]:
        """检查Git活动"""
        try:
            # 检查未提交文件
            result = subprocess.run(
                ['git', 'status', '--short'],
                capture_output=True,
                text=True,
                cwd=self.workspace_root,
                timeout=5
            )

            uncommitted = result.stdout.strip().count('\n') if result.stdout.strip() else 0
            if result.stderr:
                uncommitted = 0

            # 检查最近提交
            result = subprocess.run(
                ['git', 'log', '-1', '--format=%h %s %ar'],
                capture_output=True,
                text=True,
                cwd=self.workspace_root,
                timeout=5
            )

            last_commit = result.stdout.strip() if result.returncode == 0 else "无"

            return {
                'uncommitted_count': uncommitted,
                'last_commit': last_commit,
                'has_changes': uncommitted > 0
            }
        except Exception as e:
            return {
                'uncommitted_count': 0,
                'last_commit': "无法获取",
                'has_changes': False
            }

    def _detect_file_changes(self) -> Dict[str, List[str]]:
        """检测文件变更"""
        new_files = []
        modified_files = []

        # 简化实现：检查最近修改的文件
        now = datetime.now()
        recent_threshold = now - timedelta(hours=24)

        # 遍历项目目录
        for root_dir in ['00_Agent_Library', '01_Active_Projects', '05_Outputs']:
            dir_path = self.workspace_root / root_dir
            if not dir_path.exists():
                continue

            try:
                for file_path in dir_path.rglob('*.py'):
                    if file_path.is_file():
                        # 检查修改时间
                        mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                        if mtime > recent_threshold:
                            rel_path = file_path.relative_to(self.workspace_root)
                            if 'test' in str(rel_path).lower():
                                continue
                            modified_files.append(str(rel_path))
            except Exception:
                pass

        return {
            'new_files': new_files,
            'modified_files': modified_files
        }

    def _analyze_activity(self) -> Dict[str, Any]:
        """分析工作区活跃度"""
        today = datetime.now().date()
        activity_log = self.state.get('activity_log', [])

        # 计算今日活跃度
        today_activities = [a for a in activity_log if datetime.fromisoformat(a['timestamp']).date() == today]
        today_score = len(today_activities)

        # 分析趋势
        if len(activity_log) >= 7:
            recent_week = activity_log[-7:]
            recent_scores = [a['score'] for a in recent_week]
            avg = sum(recent_scores) / len(recent_scores)
            if today_score > avg * 1.5:
                trend = "上升"
            elif today_score < avg * 0.5:
                trend = "下降"
            else:
                trend = "稳定"
        else:
            trend = "数据不足"

        return {
            'today_score': today_score,
            'trend': trend,
            'total_activities': len(activity_log)
        }

    def _predict_needs(self, git_status: Dict, file_changes: Dict, activity: Dict) -> List[Dict]:
        """预测用户需求"""
        predictions = []

        # 基于Git状态预测
        if git_status['uncommitted_count'] > 5:
            predictions.append({
                'need': "代码可能需要提交",
                'reason': f"有{git_status['uncommitted_count']}个未提交文件",
                'priority': '高'
            })

        # 基于文件变更预测
        if file_changes['modified_files']:
            # 检查是否有Python文件被修改
            py_files = [f for f in file_changes['modified_files'] if f.endswith('.py')]
            if py_files:
                predictions.append({
                    'need': "代码测试或审查",
                    'reason': f"检测到{len(py_files)}个Python文件被修改",
                    'priority': '中'
                })

        # 基于活跃度预测
        if activity['trend'] == "上升":
            predictions.append({
                'need': "可能需要休息或总结",
                'reason': "活跃度上升，注意劳逸结合",
                'priority': '低'
            })

        # 基于时间预测
        hour = datetime.now().hour
        if 8 <= hour < 10:
            predictions.append({
                'need': "晨间规划和新闻获取",
                'reason': "早上是规划工作的好时机",
                'priority': '中'
            })
        elif 17 <= hour < 20:
            predictions.append({
                'need': "代码审查和整理",
                'reason': "傍晚适合总结和整理",
                'priority': '中'
            })

        # 基于历史记录
        last_check = self.state.get('last_check')
        if last_check:
            last_check_time = datetime.fromisoformat(last_check)
            hours_since = (now - last_check_time).total_seconds() / 3600
            if hours_since > 24:
                predictions.append({
                    'need': "检查系统状态",
                    'reason': f"距离上次检查已过{hours_since:.1f}小时",
                    'priority': '中'
                })

        return predictions


def auto_monitor():
    """自动监控并报告"""
    monitor = WorkspaceMonitor()
    status = monitor.check_environment()

    # 生成建议
    print("\n" + "=" * 60)
    print("📋 主动建议")
    print("=" * 60)

    if status['predictions']:
        print("\n基于当前状态，我建议:")
        for i, pred in enumerate(status['predictions'], 1):
            print(f"  {i}. {pred['need']} (优先级: {pred['priority']})")
            print(f"     理由: {pred['reason']}")
    else:
        print("\n当前工作区状态良好，暂无特殊建议")

    # 记录活动日志
    monitor.state['activity_log'].append({
        'timestamp': datetime.now().isoformat(),
        'activity': 'environment_check',
        'score': len(status['predictions'])
    })
    monitor._save_state()

    return status


if __name__ == "__main__":
    print("🤖 工作区环境监控器启动...")
    auto_monitor()
    print("\n✅ 监控完成")
