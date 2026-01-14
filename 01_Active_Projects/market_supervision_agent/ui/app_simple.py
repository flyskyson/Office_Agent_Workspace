#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
市场监管智能体 v4.0 - 简化版 UI（测试版）
"""

import sys
import os
from pathlib import Path

# 确保项目根目录在路径最前面
project_root = Path(__file__).parent.parent
project_root_str = str(project_root)
if project_root_str in sys.path:
    sys.path.remove(project_root_str)
sys.path.insert(0, project_root_str)

import streamlit as st
import tempfile
import shutil

# 页面配置
st.set_page_config(
    page_title="市场监管智能体 v4.0",
    page_icon="🏢",
    layout="wide"
)

# 标题
st.title("🏢 市场监管智能体 v4.0")
st.markdown("---")

# 侧边栏
with st.sidebar:
    st.title("⚙️ 功能")
    page = st.radio("选择", ["文件处理", "数据库", "生成"], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("**OCR 引擎状态**")

    # 检查 OCR 引擎
    try:
        import sys as sys_check
        if 'src.ocr_engine' in sys_check.modules:
            st.warning("⚠️ 旧版模块已加载")
        else:
            st.info("✓ 模块正常")

        from src import create_ocr_engine
        ocr = create_ocr_engine()
        st.success(f"✅ 引擎: {ocr.active_engine}")
    except Exception as e:
        st.error(f"❌ {e}")

# 主页面
if page == "文件处理":
    st.header("📤 文件处理")

    uploaded_files = st.file_uploader(
        "上传文件",
        type=["jpg", "jpeg", "png", "pdf"],
        accept_multiple_files=True
    )

    if st.button("🚀 开始处理", type="primary"):
        if uploaded_files:
            with st.spinner("处理中..."):
                temp_paths = []
                try:
                    # 保存临时文件
                    for f in uploaded_files:
                        with tempfile.NamedTemporaryFile(
                            delete=False,
                            suffix=Path(f.name).suffix
                        ) as tmp:
                            tmp.write(f.getvalue())
                            temp_paths.append(tmp.name)

                    # 处理
                    from src.workflow import process_files
                    config = {"skip_ocr": False, "skip_archiving": True}
                    result = process_files(temp_paths, config)

                    # 显示结果
                    st.success("✅ 处理完成")
                    for msg in result.get("messages", []):
                        if "成功" in msg:
                            st.success(msg)
                        elif "失败" in msg:
                            st.error(msg)

                    # 显示提取的数据
                    data = result.get("extracted_data", {})
                    if data:
                        st.json(data)

                except Exception as e:
                    st.error(f"❌ 错误: {e}")
                    import traceback
                    st.error(traceback.format_exc())
                finally:
                    for p in temp_paths:
                        try:
                            Path(p).unlink()
                        except:
                            pass
        else:
            st.warning("请先上传文件")

elif page == "数据库":
    st.header("🗄️ 数据库")
    from src.database_manager import DatabaseManager
    db = DatabaseManager()

    operators = db.list_operators(limit=20)
    if operators:
        st.dataframe(operators)
    else:
        st.info("暂无数据")

elif page == "生成":
    st.header("📄 申请书生成")
    st.info("功能开发中...")
