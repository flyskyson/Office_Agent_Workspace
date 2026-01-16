#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自定义 SQLite MCP 服务器 - 用于市场监管智能体项目
"""

from mcp.server.fastmcp import FastMCP
import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional

# 创建 FastMCP 实例
mcp = FastMCP("Market Supervision SQLite Server")

# 数据库路径（使用绝对路径）
DB_PATH = Path(r"C:\Users\flyskyson\Office_Agent_Workspace\01_Active_Projects\market_supervision_agent\data\operators_database.db")


def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


@mcp.tool()
def list_tables() -> List[str]:
    """列出数据库中的所有表"""
    conn = get_db_connection()
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    )
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables


@mcp.tool()
def get_table_schema(table_name: str) -> List[Dict[str, Any]]:
    """获取表结构

    Args:
        table_name: 表名
    """
    conn = get_db_connection()
    cursor = conn.execute(f"PRAGMA table_info({table_name})")
    columns = []
    for row in cursor.fetchall():
        columns.append({
            "name": row[1],
            "type": row[2],
            "not_null": bool(row[3]),
            "default_value": row[4],
            "primary_key": bool(row[5])
        })
    conn.close()
    return columns


@mcp.tool()
def query_operators(
    limit: int = 20,
    status: str = "active",
    offset: int = 0
) -> List[Dict[str, Any]]:
    """查询经营户记录

    Args:
        limit: 返回记录数
        status: 状态过滤 (active, deleted)
        offset: 偏移量
    """
    conn = get_db_connection()
    cursor = conn.execute("""
        SELECT * FROM operators
        WHERE status = ?
        ORDER BY updated_at DESC
        LIMIT ? OFFSET ?
    """, (status, limit, offset))

    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results


@mcp.tool()
def search_operators(keyword: str) -> List[Dict[str, Any]]:
    """搜索经营户记录

    Args:
        keyword: 搜索关键词（匹配姓名、店名、身份证号、手机号）
    """
    conn = get_db_connection()
    cursor = conn.execute("""
        SELECT * FROM operators
        WHERE status = 'active'
        AND (
            operator_name LIKE ?
            OR business_name LIKE ?
            OR id_card LIKE ?
            OR phone LIKE ?
        )
        ORDER BY updated_at DESC
    """, (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))

    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results


@mcp.tool()
def get_operator_by_id(operator_id: int) -> Optional[Dict[str, Any]]:
    """根据ID获取经营户记录

    Args:
        operator_id: 记录ID
    """
    conn = get_db_connection()
    cursor = conn.execute(
        "SELECT * FROM operators WHERE id = ?",
        (operator_id,)
    )
    row = cursor.fetchone()
    conn.close()

    if row:
        return dict(row)
    return None


@mcp.tool()
def get_operator_by_id_card(id_card: str) -> Optional[Dict[str, Any]]:
    """根据身份证号获取经营户记录

    Args:
        id_card: 身份证号
    """
    conn = get_db_connection()
    cursor = conn.execute(
        "SELECT * FROM operators WHERE id_card = ?",
        (id_card,)
    )
    row = cursor.fetchone()
    conn.close()

    if row:
        return dict(row)
    return None


@mcp.tool()
def get_statistics() -> Dict[str, Any]:
    """获取数据库统计信息"""
    conn = get_db_connection()

    # 总记录数
    total = conn.execute(
        "SELECT COUNT(*) FROM operators WHERE status = 'active'"
    ).fetchone()[0]

    # 本月新增
    this_month = conn.execute("""
        SELECT COUNT(*) FROM operators
        WHERE status = 'active'
        AND strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now')
    """).fetchone()[0]

    # 有营业执照的数量
    has_license = conn.execute("""
        SELECT COUNT(*) FROM operators
        WHERE status = 'active' AND business_license_path IS NOT NULL
    """).fetchone()[0]

    conn.close()

    return {
        "total_operators": total,
        "this_month_new": this_month,
        "has_business_license": has_license,
    }


@mcp.tool()
def execute_sql(query: str) -> List[Dict[str, Any]]:
    """执行自定义 SQL 查询（只读）

    Args:
        query: SQL 查询语句（仅支持 SELECT）
    """
    # 安全检查：只允许 SELECT 语句
    query = query.strip()
    if not query.upper().startswith('SELECT'):
        raise ValueError("只允许执行 SELECT 查询")

    conn = get_db_connection()
    try:
        cursor = conn.execute(query)
        results = [dict(row) for row in cursor.fetchall()]
        return results
    except Exception as e:
        raise Exception(f"查询失败: {str(e)}")
    finally:
        conn.close()


@mcp.resource("sqlite://tables")
def list_tables_resource() -> str:
    """列出所有表（资源形式）"""
    tables = list_tables()
    return f"数据库中的表: {', '.join(tables)}"


@mcp.resource("sqlite://schema/{table_name}")
def table_schema_resource(table_name: str) -> str:
    """获取表结构（资源形式）"""
    schema = get_table_schema(table_name)
    lines = [f"表: {table_name}"]
    for col in schema:
        lines.append(f"  - {col['name']}: {col['type']}")
    return '\n'.join(lines)


if __name__ == "__main__":
    # 运行 MCP 服务器
    mcp.run()
