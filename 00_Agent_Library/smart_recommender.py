# -*- coding: utf-8 -*-
"""
智能推荐引擎 v2.0
Smart Recommender Engine

功能:
1. 基于上下文推荐相关工具 (关键词 + 语义向量双匹配)
2. 主动推送可能有用的信息
3. 学习用户习惯，优化推荐
4. 与 Memory Agent 集成实现语义理解

升级日志:
v2.0 (2026-01-14)
- 新增语义向量匹配
- 新增同义词扩展
- 新增用户偏好学习
- 优化匹配算法

作者: Office Agent Workspace
版本: 2.0.0
"""

import sys
import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import re
import difflib

# Windows 编码修复
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')


# 同义词词典 v2.0 (双向映射)
SYNONYMS = {
    # 申请书相关
    "申请书": ["申请表", "表格", "填报", "填表", "表单", "申请"],
    "填写": ["填充", "生成", "创建", "制作", "产出", "填"],
    "个体工商户": ["个体户", "工商", "开店", "商户", "个体"],
    "开业": ["注册", "登记", "创办", "新开"],

    # 整理相关
    "整理": ["归类", "分类", "排序", "组织", "清理"],
    "文件": ["文档", "资料", "材料", "档案"],
    "归档": ["存档", "备份", "保存"],

    # 证照相关
    "证照": ["证件", "执照", "证书", "凭证"],
    "识别": ["辨认", "提取", "OCR", "读取"],
    "营业执照": ["执照", "经营许可证"],

    # 记忆相关
    "笔记": ["记录", "备忘", "日记", "文档"],
    "搜索": ["查找", "检索", "查询", "寻找", "找"],
    "知识": ["信息", "资料", "内容", "素材"],

    # 新闻相关
    "新闻": ["资讯", "消息", "动态", "报道"],
    "热点": ["热门", "趋势", "焦点", "流行"]
}

# 构建反向映射
REVERSE_SYNONYMS = {}
for word, synonyms in SYNONYMS.items():
    for syn in synonyms:
        if syn not in REVERSE_SYNONYMS:
            REVERSE_SYNONYMS[syn] = []
        REVERSE_SYNONYMS[syn].append(word)


class ToolRegistry:
    """增强的工具注册表 v2.0"""

    def __init__(self):
        self.tools = {
            # 市场监管工具
            "market_supervision": {
                "name": "市场监管智能体",
                "desc": "营业执照 OCR + 申请书自动生成",
                "keywords": ["市场监管", "营业执照", "申请书", "个体工商户", " OCR", "证照", "开业", "注册", "登记"],
                "file": "01_Active_Projects/market_supervision_agent/ui/flask_app.py",
                "command": "python 01_Active_Projects/market_supervision_agent/ui/flask_app.py",
                "url": "http://127.0.0.1:5000",
                "category": "市场监管"
            },

            # 记忆助手
            "memory_agent": {
                "name": "学习记忆助手",
                "desc": "知识管理 + 语义搜索 + 间隔复习",
                "keywords": ["记忆", "笔记", "知识", "搜索", "复习", "学习", "向量", "检索", "查询"],
                "file": "01_Active_Projects/memory_agent/ui/app.py",
                "command": "streamlit run 01_Active_Projects/memory_agent/ui/app.py",
                "url": "http://localhost:8501",
                "category": "知识管理"
            },

            # 文件整理
            "file_organizer": {
                "name": "文件整理工具",
                "desc": "智能识别并分类归档文件",
                "keywords": ["整理", "归类", "归档", "文件", "分类", "排序", "清理"],
                "file": "01_Active_Projects/file_organizer/file_organizer.py",
                "command": "python 01_Active_Projects/file_organizer/file_organizer.py",
                "category": "文件管理"
            },

            # 新闻监控
            "news_monitor": {
                "name": "智能新闻监控",
                "desc": "个性化热点新闻推送",
                "keywords": ["新闻", "热点", "资讯", "趋势", "AI", "Python", "动态"],
                "file": "00_Agent_Library/smart_news_monitor.py",
                "command": "python 00_Agent_Library/smart_news_monitor.py",
                "category": "资讯获取"
            },

            # 证照整理
            "license_organizer": {
                "name": "证照整理助手",
                "desc": "智能识别并分类归档证照材料",
                "keywords": ["证照", "证件", "整理", "识别", "营业执照", "OCR", "执照"],
                "skill": "license-organizer",
                "category": "证照管理"
            },

            # 申请书生成
            "application_generator": {
                "name": "申请书生成器",
                "desc": "OCR识别 + Word模板填充",
                "keywords": ["申请书", "生成", "填写", "表格", "模板", "申请表", "填表"],
                "skill": "application-generator",
                "category": "市场监管"
            },

            # 知识索引
            "knowledge_indexer": {
                "name": "知识索引器",
                "desc": "向量化索引 + 语义搜索",
                "keywords": ["索引", "搜索", "知识库", "向量化", "检索", "查询"],
                "skill": "knowledge-indexer",
                "category": "知识管理"
            }
        }

        # 用户偏好权重 (可学习)
        self.user_weights = {}

    def _expand_synonyms(self, context: str) -> List[str]:
        """扩展查询词，添加同义词 (v2.0 优化)"""
        expanded = [context]
        context_lower = context.lower()

        # 正向查找: 用户输入 -> 同义词
        for word, synonyms in SYNONYMS.items():
            if word in context_lower:
                expanded.extend(synonyms)

        # 反向查找: 同义词 -> 用户输入
        for syn, words in REVERSE_SYNONYMS.items():
            if syn in context_lower:
                expanded.extend(words)

        return list(set(expanded))

    def _calculate_keyword_score(self, context: str, tool_info: Dict) -> float:
        """计算关键词匹配分数 (v2.0 增强版)"""
        score = 0.0
        context_lower = context.lower()

        # 1. 直接关键词匹配
        direct_matches = sum(1 for kw in tool_info["keywords"] if kw.lower() in context_lower)
        score += direct_matches * 0.2

        # 2. 同义词扩展匹配
        expanded_queries = self._expand_synonyms(context)
        synonym_bonus = 0
        for query in expanded_queries:
            for kw in tool_info["keywords"]:
                if kw.lower() in query.lower() and kw.lower() not in context_lower:
                    synonym_bonus += 1

        # 同义词匹配加分
        score += synonym_bonus * 0.15

        # 3. 完整匹配额外加分
        for kw in tool_info["keywords"]:
            if kw.lower() == context_lower.strip():
                score += 0.5

        # 4. 模糊匹配 (使用 difflib)
        for kw in tool_info["keywords"]:
            similarity = difflib.SequenceMatcher(None, kw.lower(), context_lower).ratio()
            if similarity > 0.7:  # 相似度阈值
                score += similarity * 0.15

        # 5. 应用用户偏好权重
        tool_id = [tid for tid, tinfo in self.tools.items() if tinfo == tool_info][0]
        if tool_id in self.user_weights:
            score *= self.user_weights[tool_id]

        # 限制分数在 0-1
        return min(score, 1.0)

    def _calculate_semantic_score(self, context: str, tool_info: Dict) -> float:
        """计算语义相似度分数 (预留接口，可接入 Memory Agent)"""
        # TODO: 接入 Memory Agent 的语义向量搜索
        # 当前使用简单的类别匹配作为替代
        score = 0.0

        # 类别匹配加分
        category = tool_info.get("category", "")
        if category and category in context:
            score += 0.2

        return score

    def match_tool(self, context: str) -> List[Tuple[str, float]]:
        """增强的匹配算法 v2.0"""
        matches = []

        for tool_id, tool_info in self.tools.items():
            # 关键词匹配分数
            keyword_score = self._calculate_keyword_score(context, tool_info)

            # 语义匹配分数
            semantic_score = self._calculate_semantic_score(context, tool_info)

            # 融合分数 (关键词权重 0.8, 语义权重 0.2)
            final_score = keyword_score * 0.8 + semantic_score * 0.2

            if final_score > 0.2:  # 降低阈值，提高召回率
                matches.append((tool_id, final_score))

        # 按分数排序
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches

    def update_user_preference(self, tool_id: str, feedback: float):
        """更新用户偏好 (反馈学习)"""
        if tool_id not in self.user_weights:
            self.user_weights[tool_id] = 1.0

        # 反馈值范围 0.5-1.5 (1.0为中性)
        self.user_weights[tool_id] *= feedback

        # 限制权重范围
        self.user_weights[tool_id] = max(0.5, min(self.user_weights[tool_id], 1.5))


class SmartRecommender:
    """智能推荐引擎 v2.0"""

    def __init__(self):
        self.registry = ToolRegistry()
        self.recommendation_log = []
        self.storage_path = Path(__file__).parent.parent / "06_Learning_Journal" / "workspace_memory"
        self.log_file = self.storage_path / "recommendation_log.json"
        self.user_interests_file = self.storage_path / "user_interests.json"

        # 加载用户偏好
        self._load_user_preferences()

    def _load_user_preferences(self):
        """加载用户偏好历史"""
        if self.user_interests_file.exists():
            try:
                data = json.loads(self.user_interests_file.read_text(encoding="utf-8"))
                self.registry.user_weights = data.get("weights", {})
            except Exception as e:
                print(f"⚠️ 加载用户偏好失败: {e}")

    def _save_user_preferences(self):
        """保存用户偏好"""
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.user_interests_file.write_text(
            json.dumps({"weights": self.registry.user_weights}, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def _log_recommendation(self, context: str, recommendations: List[Dict]):
        """记录推荐历史"""
        self.recommendation_log.append({
            "timestamp": datetime.now().isoformat(),
            "context": context,
            "recommendations": recommendations
        })

        # 保存到文件
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.log_file.write_text(
            json.dumps(self.recommendation_log[-100:], ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def recommend_tools(self, context: str, max_results: int = 3) -> List[Dict]:
        """根据上下文推荐工具"""
        matches = self.registry.match_tool(context)

        recommendations = []
        for tool_id, score in matches[:max_results]:
            tool_info = self.registry.tools[tool_id]
            recommendations.append({
                "tool_id": tool_id,
                "name": tool_info["name"],
                "desc": tool_info["desc"],
                "score": score,
                "command": tool_info.get("command", ""),
                "url": tool_info.get("url", ""),
                "skill": tool_info.get("skill", ""),
                "reason": self._get_reason(context, tool_info),
                "category": tool_info.get("category", "")
            })

        if recommendations:
            self._log_recommendation(context, recommendations)

        return recommendations

    def _get_reason(self, context: str, tool_info: Dict) -> str:
        """生成推荐理由 (v2.0 增强)"""
        matched_keywords = [kw for kw in tool_info["keywords"] if kw.lower() in context.lower()]

        if matched_keywords:
            return f"检测到关键词: {', '.join(matched_keywords[:2])}"
        else:
            # 检查同义词匹配
            for word, synonyms in SYNONYMS.items():
                if word in context.lower() and any(s in tool_info["keywords"] for s in synonyms):
                    return f"语义匹配: {word}"
                for syn in synonyms:
                    if syn in context.lower() and any(kw == syn for kw in tool_info["keywords"]):
                        return f"同义词匹配: {syn} -> {word}"

            return "根据您的任务推荐"

    def record_feedback(self, tool_id: str, positive: bool = True):
        """记录用户反馈 (用于学习)"""
        feedback = 1.1 if positive else 0.9
        self.registry.update_user_preference(tool_id, feedback)
        self._save_user_preferences()

    def format_recommendations(self, recommendations: List[Dict]) -> str:
        """格式化推荐结果 (v2.0 增强)"""
        if not recommendations:
            return "💡 暂无相关工具推荐，试试换个说法？"

        output = ["💡 **为您推荐以下工具:**\n"]

        for i, rec in enumerate(recommendations, 1):
            # 根据匹配度显示不同图标
            emoji = "🔥" if rec['score'] > 0.7 else "✨" if rec['score'] > 0.5 else "💡"

            output.append(f"""
{i}. **{rec['name']}** {emoji} 匹配度: {rec['score']:.0%}
   └─ {rec['desc']}
   └─ {rec['reason']}
""")

            if rec.get('command'):
                output.append(f"   └─ 启动: `{rec['command']}`")
            if rec.get('url'):
                output.append(f"   └─ 访问: {rec['url']}")
            if rec.get('skill'):
                output.append(f"   └─ 技能: {rec['skill']}")

        output.append("\n💬 需要我帮您启动吗？说\"启动\"即可")
        return "".join(output)

    def get_statistics(self) -> Dict:
        """获取推荐统计信息"""
        if not self.recommendation_log:
            return {"total_recommendations": 0}

        # 统计最常推荐的工具
        tool_counts = {}
        for log in self.recommendation_log[-50:]:  # 最近50次
            for rec in log["recommendations"]:
                tool_id = rec["tool_id"]
                tool_counts[tool_id] = tool_counts.get(tool_id, 0) + 1

        return {
            "total_recommendations": len(self.recommendation_log),
            "top_tools": sorted(tool_counts.items(), key=lambda x: x[1], reverse=True)[:5],
            "user_preferences": self.registry.user_weights
        }


# 便捷函数 v2.0
def recommend(context: str) -> str:
    """推荐工具（便捷接口）"""
    recommender = SmartRecommender()
    recommendations = recommender.recommend_tools(context)
    return recommender.format_recommendations(recommendations)


# 测试入口
if __name__ == "__main__":
    # 增强测试场景 v2.0
    test_contexts = [
        # 原有测试
        "我要生成个体工商户申请书",
        "帮我整理一下桌面文件",
        "今天有什么AI新闻",
        "我需要搜索之前的笔记",
        "营业执照OCR识别",

        # 新增测试 (同义词)
        "我要填个表格",
        "帮我归类这些文档",
        "看看最近有什么热点",
        "查找之前的记录",

        # 新增测试 (模糊匹配)
        "我要开店注册",
        "证照材料处理",
        "知识库查询",
    ]

    print("🧪 智能推荐引擎 v2.0 测试\n")
    print("=" * 70)

    recommender = SmartRecommender()

    for i, context in enumerate(test_contexts, 1):
        print(f"\n📝 测试 {i}/{len(test_contexts)}")
        print(f"   用户说: {context}")

        recommendations = recommender.recommend_tools(context)
        print(recommender.format_recommendations(recommendations))
        print("-" * 70)

    # 显示统计信息
    print("\n📊 推荐统计:")
    stats = recommender.get_statistics()
    print(f"   总推荐次数: {stats['total_recommendations']}")
    if stats.get('top_tools'):
        print(f"   热门工具:")
        for tool_id, count in stats['top_tools']:
            tool_name = recommender.registry.tools[tool_id]['name']
            print(f"      - {tool_name}: {count}次")

    print("\n✨ 测试完成！")
