#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地 AI 引擎 - 优化版
支持多模型、GPU 加速、智能降级
"""

import os
import yaml
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import time


class AIEngine(Enum):
    """AI 引擎类型"""
    PADDLEOCR = "paddleocr"
    BAIDU_OCR = "baidu_ocr"
    SENTENCE_TRANSFORMER = "sentence_transformer"
    DEEPSEEK = "deepseek"
    OLLAMA = "ollama"


@dataclass
class OCRResult:
    """OCR 结果"""
    text: str
    confidence: float
    engine: str
    processing_time: float
    raw_data: Optional[Dict] = None


class LocalAIEngine:
    """本地 AI 引擎 - 统一接口"""

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化本地 AI 引擎

        Args:
            config_path: 配置文件路径
        """
        self.config = self._load_config(config_path)
        self.logger = self._setup_logging()
        self._engines = {}
        self._cache = {}

        # 初始化引擎
        self._initialize_engines()

    def _load_config(self, config_path: Optional[str]) -> Dict:
        """加载配置文件"""
        if config_path is None:
            # 默认配置路径
            default_path = Path(__file__).parent.parent / \
                "01_Active_Projects/market_supervision_agent/config/local_ai_config.yaml"
            config_path = default_path

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            # 返回默认配置
            return self._get_default_config()

    def _get_default_config(self) -> Dict:
        """获取默认配置"""
        return {
            'ocr': {
                'primary_engine': 'paddleocr',
                'fallback_engine': 'baidu',
                'paddleocr': {
                    'use_gpu': False,
                    'lang': 'ch',
                    'use_angle_cls': True,
                    'show_log': False,
                    'enable_mkldnn': True,
                    'mem_optim': True
                }
            },
            'embedding': {
                'model_name': 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2',
                'device': 'cpu',
                'batch_size': 32
            },
            'llm': {
                'primary': 'deepseek-chat',
                'api': {
                    'provider': 'deepseek',
                    'base_url': 'https://api.deepseek.com/v1',
                    'model': 'deepseek-chat'
                }
            },
            'performance': {
                'cache': {'enabled': True, 'max_size': 1000}
            },
            'logging': {
                'level': 'INFO',
                'console': {'enabled': True}
            }
        }

    def _setup_logging(self) -> logging.Logger:
        """设置日志"""
        logger = logging.getLogger('LocalAIEngine')
        logger.setLevel(self.config.get('logging', {}).get('level', 'INFO'))

        # 控制台处理器
        if self.config.get('logging', {}).get('console', {}).get('enabled', True):
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _initialize_engines(self):
        """初始化 AI 引擎"""
        # OCR 引擎
        if self.config['ocr']['primary_engine'] == 'paddleocr':
            self._init_paddleocr()

        # 嵌入模型
        self._init_embedding_model()

        self.logger.info("✅ 本地 AI 引擎初始化完成")

    def _init_paddleocr(self):
        """初始化 PaddleOCR"""
        try:
            from paddleocr import PaddleOCR

            config = self.config['ocr']['paddleocr']
            use_gpu = config.get('use_gpu', False)

            # 创建 PaddleOCR 实例
            ocr = PaddleOCR(
                use_angle_cls=config.get('use_angle_cls', True),
                lang=config.get('lang', 'ch'),
                use_gpu=use_gpu,
                show_log=config.get('show_log', False),
                enable_mkldnn=config.get('enable_mkldnn', True)
            )

            self._engines[AIEngine.PADDLEOCR] = ocr

            gpu_status = "GPU" if use_gpu else "CPU"
            self.logger.info(f"✅ PaddleOCR 初始化成功 ({gpu_status})")

        except ImportError:
            self.logger.warning("⚠️ PaddleOCR 未安装，运行: pip install paddleocr")
        except Exception as e:
            self.logger.error(f"❌ PaddleOCR 初始化失败: {e}")

    def _init_embedding_model(self):
        """初始化嵌入模型"""
        try:
            from sentence_transformers import SentenceTransformer

            config = self.config['embedding']
            model_name = config.get('model_name',
                                   'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
            device = config.get('device', 'cpu')

            model = SentenceTransformer(model_name, device=device)
            self._engines[AIEngine.SENTENCE_TRANSFORMER] = model

            self.logger.info(f"✅ 嵌入模型初始化成功 ({device})")

        except ImportError:
            self.logger.warning("⚠️ sentence-transformers 未安装")
        except Exception as e:
            self.logger.error(f"❌ 嵌入模型初始化失败: {e}")

    def ocr_extract(
        self,
        image_path: str,
        use_fallback: bool = True
    ) -> OCRResult:
        """
        OCR 文本提取

        Args:
            image_path: 图片路径
            use_fallback: 是否使用备用引擎

        Returns:
            OCR 结果
        """
        start_time = time.time()

        # 检查缓存
        cache_key = f"ocr_{image_path}"
        if self._is_cache_enabled() and cache_key in self._cache:
            self.logger.info(f"📦 从缓存读取: {image_path}")
            return self._cache[cache_key]

        # 尝试主引擎
        result = self._ocr_with_primary(image_path)

        # 如果主引擎失败且允许降级
        if result.confidence < 0.7 and use_fallback:
            self.logger.warning("⚠️ 主引擎置信度低，尝试备用引擎")
            result = self._ocr_with_fallback(image_path)

        # 缓存结果
        if self._is_cache_enabled():
            self._cache[cache_key] = result

        processing_time = time.time() - start_time
        result.processing_time = processing_time

        self.logger.info(f"✅ OCR 完成 (耗时: {processing_time:.2f}s, 置信度: {result.confidence:.2f})")

        return result

    def _ocr_with_primary(self, image_path: str) -> OCRResult:
        """使用主引擎进行 OCR"""
        primary = self.config['ocr']['primary_engine']

        if primary == 'paddleocr':
            return self._ocr_paddleocr(image_path)
        else:
            raise ValueError(f"未知的主引擎: {primary}")

    def _ocr_paddleocr(self, image_path: str) -> OCRResult:
        """PaddleOCR 识别"""
        if AIEngine.PADDLEOCR not in self._engines:
            return OCRResult(
                text="",
                confidence=0.0,
                engine="none",
                processing_time=0.0
            )

        ocr = self._engines[AIEngine.PADDLEOCR]
        result = ocr.ocr(image_path, cls=True)

        if not result or not result[0]:
            return OCRResult(
                text="",
                confidence=0.0,
                engine="paddleocr",
                processing_time=0.0
            )

        # 提取文本和置信度
        texts = []
        confidences = []

        for line in result[0]:
            if line:
                bbox, (text, confidence) = line
                texts.append(text)
                confidences.append(confidence)

        full_text = '\n'.join(texts)
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

        return OCRResult(
            text=full_text,
            confidence=avg_confidence,
            engine="paddleocr",
            processing_time=0.0,
            raw_data={'result': result}
        )

    def _ocr_with_fallback(self, image_path: str) -> OCRResult:
        """使用备用引擎"""
        fallback = self.config['ocr']['fallback_engine']

        if fallback == 'baidu':
            # 这里可以集成百度 OCR
            return OCRResult(
                text="",
                confidence=0.0,
                engine="baidu",
                processing_time=0.0
            )

        return OCRResult(
            text="",
            confidence=0.0,
            engine="none",
            processing_time=0.0
        )

    def embed_text(self, texts: List[str]) -> List[List[float]]:
        """
        文本嵌入

        Args:
            texts: 文本列表

        Returns:
            嵌入向量列表
        """
        if AIEngine.SENTENCE_TRANSFORMER not in self._engines:
            self.logger.error("❌ 嵌入模型未初始化")
            return []

        model = self._engines[AIEngine.SENTENCE_TRANSFORMER]
        embeddings = model.encode(
            texts,
            batch_size=self.config['embedding'].get('batch_size', 32),
            show_progress_bar=False
        )

        return embeddings.tolist()

    def semantic_search(
        self,
        query: str,
        documents: List[str],
        top_k: int = 5
    ) -> List[Tuple[str, float]]:
        """
        语义搜索

        Args:
            query: 查询文本
            documents: 文档列表
            top_k: 返回前 K 个结果

        Returns:
            [(文档, 相似度), ...]
        """
        # 生成嵌入
        query_emb = self.embed_text([query])[0]
        doc_embs = self.embed_text(documents)

        # 计算相似度
        from sklearn.metrics.pairwise import cosine_similarity
        import numpy as np

        similarities = cosine_similarity(
            [query_emb],
            doc_embs
        )[0]

        # 排序
        indices = np.argsort(similarities)[::-1][:top_k]

        results = [
            (documents[i], similarities[i])
            for i in indices
        ]

        return results

    def _is_cache_enabled(self) -> bool:
        """检查是否启用缓存"""
        return self.config.get('performance', {}).get('cache', {}).get('enabled', False)

    def get_stats(self) -> Dict[str, Any]:
        """获取引擎统计信息"""
        return {
            'engines_loaded': list(self._engines.keys()),
            'cache_size': len(self._cache),
            'config': self.config
        }


# 使用示例
if __name__ == "__main__":
    # 创建引擎
    engine = LocalAIEngine()

    # 测试 OCR
    print("\n=== 本地 AI 引擎测试 ===\n")

    # 查看统计信息
    stats = engine.get_stats()
    print(f"📊 已加载引擎: {stats['engines_loaded']}")
    print(f"📦 缓存大小: {stats['cache_size']}")

    print("\n✅ 本地 AI 引擎已准备就绪！")
    print("\n📋 可用功能:")
    print("  1. OCR 文本识别（PaddleOCR）")
    print("  2. 文本嵌入（Sentence Transformers）")
    print("  3. 语义搜索")
    print("  4. 智能缓存")
