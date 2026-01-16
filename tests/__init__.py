"""
Office Agent Workspace - 测试套件

测试结构:
- unit/       : 单元测试（测试单个函数/类）
- integration/ : 集成测试（测试组件间交互）
- e2e/        : 端到端测试（测试完整工作流）
- fixtures/   : 测试数据和夹具
- mocks/      : Mock 对象和模拟服务

运行测试:
    pytest                    # 运行所有测试
    pytest tests/unit/        # 只运行单元测试
    pytest -m "not slow"      # 排除慢速测试
    pytest --cov=00_Agent_Library  # 生成覆盖率报告
"""

__version__ = "2.0.0"
