# 知识索引技能 (Knowledge Indexer)

**描述**: 智能知识库索引工具，扫描工作区学习笔记、项目代码、文档资料，生成语义向量索引，支持自然语言搜索和智能复习。当用户需要"索引笔记"、"更新知识库"、"构建搜索索引"、"学习笔记索引"时触发。适用于知识管理、代码检索、学习回顾。不支持索引网络资源或需要特殊权限的文件。

---

## 概述

本技能自动化构建和维护知识库索引，核心功能：
1. **全文扫描**: 扫描 Markdown、Python、TXT 等文件
2. **语义向量化**: 使用 sentence-transformers 生成向量嵌入
3. **智能索引**: 存储到 ChromaDB 本地向量数据库
4. **增量更新**: 只索引新增或修改的文件

**关键优势**：
- 语义搜索，理解查询意图
- 本地存储，隐私安全
- 增量更新，高效维护
- 多语言支持，中英皆可

---

## 前置条件

### 必需文件
```
01_Active_Projects/memory_agent/
├── memory_agent.py              # 主程序
├── embedder.py                  # 文本嵌入模块
├── vector_store.py              # 向量数据库（ChromaDB）
├── indexer.py                   # 索引器
├── config.yaml                  # 配置文件
└── data/                        # ChromaDB 数据目录
```

### 环境依赖
```bash
pip install chromadb sentence-transformers jieba
```

### 首次运行
```bash
# 下载嵌入模型（约500MB，仅首次）
cd 01_Active_Projects/memory_agent
python memory_agent.py index
```

---

## 执行步骤

### 步骤 1: 确定索引范围

**询问用户**：
```
要索引哪些内容？
A. 全部工作区（学习笔记+项目代码）
B. 仅学习笔记（06_Learning_Journal/）
C. 仅项目代码（01_Active_Projects/）
D. 自定义目录
```

**默认索引路径**：
```yaml
学习笔记: ../06_Learning_Journal/
项目代码: ../01_Active_Projects/
工作文档: ../04_Data_&_Resources/
```

---

### 步骤 2: 扫描文件

**执行命令**：
```bash
cd 01_Active_Projects/memory_agent
python memory_agent.py scan <目标目录>
```

**扫描结果示例**：
```
扫描 06_Learning_Journal/:
├── Markdown 文件: 45 个
├── Python 文件: 12 个
├── JSON 文件: 8 个
└── 其他: 5 个

总计: 70 个文件待索引
```

---

### 步骤 3: 文件解析

**支持的文件类型**：

| 类型 | 扩展名 | 解析方法 |
|------|--------|---------|
| Markdown | .md | 提取标题、段落、代码块 |
| Python | .py | 提取函数、类、文档字符串 |
| 文本 | .txt | 直接提取文本 |
| JSON | .json | 提取键值对内容 |

**解析代码示例**：
```python
from indexer import DocumentIndexer

indexer = DocumentIndexer()

# 解析单个文件
doc = indexer.parse_file("example.md")
# 输出: {
#   "content": "文件内容",
#   "metadata": {"title": "标题", "path": "example.md"},
#   "chunks": ["片段1", "片段2", ...]
# }

# 批量解析目录
docs = indexer.parse_directory("../06_Learning_Journal/")
```

---

### 步骤 4: 生成向量嵌入

**嵌入模型**：
```
模型: paraphrase-multilingual-mpnet-base-v2
语言: 中文、英文
维度: 768 维向量
设备: CPU（可配置 GPU）
```

**嵌入代码**：
```python
from embedder import TextEmbedder

embedder = TextEmbedder(model_name="paraphrase-multilingual-mpnet-base-v2")

# 生成单个向量
vector = embedder.embed("如何批量重命名文件？")
# 输出: [0.12, -0.34, 0.56, ...]  (768维)

# 批量生成（更快）
vectors = embedder.embed_batch([
    "文件重命名技巧",
    "批量处理方法",
    "Path操作指南"
])
```

---

### 步骤 5: 存储到向量数据库

**数据库配置**：
```yaml
vector_db:
  type: chromadb
  persist_directory: ../06_Learning_Journal/workspace_memory/chroma_db
  collection_name: knowledge_base
```

**存储代码**：
```python
from vector_store import VectorStore

store = VectorStore(persist_directory="data/chroma_db")

# 创建或获取集合
collection = store.get_or_create_collection("knowledge_base")

# 添加文档
collection.add(
    documents=docs,           # 文本内容
    embeddings=vectors,       # 向量嵌入
    metadatas=metadata_list,  # 元数据（路径、类型等）
    ids=doc_ids              # 唯一ID
)

# 持久化到磁盘
store.persist()
```

---

### 步骤 6: 增量更新

**检测变更**：
```python
def check_updates(last_index_time):
    """检测新增或修改的文件"""
    new_files = []
    modified_files = []

    for file in scan_directory():
        if file.created > last_index_time:
            new_files.append(file)
        elif file.modified > last_index_time:
            modified_files.append(file)

    return new_files + modified_files
```

**增量索引**：
```bash
# 只索引变更的文件
python memory_agent.py index --incremental
```

---

## 使用示例

### 示例 1: 首次全量索引

```
你: 帮我索引一下我的学习笔记

我: 好的，开始扫描学习笔记目录...

    扫描 06_Learning_Journal/:
    ├── 发现 70 个文件

    正在解析和向量化...
    [██████████] 100% 70/70

    正在存储到向量数据库...
    ✅ 索引完成！

    统计信息：
    - 已索引文档: 70 个
    - 向量维度: 768
    - 数据库大小: 15.2 MB
    - 存储位置: 06_Learning_Journal/workspace_memory/chroma_db

    现在可以进行语义搜索了！
```

---

### 示例 2: 增量更新

```
你: 更新知识库，只索引新增的笔记

我: 好的，检测上次索引后的变更...

    发现 5 个新文件：
    ├── 20260113_python技巧.md
    ├── 20260113_调试方法.md
    └── ...

    正在索引新增文件...
    ✅ 增量更新完成！
```

---

### 示例 3: 重建索引

```
你: 重新构建整个索引

我: 好的，这将清空现有索引并重建...

    ⚠️ 警告：这将删除现有向量数据库
    要继续吗？(y/n)

    [用户确认 y]

    清空旧索引...
    扫描全部文件...
    重建向量数据库...
    ✅ 重建完成！
```

---

## 配置说明

### 编辑配置文件

编辑 [config.yaml](../../01_Active_Projects/memory_agent/config.yaml)：

```yaml
# 向量数据库
vector_db:
  persist_directory: "../06_Learning_Journal/workspace_memory/chroma_db"
  collection_name: "knowledge_base"

# 文本嵌入模型
embedding:
  model_name: "paraphrase-multilingual-mpnet-base-v2"
  device: "cpu"  # 或 "cuda" 如果有GPU
  batch_size: 32

# 索引配置
indexing:
  chunk_size: 500              # 文本分块大小
  chunk_overlap: 50            # 分块重叠
  file_extensions:             # 支持的文件类型
    - .md
    - .py
    - .txt
    - .json

# 排除目录
exclude_dirs:
  - __pycache__
  - venv
  - node_modules
  - .git
```

---

## 错误处理

### 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| `ModelNotFoundError` | 嵌入模型未下载 | 首次运行会自动下载，请等待 |
| `CorruptionError` | 数据库损坏 | 删除数据库目录重新索引 |
| `EncodingError` | 文件编码问题 | 跳过该文件或转换编码为 UTF-8 |
| `OOMError` | 内存不足 | 减小 `batch_size` 或使用更小的模型 |

### 跳过机制

```python
# 遇到无法解析的文件时跳过
try:
    doc = parse_file(file)
except Exception as e:
    print(f"⚠️ 跳过文件 {file}: {e}")
    log_error(file, e)
    continue
```

---

## 性能优化

### 批量处理

```python
# 批量嵌入（比逐个快10倍）
embedder.embed_batch(texts, batch_size=32)
```

### 并行索引

```python
from concurrent.futures import ThreadPoolExecutor

def parallel_index(files):
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(index_single_file, files)
```

### 缓存机制

```python
# 缓存已嵌入的文本
@lru_cache(maxsize=1000)
def get_cached_embedding(text):
    return embedder.embed(text)
```

---

## 验证索引

### 搜索测试

```bash
# 测试索引是否正常
python memory_agent.py search "文件重命名"
```

**期望输出**：
```
🔍 搜索结果（相似度 > 0.5）:
================================
1. batch_rename_helper.py
   📁 01_Active_Projects/file_organizer/
   🎯 相似度: 0.89
   📝 批量重命名文件工具...

2. file_operations.md
   📁 06_Learning_Journal/notes/
   🎯 相似度: 0.76
   📝 文件操作最佳实践...
```

### 数据库检查

```python
import chromadb

db = chromadb.PersistentClient(path="data/chroma_db")
collection = db.get_collection("knowledge_base")

print(f"文档总数: {collection.count()}")
print(f"维度: {len(collection.get(limit=1)['embeddings'][0])}")
```

---

## 展开功能

### 多模态索引

```python
# 未来支持图片索引
from embedder import ImageEmbedder

img_embedder = ImageEmbedder()
img_vector = img_embedder.embed("screenshot.png")
```

### 实时监控

```python
# 监控文件变化，自动更新索引
from watchdog.observers import Observer

class IndexWatcher(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.md'):
            index_single_file(event.src_path)
```

---

## 相关文件

- **核心代码**: [01_Active_Projects/memory_agent/memory_agent.py](../../01_Active_Projects/memory_agent/memory_agent.py)
- **嵌入模块**: [01_Active_Projects/memory_agent/embedder.py](../../01_Active_Projects/memory_agent/embedder.py)
- **向量存储**: [01_Active_Projects/memory_agent/vector_store.py](../../01_Active_Projects/memory_agent/vector_store.py)
- **索引器**: [01_Active_Projects/memory_agent/indexer.py](../../01_Active_Projects/memory_agent/indexer.py)
- **配置文件**: [01_Active_Projects/memory_agent/config.yaml](../../01_Active_Projects/memory_agent/config.yaml)
- **数据库**: [06_Learning_Journal/workspace_memory/chroma_db/](../../06_Learning_Journal/workspace_memory/chroma_db/)

---

## 版本历史

- **v1.0** (2026-01-13): 初始版本，支持全量索引和增量更新

---

**技能触发关键词**: `索引笔记`、`更新知识库`、`构建索引`、`学习笔记索引`、`向量化`、`语义搜索索引`
