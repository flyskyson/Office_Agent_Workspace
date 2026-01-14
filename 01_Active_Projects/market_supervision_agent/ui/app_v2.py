#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
市场监管智能体 v4.0 - 简化版 Streamlit UI

确保使用正确的 OCR 引擎适配器
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

# 导入核心模块 - 使用绝对导入避免缓存
from src.workflow import process_files

# 页面配置
st.set_page_config(
    page_title="市场监管智能体 v4.0",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义 CSS
st.markdown("""
<style>
    .stApp { background-color: #f5f5f5; }
    .main-header {
        background: linear-gradient(90deg, #1f77b4 0%, #17becf 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 5px;
        border-left: 5px solid #28a745;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 5px;
        border-left: 5px solid #dc3545;
    }
</style>
""", unsafe_allow_html=True)

# 标题
st.markdown("""
<div class="main-header">
    <h1>🏢 市场监管智能体 v4.0</h1>
    <p>自动化 OCR 识别和数据提取</p>
</div>
""", unsafe_allow_html=True)

# 侧边栏
with st.sidebar:
    st.title("⚙️ 功能选择")

    page = st.radio(
        "选择页面",
        ["📤 文件处理", "🗄️ 数据库管理", "📄 申请书生成"],
        label_visibility="collapsed"
    )

    st.divider()

    # OCR 引擎状态 - 添加详细调试
    st.markdown("**系统状态**")
    try:
        # 检查模块加载情况
        import sys
        ocr_modules = [m for m in sys.modules.keys() if 'ocr' in m.lower()]
        st.caption(f"已加载 {len(ocr_modules)} 个 OCR 相关模块")

        from src import create_ocr_engine
        ocr = create_ocr_engine()
        st.success(f"✅ OCR 引擎: {ocr.active_engine.upper()}")

        # 检查是否有 OCREngine 被意外加载
        if 'src.ocr_engine' in sys.modules:
            st.warning("⚠️ 检测到旧版 OCR 模块已加载")
        else:
            st.info("✓ 模块加载正常")

    except Exception as e:
        st.error(f"❌ OCR 引擎错误: {e}")
        import traceback
        st.error(traceback.format_exc())

    st.divider()

    # 使用说明
    st.markdown("""
    ### 📖 使用说明

    **文件处理页面：**
    1. 上传身份证、营业执照等图片
    2. 点击"开始处理"
    3. 查看 OCR 识别结果

    **支持的格式：** JPG, PNG, PDF
    **OCR 引擎：** 百度 OCR API
    """)

# ============ 文件处理页面 ============
if page == "📤 文件处理":
    st.header("📤 文件处理")
    st.markdown("上传文件进行自动 OCR 识别和数据提取")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("上传文件")

        uploaded_files = st.file_uploader(
            "选择文件",
            type=["jpg", "jpeg", "png", "pdf"],
            accept_multiple_files=True,
            help="支持身份证、营业执照等文件"
        )

        st.subheader("处理选项")
        skip_ocr = st.checkbox("跳过 OCR（测试模式）", value=False)
        auto_archive = st.checkbox("自动归档", value=True)

        if st.button("🚀 开始处理", type="primary", use_container_width=True):
            if not uploaded_files:
                st.warning("⚠️ 请先上传文件")
            else:
                with st.spinner("🔄 正在处理..."):
                    # 保存临时文件
                    temp_paths = []
                    try:
                        for uploaded_file in uploaded_files:
                            with tempfile.NamedTemporaryFile(
                                delete=False,
                                suffix=Path(uploaded_file.name).suffix
                            ) as tmp:
                                tmp.write(uploaded_file.getvalue())
                                temp_paths.append(tmp.name)

                        # 配置
                        config = {
                            "skip_ocr": skip_ocr,
                            "skip_archiving": not auto_archive
                        }

                        # 处理文件
                        result = process_files(temp_paths, config)

                        # 显示结果
                        st.success("✅ 处理完成！")

                        # 显示消息
                        for msg in result.get("messages", []):
                            if "成功" in msg:
                                st.success(msg)
                            elif "失败" in msg or "错误" in msg:
                                st.error(msg)
                            else:
                                st.info(msg)

                        # 显示提取的数据
                        extracted = result.get("extracted_data", {})
                        if extracted:
                            st.subheader("📋 提取的数据")

                            col_a, col_b = st.columns(2)
                            with col_a:
                                st.markdown("**基本信息**")
                                st.write(f"- 👤 姓名: `{extracted.get('operator_name', 'N/A')}`")
                                st.write(f"- 🆔 身份证: `{extracted.get('id_card', 'N/A')}`")
                                st.write(f"- 👫 性别: `{extracted.get('gender', 'N/A')}`")
                                st.write(f"- 🌏 民族: `{extracted.get('nation', 'N/A')}`")
                                st.write(f"- 🏠 地址: `{extracted.get('address', 'N/A')}`")

                            with col_b:
                                st.markdown("**经营信息**")
                                st.write(f"- 🏪 店名: `{extracted.get('business_name', 'N/A')}`")
                                st.write(f"- 📍 经营地址: `{extracted.get('business_address', 'N/A')}`")
                                st.write(f"- 📝 经营范围: `{extracted.get('business_scope', 'N/A')[:50]}...`" if extracted.get('business_scope') else "- 📝 经营范围: `N/A`")

                        # 显示错误
                        if result.get("error_message"):
                            st.error(f"❌ {result['error_message']}")

                    except Exception as e:
                        st.error(f"❌ 处理失败: {str(e)}")
                        import traceback
                        st.error(traceback.format_exc())

                    finally:
                        # 清理临时文件
                        for path in temp_paths:
                            try:
                                Path(path).unlink(missing_ok=True)
                            except:
                                pass

    with col2:
        st.subheader("💡 提示")
        st.info("""
        **支持的文件类型：**

        - 📇 身份证（正反面）
        - 📋 营业执照
        - 📄 租赁合同
        - 🏠 产权证明

        **OCR 识别内容：**
        - 姓名、身份证号
        - 性别、民族
        - 店名、地址
        - 经营范围
        """)

# ============ 数据库管理页面 ============
elif page == "🗄️ 数据库管理":
    st.header("🗄️ 数据库管理")

    from src.database_manager import DatabaseManager
    db = DatabaseManager()

    col1, col2 = st.columns([2, 1])

    with col1:
        keyword = st.text_input("🔍 搜索", placeholder="输入姓名、店名或身份证号")

    with col2:
        limit = st.number_input("显示数量", min_value=5, max_value=100, value=20)

    if keyword:
        operators = db.search_operators(keyword)
        st.caption(f"找到 {len(operators)} 条匹配记录")
    else:
        operators = db.list_operators(limit=limit)
        st.caption(f"共 {len(operators)} 条记录")

    if operators:
        st.dataframe(
            operators,
            column_config={
                "id": st.column_config.NumberColumn("ID", width="small"),
                "operator_name": st.column_config.TextColumn("姓名"),
                "id_card": st.column_config.TextColumn("身份证号"),
                "business_name": st.column_config.TextColumn("店名"),
                "phone": st.column_config.TextColumn("电话"),
                "created_at": st.column_config.DatetimeColumn("创建时间")
            },
            use_container_width=True
        )
    else:
        st.info("📭 暂无数据")

# ============ 申请书生成页面 ============
elif page == "📄 申请书生成":
    st.header("📄 申请书生成")

    from src.database_manager import DatabaseManager
    from src.application_generator import ApplicationGenerator

    db = DatabaseManager()
    generator = ApplicationGenerator()

    # 获取所有记录
    operators = db.list_operators(limit=100)

    if not operators:
        st.warning("⚠️ 数据库中暂无记录，请先处理文件")
    else:
        # 选择记录
        operator_dict = {f"{op['operator_name']} ({op['id_card']})": op for op in operators}

        selected = st.selectbox(
            "选择经营户",
            options=list(operator_dict.keys()),
            help="选择要生成申请书的经营户"
        )

        if selected:
            operator = operator_dict[selected]

            # 显示经营户信息
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("基本信息")
                st.write(f"**姓名:** {operator['operator_name']}")
                st.write(f"**身份证:** {operator['id_card']}")
                st.write(f"**性别:** {operator.get('gender', 'N/A')}")
                st.write(f"**民族:** {operator.get('nation', 'N/A')}")

            with col2:
                st.subheader("经营信息")
                st.write(f"**店名:** {operator.get('business_name', 'N/A')}")
                st.write(f"**地址:** {operator.get('business_address', 'N/A')}")

            # 生成按钮
            if st.button("📄 生成申请书", type="primary"):
                with st.spinner("正在生成..."):
                    try:
                        output_path = generator.generate_application(
                            operator_data=operator,
                            output_dir="output"
                        )
                        st.success(f"✅ 申请书已生成: `{output_path}`")

                        # 提供下载
                        with open(output_path, 'rb') as f:
                            st.download_button(
                                label="💾 下载申请书",
                                data=f,
                                file_name=Path(output_path).name,
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            )
                    except Exception as e:
                        st.error(f"❌ 生成失败: {str(e)}")

# 页脚
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.8rem;'>
    <p>市场监管智能体 v4.0 | 使用百度 OCR API | © 2026</p>
</div>
""", unsafe_allow_html=True)
