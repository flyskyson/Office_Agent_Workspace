"""
市场监管智能体 v4.0 - Streamlit Web界面

功能：
- 上传文件进行OCR识别
- 查看和管理经营户数据库
- 生成申请书
- 文件归档管理
"""

import sys
from pathlib import Path
import streamlit as st
import pandas as pd
from datetime import datetime

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 导入核心模块
from src.workflow import process_files, quick_process
from src.database_manager import DatabaseManager
from src.file_archiver import FileArchiver
from src.application_generator import ApplicationGenerator

# 页面配置
st.set_page_config(
    page_title="市场监管智能体 v4.0",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化session state
if "db" not in st.session_state:
    st.session_state.db = DatabaseManager()
if "archiver" not in st.session_state:
    st.session_state.archiver = FileArchiver()
if "generator" not in st.session_state:
    st.session_state.generator = ApplicationGenerator()


# ============ 侧边栏 ============

def render_sidebar():
    """渲染侧边栏"""
    with st.sidebar:
        st.title("🏢 市场监管智能体")
        st.caption("v4.0 - 自动化申请处理")

        st.divider()

        # 导航菜单
        page = st.radio(
            "选择功能",
            ["📤 文件处理", "🗄️ 数据库管理", "📄 申请书生成", "📁 归档管理"],
            label_visibility="collapsed"
        )

        st.divider()

        # 统计信息
        stats = st.session_state.db.get_statistics()
        st.metric("总记录数", stats["total_operators"])
        st.metric("本月新增", stats["this_month_new"])

        return page


# ============ 主页面 ============

def main():
    """主函数"""
    page = render_sidebar()

    if page == "📤 文件处理":
        page_file_processing()
    elif page == "🗄️ 数据库管理":
        page_database_management()
    elif page == "📄 申请书生成":
        page_application_generation()
    elif page == "📁 归档管理":
        page_archive_management()


# ============ 文件处理页面 ============

def page_file_processing():
    """文件处理页面"""
    st.header("📤 文件处理")
    st.caption("上传文件进行自动OCR识别和数据提取")

    # 创建两列布局
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("上传文件")

        # 文件上传
        uploaded_files = st.file_uploader(
            "选择要上传的文件",
            type=["jpg", "jpeg", "png", "pdf"],
            accept_multiple_files=True,
            help="支持上传身份证、营业执照、租赁合同等文件"
        )

        # 配置选项
        st.subheader("处理选项")
        skip_ocr = st.checkbox("跳过OCR识别（测试模式）", value=False)
        auto_archive = st.checkbox("自动归档文件", value=True)
        auto_clean = st.checkbox("自动清理桌面", value=False)
        desktop_path = st.text_input("桌面路径", "")

        # 处理按钮
        if st.button("🚀 开始处理", type="primary", use_container_width=True):
            if uploaded_files:
                process_uploaded_files(uploaded_files, skip_ocr, auto_archive, auto_clean, desktop_path)
            else:
                st.warning("请先上传文件")

    with col2:
        st.subheader("处理结果")

        # 显示处理结果
        if "processing_result" in st.session_state:
            result = st.session_state.processing_result

            # 显示消息
            for msg in result.get("messages", []):
                st.info(msg)

            # 显示提取的数据
            if result.get("extracted_data"):
                st.success("✅ 数据提取成功！")
                data = result["extracted_data"]

                # 使用expander显示详细信息
                with st.expander("查看提取的数据", expanded=True):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.write("**基本信息**")
                        st.write(f"- 姓名: {data.get('operator_name', 'N/A')}")
                        st.write(f"- 身份证: {data.get('id_card', 'N/A')}")
                        st.write(f"- 性别: {data.get('gender', 'N/A')}")
                        st.write(f"- 民族: {data.get('nation', 'N/A')}")

                    with col_b:
                        st.write("**经营信息**")
                        st.write(f"- 店名: {data.get('business_name', 'N/A')}")
                        st.write(f"- 地址: {data.get('business_address', 'N/A')}")
                        st.write(f"- 范围: {data.get('business_scope', 'N/A')}")

            # 显示错误
            if result.get("error_message"):
                st.error(f"❌ 错误: {result['error_message']}")
        else:
            st.info("👈 上传文件后点击处理按钮")


def process_uploaded_files(uploaded_files, skip_ocr, auto_archive, auto_clean, desktop_path):
    """处理上传的文件"""
    # 保存临时文件
    import tempfile
    temp_paths = []

    with st.spinner("正在处理文件..."):
        for file in uploaded_files:
            # 保存到临时目录
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.name).suffix) as tmp:
                tmp.write(file.getvalue())
                temp_paths.append(tmp.name)

        try:
            # 处理文件
            config = {
                "skip_ocr": skip_ocr,
                "skip_archiving": not auto_archive,
                "auto_clean_desktop": auto_clean,
                "desktop_path": desktop_path
            }

            result = process_files(temp_paths, config, desktop_path)
            st.session_state.processing_result = result

        finally:
            # 清理临时文件
            for path in temp_paths:
                try:
                    Path(path).unlink()
                except:
                    pass


# ============ 数据库管理页面 ============

def page_database_management():
    """数据库管理页面"""
    st.header("🗄️ 数据库管理")
    st.caption("查看和管理经营户档案")

    # 操作栏
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        keyword = st.text_input("搜索经营户", placeholder="输入姓名、店名或身份证号")

    with col2:
        limit = st.number_input("显示数量", min_value=10, max_value=100, value=20)

    with col3:
        st.write("")
        if st.button("🔍 搜索", use_container_width=True):
            st.rerun()

    # 搜索或列表
    if keyword:
        operators = st.session_state.db.search_operators(keyword)
        st.caption(f"找到 {len(operators)} 条匹配记录")
    else:
        operators = st.session_state.db.list_operators(limit=limit)
        st.caption(f"共 {len(operators)} 条记录")

    if not operators:
        st.info("没有找到记录")
        return

    # 显示数据表格
    df = pd.DataFrame(operators)
    display_columns = ["id", "operator_name", "business_name", "id_card", "phone", "business_address", "created_at"]
    df = df[display_columns]

    # 重命名列
    df.columns = ["ID", "姓名", "店名", "身份证", "电话", "地址", "创建时间"]

    st.dataframe(df, use_container_width=True, hide_index=True)

    # 详细信息
    st.subheader("记录详情")
    selected_id = st.selectbox(
        "选择记录查看详情",
        options=[op["id"] for op in operators],
        format_func=lambda x: f"#{x} - {next(op['operator_name'] for op in operators if op['id'] == x)}"
    )

    if selected_id:
        operator = st.session_state.db.get_operator_by_id(selected_id)
        if operator:
            display_operator_details(operator)


def display_operator_details(operator):
    """显示经营户详细信息"""
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("基本信息")
        st.write(f"**姓名:** {operator.get('operator_name', 'N/A')}")
        st.write(f"**身份证:** {operator.get('id_card', 'N/A')}")
        st.write(f"**性别:** {operator.get('gender', 'N/A')}")
        st.write(f"**民族:** {operator.get('nation', 'N/A')}")
        st.write(f"**电话:** {operator.get('phone', 'N/A')}")
        st.write(f"**邮箱:** {operator.get('email', 'N/A')}")

    with col2:
        st.subheader("经营信息")
        st.write(f"**店名:** {operator.get('business_name', 'N/A')}")
        st.write(f"**地址:** {operator.get('business_address', 'N/A')}")
        st.write(f"**范围:** {operator.get('business_scope', 'N/A')}")
        st.write(f"**信用代码:** {operator.get('credit_code', 'N/A')}")
        st.write(f"**房东:** {operator.get('property_owner', 'N/A')}")

    st.subheader("文件信息")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"**身份证正面:** {operator.get('id_card_front_path', 'N/A')}")
        st.write(f"**身份证反面:** {operator.get('id_card_back_path', 'N/A')}")
    with col2:
        st.write(f"**营业执照:** {operator.get('business_license_path', 'N/A')}")
        st.write(f"**租赁合同:** {operator.get('lease_contract_path', 'N/A')}")
    with col3:
        st.write(f"**产权证明:** {operator.get('property_cert_path', 'N/A')}")
        st.write(f"**归档路径:** {operator.get('archive_path', 'N/A')}")

    # 操作按钮
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📄 生成申请书", type="primary"):
            st.session_state.selected_operator_id = operator["id"]
            st.switch_to("📄 申请书生成")
    with col2:
        if st.button("✏️ 编辑记录"):
            st.info("编辑功能开发中...")
    with col3:
        if st.button("🗑️ 删除记录", type="secondary"):
            if st.session_state.db.delete_operator(operator["id_card"]):
                st.success("记录已删除")
                st.rerun()


# ============ 申请书生成页面 ============

def page_application_generation():
    """申请书生成页面"""
    st.header("📄 申请书生成")
    st.caption("从数据库生成申请书文档")

    # 选择模板
    templates = st.session_state.generator.list_templates()
    if templates:
        template_names = [t["name"] for t in templates]
        selected_template = st.selectbox("选择模板", template_names)
    else:
        st.warning("没有找到模板文件")
        selected_template = None

    # 选择记录
    operators = st.session_state.db.list_operators(limit=100)
    if not operators:
        st.info("数据库中没有记录")
        return

    operator_options = {
        f"{op['operator_name']} - {op.get('business_name', 'N/A')}": op
        for op in operators
    }

    selected_option = st.selectbox("选择经营户", list(operator_options.keys()))
    selected_operator = operator_options[selected_option]

    # 显示选中记录的信息
    if selected_operator:
        with st.expander("查看记录信息", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**姓名:** {selected_operator.get('operator_name')}")
                st.write(f"**身份证:** {selected_operator.get('id_card')}")
            with col2:
                st.write(f"**店名:** {selected_operator.get('business_name', 'N/A')}")
                st.write(f"**地址:** {selected_operator.get('business_address', 'N/A')}")

    # 生成按钮
    if st.button("📄 生成申请书", type="primary", use_container_width=True):
        if selected_template and selected_operator:
            with st.spinner("正在生成申请书..."):
                try:
                    output_path = st.session_state.generator.generate_application(
                        selected_operator,
                        selected_template
                    )

                    st.success(f"✅ 申请书生成成功！")
                    st.info(f"保存路径: `{output_path}`")

                    # 提供下载链接
                    with open(output_path, "rb") as f:
                        st.download_button(
                            label="⬇️ 下载文档",
                            data=f,
                            file_name=Path(output_path).name,
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )

                except Exception as e:
                    st.error(f"❌ 生成失败: {str(e)}")


# ============ 归档管理页面 ============

def page_archive_management():
    """归档管理页面"""
    st.header("📁 归档管理")
    st.caption("查看和管理文件归档")

    # 统计信息
    stats = st.session_state.archiver.get_storage_stats()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("归档数量", stats["total_archives"])
    with col2:
        st.metric("文件数量", stats["total_files"])
    with col3:
        st.metric("总大小", f'{stats["total_size_mb"]} MB')

    st.divider()

    # 列出归档
    archives = st.session_state.archiver.list_archives()

    if not archives:
        st.info("没有归档记录")
        return

    # 显示归档列表
    for archive in archives:
        with st.expander(f"📂 {archive['name']} ({archive['total_files']} 个文件)"):
            st.write(f"**路径:** `{archive['path']}`")

            # 显示分类统计
            for category, count in archive["categories"].items():
                if count > 0:
                    st.write(f"- **{category}:** {count} 个文件")


# ============ 运行 ============

if __name__ == "__main__":
    main()
