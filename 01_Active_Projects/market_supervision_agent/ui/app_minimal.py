import streamlit as st
import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

st.title("测试 UI")

st.write("系统状态:")
try:
    from src import create_ocr_engine
    ocr = create_ocr_engine()
    st.success(f"OCR 引擎: {ocr.active_engine}")
except Exception as e:
    st.error(f"错误: {e}")

if st.button("测试 OCR"):
    st.write("按钮被点击了")
