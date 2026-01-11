"""
智能体核心功能测试
"""

import pytest
import sys
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agent_core import MarketSupervisionAgent


def test_agent_initialization():
    """测试智能体初始化"""
    agent = MarketSupervisionAgent()

    assert agent.logger is not None
    assert agent.config is not None


def test_annual_report_processing():
    """测试年报处理"""
    agent = MarketSupervisionAgent()

    sample_data = {
        'company_name': '测试公司',
        'credit_code': '91110000XXXXXXXXXX',
        'year': 2024
    }

    # 注意：这里只测试调用，不测试实际执行
    # 实际执行需要真实的浏览器环境和网站
    result = agent.process_annual_report(sample_data)

    # 由于没有实际实现，目前会返回 True
    assert isinstance(result, bool)


def test_batch_processing():
    """测试批量处理"""
    agent = MarketSupervisionAgent()

    tasks = [
        {
            'type': 'annual_report',
            'data': {
                'company_name': '公司A',
                'year': 2024
            }
        },
        {
            'type': 'annual_report',
            'data': {
                'company_name': '公司B',
                'year': 2024
            }
        }
    ]

    results = agent.batch_process(tasks)

    assert results['total'] == 2
    assert 'success' in results
    assert 'failed' in results


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
