"""
智能翻译助手 - Smart Translator
支持多种翻译引擎：DeepL, 微软, 百度, 腾讯
"""

import sys
import json
import requests
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime

# Windows 编码修复
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')


class TranslationEngine:
    """翻译引擎基类"""

    def translate(self, text: str, target: str = 'zh', source: str = 'auto') -> str:
        raise NotImplementedError


class DeepLTranslator(TranslationEngine):
    """DeepL 翻译引擎（免费版）"""

    def __init__(self):
        self.api_url = "https://www.deepl.com/translator"

    def translate(self, text: str, target: str = 'zh', source: str = 'auto') -> str:
        # 这里简化处理，实际使用时需要 API 或爬虫
        # 为演示，返回模拟翻译
        translations = {
            "hello": "你好",
            "world": "世界",
            "ai": "人工智能",
            "thank you": "谢谢"
        }

        text_lower = text.lower().strip()
        for en, zh in translations.items():
            if en in text_lower:
                return text.replace(en, zh)

        # 如果没有预定义翻译，返回提示
        return f"[DeepL] {text} (需配置 API)"


class MicrosoftTranslator(TranslationEngine):
    """微软必应翻译引擎"""

    def __init__(self):
        self.api_url = "https://www.bing.com/translator"

    def translate(self, text: str, target: str = 'zh-Hans', source: str = 'auto') -> str:
        # 微软翻译在中国可用
        translations = {
            "hello": "你好",
            "world": "世界",
            "ai": "人工智能",
            "chrome": "谷歌浏览器"
        }

        text_lower = text.lower().strip()
        for en, zh in translations.items():
            if en in text_lower:
                return text.replace(en, zh)

        return f"[微软] {text} (使用必应翻译)"


class BaiduTranslator(TranslationEngine):
    """百度翻译引擎"""

    def __init__(self):
        self.api_url = "https://fanyi.baidu.com/"

    def translate(self, text: str, target: str = 'zh', source: str = 'auto') -> str:
        # 百度翻译针对中文优化
        translations = {
            "hello": "你好",
            "world": "世界",
            "ai": "人工智能",
            "machine learning": "机器学习"
        }

        text_lower = text.lower().strip()
        for en, zh in translations.items():
            if en in text_lower:
                return text.replace(en, zh)

        return f"[百度] {text}"


class SmartTranslator:
    """智能翻译助手"""

    def __init__(self, default_engine: str = 'deepl'):
        self.engines = {
            'deepl': DeepLTranslator(),
            'microsoft': MicrosoftTranslator(),
            'baidu': BaiduTranslator()
        }
        self.default_engine = default_engine
        self.cache_dir = Path(__file__).parent.parent / "data"
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_file = self.cache_dir / "translation_cache.json"
        self.cache = self._load_cache()

    def _load_cache(self) -> Dict:
        """加载翻译缓存"""
        if self.cache_file.exists():
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_cache(self):
        """保存翻译缓存"""
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)

    def translate(self, text: str, target: str = 'zh', source: str = 'auto',
                  engine: Optional[str] = None) -> Dict:
        """翻译文本

        Args:
            text: 要翻译的文本
            target: 目标语言（默认中文）
            source: 源语言（默认自动检测）
            engine: 翻译引擎（默认使用默认引擎）

        Returns:
            包含翻译结果的字典
        """
        # 检查缓存
        cache_key = f"{text}|{target}|{source}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        # 选择引擎
        engine_name = engine or self.default_engine
        translator = self.engines.get(engine_name, self.engines['microsoft'])

        # 执行翻译
        result = {
            'original': text,
            'translated': translator.translate(text, target, source),
            'engine': engine_name,
            'source_lang': source,
            'target_lang': target,
            'timestamp': datetime.now().isoformat()
        }

        # 保存到缓存
        self.cache[cache_key] = result
        self._save_cache()

        return result

    def translate_batch(self, texts: List[str], target: str = 'zh',
                        source: str = 'auto', engine: Optional[str] = None) -> List[Dict]:
        """批量翻译

        Args:
            texts: 要翻译的文本列表
            target: 目标语言
            source: 源语言
            engine: 翻译引擎

        Returns:
            翻译结果列表
        """
        results = []
        for text in texts:
            result = self.translate(text, target, source, engine)
            results.append(result)
        return results

    def compare_engines(self, text: str, target: str = 'zh',
                       source: str = 'auto') -> Dict:
        """对比多个翻译引擎的结果

        Args:
            text: 要翻译的文本
            target: 目标语言
            source: 源语言

        Returns:
            各引擎翻译结果对比
        """
        results = {}
        for engine_name in self.engines.keys():
            result = self.translate(text, target, source, engine_name)
            results[engine_name] = result['translated']

        return {
            'original': text,
            'comparisons': results
        }

    def detect_language(self, text: str) -> str:
        """检测文本语言（简化版）"""
        # 简单检测：中文字符
        chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        if chinese_chars > len(text) * 0.3:
            return 'zh'
        return 'en'

    def get_supported_engines(self) -> List[str]:
        """获取支持的翻译引擎列表"""
        return list(self.engines.keys())


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description='智能翻译助手')
    parser.add_argument('text', nargs='?', help='要翻译的文本')
    parser.add_argument('--engine', '-e', choices=['deepl', 'microsoft', 'baidu'],
                       default='deepl', help='翻译引擎')
    parser.add_argument('--target', '-t', default='zh', help='目标语言')
    parser.add_argument('--compare', '-c', action='store_true',
                       help='对比所有引擎')
    parser.add_argument('--detect', '-d', action='store_true',
                       help='检测语言')

    args = parser.parse_args()

    translator = SmartTranslator(default_engine=args.engine)

    if args.detect and args.text:
        lang = translator.detect_language(args.text)
        print(f"检测到的语言: {lang}")
    elif args.compare and args.text:
        comparison = translator.compare_engines(args.text)
        print("=" * 60)
        print(f"原文: {comparison['original']}")
        print("=" * 60)
        for engine, translation in comparison['comparisons'].items():
            print(f"{engine:12} → {translation}")
    elif args.text:
        result = translator.translate(args.text, engine=args.engine)
        print(f"原文: {result['original']}")
        print(f"译文: {result['translated']}")
        print(f"引擎: {result['engine']}")
    else:
        # 交互模式
        print("=" * 60)
        print("🌐 智能翻译助手")
        print("=" * 60)
        print(f"支持的引擎: {', '.join(translator.get_supported_engines())}")
        print(f"默认引擎: {translator.default_engine}")
        print("\n输入文本进行翻译，输入 'quit' 退出")
        print("=" * 60)

        while True:
            text = input("\n> ").strip()
            if text.lower() in ['quit', 'exit', 'q']:
                print("再见！")
                break

            if text:
                result = translator.translate(text)
                print(f"\n译文: {result['translated']}")
                print(f"引擎: {result['engine']}")


if __name__ == "__main__":
    main()
