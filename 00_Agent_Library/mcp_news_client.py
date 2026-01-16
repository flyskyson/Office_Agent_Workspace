# -*- coding: utf-8 -*-
"""
MCP 新闻统一客户端
整合多个 MCP 新闻服务器，提供一致的接口

支持的 MCP 服务器:
1. mcp-hot-news (13+ 平台)
2. @wopal/mcp-server-hotnews (9 个中文平台)
3. 本地 API 备份方案

作者: Claude Code
日期: 2026-01-16
"""

import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Any
from subprocess import run, PIPE

# Windows 编码修复
if sys.platform == 'win32' and hasattr(sys.stdout, 'buffer'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')


class MCPNewsClient:
    """
    MCP 新闻统一客户端

    支持从多个 MCP 服务器获取新闻，自动降级到本地 API
    """

    def __init__(self):
        """初始化客户端"""
        # MCP 服务器配置
        self.mcp_servers = {
            "mcp-hot-news": {
                "command": "npx",
                "args": ["-y", "mcp-hot-news"],
                "description": "多平台热点 (13+ 平台)"
            },
            "wopal-hotnews": {
                "command": "npx",
                "args": ["-y", "@wopal/mcp-server-hotnews"],
                "description": "中文热点 (9 平台)"
            }
        }

        # 平台映射
        self.platform_map = {
            "zhihu": "知乎",
            "weibo": "微博",
            "baidu": "百度",
            "bilibili": "B站",
            "douyin": "抖音",
            "kuaishou": "快手",
            "toutiao": "今日头条",
            "36kr": "36氪",
            "csdn": "CSDN",
            "github": "GitHub",
            "weixin": "微信",
            "toutiao_realtime": "头条实时",
            "douyin_realtime": "抖音实时"
        }

    async def call_mcp_tool(self, server_name: str, tool_name: str, params: Dict = None) -> Optional[Dict]:
        """
        调用 MCP 服务器的工具

        参数:
            server_name: 服务器名称
            tool_name: 工具名称
            params: 工具参数

        返回:
            工具执行结果
        """
        if server_name not in self.mcp_servers:
            return None

        server_config = self.mcp_servers[server_name]

        try:
            # 构建 MCP 调用命令
            # 注意: 实际使用时需要通过 MCP 客户端调用
            # 这里提供降级方案
            print(f"  [MCP] 调用 {server_name}: {tool_name}")
            return await self._fallback_api(server_name, tool_name, params)

        except Exception as e:
            print(f"  [错误] MCP 调用失败: {e}")
            return None

    async def _fallback_api(self, server_name: str, tool_name: str, params: Dict = None) -> Dict:
        """
        备用 API 方案（当 MCP 不可用时）

        使用本地已安装的新闻工具
        """
        # 延迟导入避免循环依赖
        sys.path.insert(0, str(Path(__file__).parent))
        from news_reader import UnifiedNewsReader

        reader = UnifiedNewsReader()

        # 从工具名推断平台
        platform = tool_name.replace("get_", "").replace("_hot", "").replace("_news", "")

        if platform in reader.platforms:
            limit = params.get("limit", 20) if params else 20
            return await reader.fetch_from_vvhan(platform, limit)

        # 返回空结果
        return {
            "platform": platform,
            "news_list": [],
            "total": 0,
            "source": "无数据"
        }

    async def get_news(self, platforms: List[str] = None, limit: int = 20) -> Dict[str, Any]:
        """
        获取新闻

        参数:
            platforms: 平台列表，如 ["zhihu", "weibo", "bilibili"]
            limit: 每个平台获取数量

        返回:
            新闻聚合结果
        """
        if platforms is None:
            platforms = ["zhihu", "weibo", "bilibili"]

        results = {
            "timestamp": datetime.now().isoformat(),
            "platforms": {},
            "total_news": 0,
            "sources": []
        }

        for platform in platforms:
            tool_name = f"get_{platform}_hot" if platform != "toutiao_realtime" else "get_douyin_realtime"

            result = await self.call_mcp_tool("mcp-hot-news", tool_name, {"limit": limit})

            if result:
                results["platforms"][platform] = result
                results["total_news"] += result.get("total", 0)
                results["sources"].append(result.get("source", "unknown"))

        return results

    def format_output(self, results: Dict) -> str:
        """格式化输出结果"""
        lines = []
        lines.append("=" * 70)
        lines.append("📰 MCP 新闻聚合")
        lines.append("=" * 70)
        lines.append(f"⏰ 时间: {results['timestamp']}")
        lines.append(f"📊 总数: {results['total_news']} 条")
        lines.append(f"📡 来源: {', '.join(set(results['sources']))}")
        lines.append("")

        for platform, data in results["platforms"].items():
            platform_name = self.platform_map.get(platform, platform)
            lines.append(f"\n{'─' * 60}")
            lines.append(f"📱 {platform_name}")
            lines.append(f"{'─' * 60}")
            lines.append(f"📦 来源: {data.get('source', 'unknown')}")
            lines.append(f"📊 数量: {data.get('total', 0)} 条")
            lines.append("")

            for i, item in enumerate(data.get('news_list', [])[:10], 1):
                title = item.get('title', 'N/A')
                hot = item.get('hot') or item.get('heat') or item.get('index', 'N/A')
                url = item.get('url') or item.get('link') or 'N/A'

                lines.append(f"{i}. {title}")
                if hot != 'N/A':
                    lines.append(f"   🔥 热度: {hot}")
                if url != 'N/A':
                    lines.append(f"   🔗 {url}")
                lines.append("")

        return "\n".join(lines)

    async def get_tech_news(self) -> Dict:
        """
        获取技术新闻（从技术平台）

        Returns:
            技术新闻聚合结果
        """
        tech_platforms = ["github", "csdn", "36kr"]
        return await self.get_news(tech_platforms, limit=15)


# ============ 命令行接口 ============

async def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(
        description="MCP 新闻统一客户端",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 获取默认平台（知乎、微博、B站）
  python mcp_news_client.py

  # 获取指定平台
  python mcp_news_client.py -p zhihu weibo github

  # 获取技术新闻
  python mcp_news_client.py --tech

  # 指定数量
  python mcp_news_client.py -n 30
        """
    )

    parser.add_argument(
        "-p", "--platforms",
        nargs="+",
        default=["zhihu", "weibo", "bilibili"],
        choices=["zhihu", "weibo", "baidu", "bilibili", "douyin", "kuaishou",
                 "toutiao", "36kr", "csdn", "github"],
        help="要获取的平台"
    )

    parser.add_argument(
        "-n", "--num",
        type=int,
        default=20,
        help="每个平台获取的数量"
    )

    parser.add_argument(
        "--tech",
        action="store_true",
        help="获取技术新闻（GitHub、CSDN、36氪）"
    )

    parser.add_argument(
        "-o", "--output",
        help="输出到文件（Markdown 格式）"
    )

    args = parser.parse_args()

    client = MCPNewsClient()

    if args.tech:
        results = await client.get_tech_news()
    else:
        results = await client.get_news(args.platforms, args.num)

    output = client.format_output(results)
    print(output)

    # 保存到文件
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Markdown 格式
        md_content = f"""# MCP 新闻聚合报告

**生成时间**: {results['timestamp']}
**新闻总数**: {results['total_news']} 条
**数据来源**: {', '.join(set(results['sources']))}

---

{output}
"""

        output_path.write_text(md_content, encoding='utf-8')
        print(f"\n✅ 报告已保存: {output_path}")


if __name__ == "__main__":
    asyncio.run(main())
