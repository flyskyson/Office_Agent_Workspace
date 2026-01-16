#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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


"""
向量语义记忆系统

基于ChromaDB和sentence-transformers的语义搜索实现，
为Claude Code提供真正的语义理解能力。

作者: Claude Code
日期: 2026-01-16
版本: v2.0
"""

import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

# Windows 终端编码修复
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass

# ============================================================================
# 导入依赖（延迟导入以提供友好的错误信息）
# ============================================================================

def check_dependencies():
    """检查必要的依赖是否安装"""
    missing = []

    try:
        import chromadb
    except ImportError:
        missing.append('chromadb')

    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        missing.append('sentence-transformers')

    return missing


# ============================================================================
# 语义记忆核心类
# ============================================================================

class SemanticMemory:
    """
    向量语义记忆系统

    基于ChromaDB和sentence-transformers实现高性能语义搜索。

    特性:
    - 真正的语义理解（非关键词匹配）
    - 中英文混合支持
    - 亚毫秒级搜索速度
    - 自动增量更新
    - 元数据过滤
    """

    # 推荐的中文嵌入模型
    RECOMMENDED_MODELS = {
        'fast': 'paraphrase-multilingual-MiniLM-L12-v2',  # 快速，适合大多数场景
        'quality': 'paraphrase-multilingual-mpnet-base-v2',  # 高质量
        'large': 'moka-ai/m3e-large',  # 中文专用大模型
    }

    def __init__(self,
                 workspace_root: Optional[Path] = None,
                 model_name: str = 'fast',
                 collection_name: str = 'claude_memories'):
        """
        初始化语义记忆系统

        参数:
            workspace_root: 工作区根目录
            model_name: 嵌入模型名称 ('fast', 'quality', 'large' 或具体模型名)
            collection_name: ChromaDB集合名称
        """
        # 检查依赖
        missing = check_dependencies()
        if missing:
            print(f"❌ 缺少依赖: {', '.join(missing)}")
            print("📦 请运行: pip install", ' '.join(missing))
            raise ImportError(f"Missing dependencies: {missing}")

        # 初始化工作区
        if workspace_root is None:
            workspace_root = Path(__file__).parent.parent

        self.workspace_root = Path(workspace_root)
        self.vector_db_dir = self.workspace_root / "06_Learning_Journal" / "vector_db"

        # 确保目录存在
        self.vector_db_dir.mkdir(parents=True, exist_ok=True)

        # 初始化嵌入模型
        self._init_embedder(model_name)

        # 初始化ChromaDB
        self._init_chroma(collection_name)

        # 统计信息
        self.stats = {
            'total_memories': 0,
            'last_update': None,
            'model_name': self.model_name
        }

    def _init_embedder(self, model_name: str):
        """初始化嵌入模型"""
        from sentence_transformers import SentenceTransformer

        # 解析模型名称
        if model_name in self.RECOMMENDED_MODELS:
            self.model_name = self.RECOMMENDED_MODELS[model_name]
        else:
            self.model_name = model_name

        print(f"🔄 加载嵌入模型: {self.model_name}")
        self.embedder = SentenceTransformer(self.model_name)
        print(f"✅ 模型加载完成")

        # 记录模型维度
        self.embedding_dim = self.embedder.get_sentence_embedding_dimension()
        print(f"📊 嵌入维度: {self.embedding_dim}")

    def _init_chroma(self, collection_name: str):
        """初始化ChromaDB"""
        import chromadb

        # 创建持久化客户端
        print(f"🔄 初始化向量数据库: {self.vector_db_dir}")
        self.chroma_client = chromadb.PersistentClient(
            path=str(self.vector_db_dir)
        )

        # 获取或创建集合
        try:
            self.collection = self.chroma_client.get_collection(name=collection_name)
            print(f"✅ 加载现有集合: {collection_name}")
            print(f"📊 现有记忆数: {self.collection.count()}")
        except:
            self.collection = self.chroma_client.create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}  # 使用余弦相似度
            )
            print(f"✅ 创建新集合: {collection_name}")

    def add_memory(self,
                   memory_id: str,
                   text: str,
                   metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        添加记忆到向量数据库

        参数:
            memory_id: 记忆唯一ID
            text: 记忆文本内容
            metadata: 附加元数据

        返回:
            是否成功
        """
        try:
            # 生成嵌入向量
            embedding = self.embedder.encode(text, convert_to_numpy=True).tolist()

            # 准备元数据
            if metadata is None:
                metadata = {}

            # 添加时间戳
            metadata['timestamp'] = datetime.now().isoformat()
            metadata['text_length'] = len(text)

            # 转换元数据值为字符串（ChromaDB要求）
            metadata_str = {k: str(v) for k, v in metadata.items()}

            # 添加到集合
            self.collection.add(
                ids=[memory_id],
                embeddings=[embedding],
                documents=[text],
                metadatas=[metadata_str]
            )

            # 更新统计
            self.stats['total_memories'] = self.collection.count()
            self.stats['last_update'] = datetime.now().isoformat()

            return True

        except Exception as e:
            print(f"❌ 添加记忆失败: {e}")
            return False

    def add_memories_batch(self,
                          memories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        批量添加记忆（更高效）

        参数:
            memories: 记忆列表，每个记忆包含 id, text, metadata

        返回:
            批量操作结果统计
        """
        results = {
            'success': 0,
            'failed': 0,
            'errors': []
        }

        try:
            # 批量生成嵌入
            texts = [m['text'] for m in memories]
            embeddings = self.embedder.encode(texts, convert_to_numpy=True).tolist()

            # 准备数据
            ids = [m['id'] for m in memories]
            documents = texts
            metadatas = []

            for m in memories:
                metadata = m.get('metadata', {})
                metadata['timestamp'] = datetime.now().isoformat()
                metadata['text_length'] = len(m['text'])
                # 转换为字符串
                metadatas.append({k: str(v) for k, v in metadata.items()})

            # 批量添加
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas
            )

            results['success'] = len(memories)

        except Exception as e:
            results['failed'] = len(memories)
            results['errors'].append(str(e))

        # 更新统计
        self.stats['total_memories'] = self.collection.count()
        self.stats['last_update'] = datetime.now().isoformat()

        return results

    def search(self,
              query: str,
              top_k: int = 5,
              filter_metadata: Optional[Dict[str, str]] = None) -> List[Dict[str, Any]]:
        """
        语义搜索

        参数:
            query: 搜索查询
            top_k: 返回前K个结果
            filter_metadata: 元数据过滤条件

        返回:
            搜索结果列表，每个结果包含:
            - id: 记忆ID
            - text: 记忆文本
            - metadata: 元数据
            - score: 相似度分数 (0-1)
        """
        try:
            # 生成查询嵌入
            query_embedding = self.embedder.encode(query, convert_to_numpy=True).tolist()

            # 执行搜索
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=filter_metadata
            )

            # 格式化结果
            formatted_results = []

            if results['ids'] and len(results['ids']) > 0:
                for i, memory_id in enumerate(results['ids'][0]):
                    # ChromaDB返回的距离，转换为相似度 (cosine distance -> similarity)
                    distance = results['distances'][0][i]
                    similarity = 1 - distance  # 余弦距离转相似度

                    formatted_results.append({
                        'id': memory_id,
                        'text': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'similarity_score': round(similarity, 4),
                        'distance': round(distance, 4)
                    })

            return formatted_results

        except Exception as e:
            print(f"❌ 搜索失败: {e}")
            return []

    def hybrid_search(self,
                     query: str,
                     keyword_results: List[Dict[str, Any]],
                     top_k: int = 5,
                     semantic_weight: float = 0.7) -> List[Dict[str, Any]]:
        """
        混合搜索（语义+关键词）

        结合语义搜索和关键词搜索的结果，
       通过加权融合获得更准确的结果。

        参数:
            query: 搜索查询
            keyword_results: 关键词搜索结果
            top_k: 返回前K个结果
            semantic_weight: 语义搜索权重 (0-1)

        返回:
            融合后的搜索结果
        """
        # 语义搜索
        semantic_results = self.search(query, top_k=top_k * 2)

        # 创建ID到结果的映射
        result_map = {}

        # 添加语义结果
        for result in semantic_results:
            result_map[result['id']] = {
                'result': result,
                'semantic_score': result['similarity_score'],
                'keyword_score': 0.0
            }

        # 融合关键词结果
        for i, kw_result in enumerate(keyword_results):
            result_id = kw_result.get('id') or kw_result.get('timestamp', '')

            if result_id in result_map:
                # 已存在，更新关键词分数
                # 关键词分数：位置越靠前分数越高
                kw_score = 1.0 - (i / len(keyword_results))
                result_map[result_id]['keyword_score'] = kw_score
            else:
                # 不存在，添加新结果
                kw_score = 1.0 - (i / len(keyword_results))
                result_map[result_id] = {
                    'result': kw_result,
                    'semantic_score': 0.0,
                    'keyword_score': kw_score
                }

        # 计算融合分数
        for result_id, data in result_map.items():
            data['hybrid_score'] = (
                data['semantic_score'] * semantic_weight +
                data['keyword_score'] * (1 - semantic_weight)
            )

        # 排序并返回top-k
        sorted_results = sorted(
            result_map.values(),
            key=lambda x: x['hybrid_score'],
            reverse=True
        )[:top_k]

        # 添加分数信息到结果中
        final_results = []
        for data in sorted_results:
            result = data['result'].copy()
            result['scores'] = {
                'semantic': round(data['semantic_score'], 4),
                'keyword': round(data['keyword_score'], 4),
                'hybrid': round(data['hybrid_score'], 4)
            }
            final_results.append(result)

        return final_results

    def delete_memory(self, memory_id: str) -> bool:
        """删除记忆"""
        try:
            self.collection.delete(ids=[memory_id])
            self.stats['total_memories'] = self.collection.count()
            return True
        except Exception as e:
            print(f"❌ 删除失败: {e}")
            return False

    def update_memory(self,
                     memory_id: str,
                     text: Optional[str] = None,
                     metadata: Optional[Dict[str, Any]] = None) -> bool:
        """更新记忆"""
        try:
            # ChromaDB不支持直接更新，需要先删除再添加
            self.delete_memory(memory_id)

            # 获取原始数据（如果只更新部分字段）
            if text is None or metadata is None:
                # 这里需要从备份存储中获取原始数据
                # 暂时要求提供完整数据
                raise ValueError("更新需要提供完整的text和metadata")

            # 重新添加
            return self.add_memory(memory_id, text, metadata)

        except Exception as e:
            print(f"❌ 更新失败: {e}")
            return False

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        self.stats['total_memories'] = self.collection.count()
        return self.stats.copy()

    def clear_all(self) -> bool:
        """清空所有记忆（危险操作）"""
        try:
            self.chroma_client.delete_collection(self.collection.name)
            self._init_chroma(self.collection.name)
            self.stats['total_memories'] = 0
            return True
        except Exception as e:
            print(f"❌ 清空失败: {e}")
            return False

    def print_stats(self):
        """打印统计信息"""
        stats = self.get_stats()

        print("\n" + "=" * 70)
        print("🧠 语义记忆系统统计")
        print("=" * 70)
        print(f"\n📊 记忆数量: {stats['total_memories']}")
        print(f"🤖 模型: {stats['model_name']}")
        print(f"📏 嵌入维度: {self.embedding_dim}")
        print(f"🕐 最后更新: {stats['last_update']}")
        print(f"📁 数据库路径: {self.vector_db_dir}")
        print("\n" + "=" * 70)


# ============================================================================
# 记忆迁移工具
# ============================================================================

class MemoryMigrator:
    """
    记忆迁移工具

    将现有的JSON记忆迁移到向量数据库
    """

    def __init__(self, semantic_memory: SemanticMemory):
        self.semantic_memory = semantic_memory

    def migrate_from_json(self,
                         json_file: Path,
                         batch_size: int = 10) -> Dict[str, Any]:
        """
        从JSON文件迁移记忆

        参数:
            json_file: JSON记忆文件路径
            batch_size: 批量处理大小

        返回:
            迁移结果统计
        """
        if not json_file.exists():
            return {'error': '文件不存在'}

        # 读取JSON
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 提取contexts
        contexts = data.get('contexts', [])

        if not contexts:
            return {'error': '没有找到contexts'}

        # 批量迁移
        results = {
            'total': len(contexts),
            'success': 0,
            'failed': 0
        }

        for i in range(0, len(contexts), batch_size):
            batch = contexts[i:i + batch_size]

            # 准备记忆数据
            memories = []
            for ctx in batch:
                # 组合文本（主题+摘要）
                text = f"{ctx.get('topic', '')}. {ctx.get('summary', '')}"

                # 准备元数据
                metadata = {
                    'topic': ctx.get('topic', ''),
                    'session_id': ctx.get('session_id', ''),
                    'priority': ctx.get('priority', 'normal'),
                    'tags': ','.join(ctx.get('tags', [])),
                    'timestamp': ctx.get('timestamp', '')
                }

                memories.append({
                    'id': ctx.get('timestamp', str(hash(text))),
                    'text': text,
                    'metadata': metadata
                })

            # 批量添加
            batch_result = self.semantic_memory.add_memories_batch(memories)
            results['success'] += batch_result['success']
            results['failed'] += batch_result['failed']

            print(f"🔄 进度: {min(i + batch_size, len(contexts))}/{len(contexts)}")

        return results


# ============================================================================
# 演示程序
# ============================================================================

def demo_semantic_memory():
    """演示语义记忆系统"""

    print("""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║              向量语义记忆系统演示 (v2.0)                            ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
    """)

    # 创建语义记忆
    semantic = SemanticMemory()

    # 添加示例记忆
    print("\n📝 添加示例记忆...")
    print("-" * 70)

    memories = [
        {
            'id': 'mem_001',
            'text': '多Agent系统开发：创建了基于WorkflowEngine的多Agent演示系统',
            'metadata': {'topic': '多Agent系统', 'priority': 'high'}
        },
        {
            'id': 'mem_002',
            'text': '市场监管智能体：使用Jinja2模板引擎生成个体工商户开业申请书',
            'metadata': {'topic': '市场监管', 'priority': 'normal'}
        },
        {
            'id': 'mem_003',
            'text': 'Claude Code核心角色定义：不只是会用工具的AI，而是有记忆、能思考、会进化的协作伙伴',
            'metadata': {'topic': '角色定义', 'priority': 'high'}
        },
        {
            'id': 'mem_004',
            'text': '实现自动记忆加载系统：创建session_initializer.py，实现每次会话开始时自动加载角色定义',
            'metadata': {'topic': '记忆系统', 'priority': 'high'}
        },
        {
            'id': 'mem_005',
            'text': '日常维护任务：清理临时文件，整理文档目录',
            'metadata': {'topic': '日常任务', 'priority': 'low'}
        }
    ]

    result = semantic.add_memories_batch(memories)
    print(f"✅ 批量添加完成: {result['success']} 成功, {result['failed']} 失败")

    # 语义搜索演示
    print("\n🔍 语义搜索演示")
    print("-" * 70)

    queries = [
        "Agent相关的",
        "如何生成申请书",
        "记忆和角色",
        "系统维护"
    ]

    for query in queries:
        print(f"\n💭 查询: {query}")
        results = semantic.search(query, top_k=2)

        for i, result in enumerate(results, 1):
            print(f"\n   结果 {i}:")
            print(f"   📄 内容: {result['text'][:80]}...")
            print(f"   🎯 相似度: {result['similarity_score']:.2%}")
            print(f"   📌 主题: {result['metadata'].get('topic', 'N/A')}")

    # 显示统计
    semantic.print_stats()

    print("\n✅ 演示完成！")


if __name__ == "__main__":
    demo_semantic_memory()
