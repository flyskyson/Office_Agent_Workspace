#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
笔记索引器
扫描学习笔记和项目代码，生成向量嵌入并存入数据库
"""

import yaml
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple
from tqdm import tqdm

from embedder import TextEmbedder
from vector_store import VectorStore


class DocumentIndexer:
    """文档索引器 - 扫描和索引学习资料"""

    def __init__(self, config_path="config.yaml"):
        """初始化索引器"""
        # 加载配置
        config_path = Path(__file__).parent / config_path
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

        self.workspace_root = Path(__file__).parent.parent.parent

        # 初始化嵌入器和向量数据库
        self.embedder = TextEmbedder(config_path)
        self.vector_store = VectorStore(config_path)

        # 统计信息
        self.stats = {
            'indexed': 0,
            'skipped': 0,
            'failed': 0
        }

    def scan_sources(self) -> List[Dict]:
        """
        扫描所有配置的源目录

        Returns:
            文档信息列表
        """
        all_docs = []

        # 扫描学习日志
        all_docs.extend(self._scan_learning_journal())

        # 扫描项目代码
        all_docs.extend(self._scan_projects())

        return all_docs

    def _scan_learning_journal(self) -> List[Dict]:
        """扫描学习日志目录"""
        source_config = self.config['sources']['learning_journal']
        base_path = self.workspace_root / source_config['path']

        if not base_path.exists():
            print(f"⚠️  学习日志目录不存在: {base_path}")
            return []

        print(f"\n📚 扫描学习日志: {base_path}")

        docs = []
        patterns = source_config['patterns']
        exclude_patterns = source_config.get('exclude_patterns', [])

        for pattern in patterns:
            matched_files = list(base_path.glob(pattern))

            for file_path in tqdm(matched_files, desc=f"  扫描 {pattern}"):
                # 检查排除规则
                if self._should_exclude(file_path, exclude_patterns):
                    continue

                # 读取文件
                content = self._read_file(file_path)
                if content is None:
                    continue

                # 解析元数据
                metadata = self._parse_metadata(file_path, content, 'journal')

                docs.append({
                    'content': content,
                    'metadata': metadata,
                    'file_path': file_path
                })

        print(f"   找到 {len(docs)} 个学习笔记文件")
        return docs

    def _scan_projects(self) -> List[Dict]:
        """扫描项目代码"""
        source_config = self.config['sources']['projects']
        base_path = self.workspace_root / source_config['path']

        if not base_path.exists():
            print(f"⚠️  项目目录不存在: {base_path}")
            return []

        print(f"\n💻 扫描项目代码: {base_path}")

        docs = []
        patterns = source_config['patterns']
        exclude_patterns = source_config.get('exclude_patterns', [])

        for pattern in patterns:
            matched_files = list(base_path.glob(pattern))

            for file_path in tqdm(matched_files, desc=f"  扫描 {pattern}"):
                # 检查排除规则
                if self._should_exclude(file_path, exclude_patterns):
                    continue

                # 读取文件
                content = self._read_file(file_path)
                if content is None:
                    continue

                # 解析元数据
                metadata = self._parse_metadata(file_path, content, 'project')

                docs.append({
                    'content': content,
                    'metadata': metadata,
                    'file_path': file_path
                })

        print(f"   找到 {len(docs)} 个项目文件")
        return docs

    def _should_exclude(self, file_path: Path, exclude_patterns: List[str]) -> bool:
        """检查文件是否应该被排除"""
        file_str = str(file_path)

        for pattern in exclude_patterns:
            if pattern in file_str:
                return True

        return False

    def _read_file(self, file_path: Path) -> str:
        """读取文件内容"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"❌ 读取文件失败 {file_path}: {e}")
            self.stats['failed'] += 1
            return None

    def _parse_metadata(self, file_path: Path, content: str, doc_type: str) -> Dict:
        """解析文档元数据"""
        # 相对路径（便于显示）
        rel_path = file_path.relative_to(self.workspace_root)

        # 文件修改时间
        mtime = datetime.fromtimestamp(file_path.stat().st_mtime)

        # 提取标题（Markdown文件的第一行#标题）
        title = file_path.stem
        if doc_type == 'journal' and content.strip().startswith('#'):
            first_line = content.strip().split('\n')[0]
            if first_line.startswith('#'):
                title = first_line.lstrip('#').strip()

        metadata = {
            'title': title,
            'path': str(rel_path),
            'type': doc_type,
            'extension': file_path.suffix,
            'modified': mtime.strftime("%Y-%m-%d %H:%M:%S"),
            'modified_timestamp': mtime.timestamp()
        }

        # 提取分类（基于目录结构）
        path_parts = rel_path.parts
        if len(path_parts) > 2:
            metadata['category'] = path_parts[2]  # 例如: daily_logs, challenges_solved

        return metadata

    def index_documents(self, docs: List[Dict], batch_size: int = 32):
        """
        批量索引文档

        Args:
            docs: 文档列表
            batch_size: 批处理大小
        """
        if not docs:
            print("⚠️  没有文档需要索引")
            return

        print(f"\n🔄 开始索引 {len(docs)} 个文档...")

        # 分批处理
        for i in tqdm(range(0, len(docs), batch_size), desc="生成嵌入向量"):
            batch = docs[i:i + batch_size]

            # 提取内容
            contents = [doc['content'] for doc in batch]
            metadatas = [doc['metadata'] for doc in batch]

            # 生成ID（基于文件路径的哈希）
            ids = [hashlib.md5(str(doc['file_path']).encode()).hexdigest() for doc in batch]

            # 生成嵌入
            embeddings = self.embedder.embed_texts(contents)

            # 检查是否已存在
            existing_docs = []
            new_contents = []
            new_embeddings = []
            new_metadatas = []
            new_ids = []

            for j, (content, emb, meta, doc_id) in enumerate(zip(contents, embeddings, metadatas, ids)):
                existing = self.vector_store.get_document(doc_id)

                # 如果已存在，更新
                if existing:
                    self.vector_store.update_document(
                        doc_id=doc_id,
                        document=content,
                        embedding=emb,
                        metadata=meta
                    )
                    self.stats['indexed'] += 1
                else:
                    # 新文档
                    new_contents.append(content)
                    new_embeddings.append(emb)
                    new_metadatas.append(meta)
                    new_ids.append(doc_id)

            # 添加新文档
            if new_contents:
                self.vector_store.add_documents(
                    documents=new_contents,
                    embeddings=new_embeddings,
                    metadatas=new_metadatas,
                    ids=new_ids
                )
                self.stats['indexed'] += len(new_contents)

    def build_index(self):
        """构建完整索引"""
        print("\n" + "=" * 70)
        print("🚀 开始构建学习记忆索引")
        print("=" * 70)

        # 扫描文档
        docs = self.scan_sources()

        if not docs:
            print("\n⚠️  未找到任何文档")
            return

        # 索引文档
        self.index_documents(docs)

        # 显示统计
        print("\n" + "=" * 70)
        print("📊 索引完成")
        print("=" * 70)
        print(f"✅ 成功索引: {self.stats['indexed']} 个")
        print(f"⏭️  跳过: {self.stats['skipped']} 个")
        print(f"❌ 失败: {self.stats['failed']} 个")
        print(f"\n📚 总文档数: {self.vector_store.count()}")


def main():
    """主函数"""
    indexer = DocumentIndexer()
    indexer.build_index()


if __name__ == "__main__":
    main()
