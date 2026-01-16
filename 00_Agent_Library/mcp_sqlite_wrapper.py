#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP SQLite 服务器 - 自定义实现
为 Office Agent Workspace 提供统一的数据库访问接口

作者: Claude Code
日期: 2026-01-16
版本: 1.0.0
"""

import sys
import json
import sqlite3
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Windows 终端编码修复
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass


# ============================================================================
# MCP SQLite 服务器实现
# ============================================================================

class MCPSqliteServer:
    """
    MCP SQLite 服务器 - 为 Office Agent Workspace 提供数据库服务

    功能:
    1. 统一数据库访问接口
    2. 安全的 SQL 查询执行
    3. 多数据库支持
    4. 自动建表和迁移
    5. 事务管理
    """

    def __init__(self, base_db_path: str = None):
        """
        初始化 MCP SQLite 服务器

        参数:
            base_db_path: 数据库基础路径
        """
        if base_db_path is None:
            # 默认使用工作区数据目录
            workspace_root = Path(__file__).parent.parent
            base_db_path = workspace_root / "04_Data_&_Resources"

        self.base_db_path = Path(base_db_path)
        self.base_db_path.mkdir(parents=True, exist_ok=True)

        # 数据库连接池
        self.connections: Dict[str, sqlite3.Connection] = {}

        # 支持的数据库
        self.databases = {
            "office_agent": "office_agent.db",           # 主数据库
            "market_supervision": "operators_database.db",  # 市场监管
            "memory": "memory_store.db",                 # 记忆助手
        }

        print(f"[INFO] MCP SQLite 服务器初始化完成")
        print(f"[INFO] 数据库路径: {self.base_db_path}")

    def get_db_path(self, db_name: str) -> Path:
        """获取数据库文件路径"""
        if db_name in self.databases:
            return self.base_db_path / self.databases[db_name]
        return self.base_db_path / f"{db_name}.db"

    def get_connection(self, db_name: str = "office_agent") -> sqlite3.Connection:
        """获取数据库连接（连接池）"""
        if db_name not in self.connections:
            db_path = self.get_db_path(db_name)
            conn = sqlite3.connect(str(db_path), check_same_thread=False)
            conn.row_factory = sqlite3.Row  # 返回字典格式
            self.connections[db_name] = conn

        return self.connections[db_name]

    def execute_query(
        self,
        query: str,
        params: tuple = (),
        db_name: str = "office_agent"
    ) -> List[Dict[str, Any]]:
        """
        执行查询并返回结果

        参数:
            query: SQL 查询语句
            params: 查询参数
            db_name: 数据库名称

        返回:
            查询结果列表
        """
        conn = self.get_connection(db_name)
        cursor = conn.execute(query, params)

        # 转换为字典列表
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return results

    def execute_update(
        self,
        query: str,
        params: tuple = (),
        db_name: str = "office_agent"
    ) -> int:
        """
        执行更新操作

        参数:
            query: SQL 语句
            params: 参数
            db_name: 数据库名称

        返回:
            影响的行数
        """
        conn = self.get_connection(db_name)
        cursor = conn.execute(query, params)
        conn.commit()
        return cursor.rowcount

    def list_tables(self, db_name: str = "office_agent") -> List[str]:
        """列出数据库中的所有表"""
        query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        results = self.execute_query(query, db_name=db_name)
        return [r['name'] for r in results]

    def describe_table(
        self,
        table_name: str,
        db_name: str = "office_agent"
    ) -> List[Dict[str, Any]]:
        """获取表结构"""
        query = f"PRAGMA table_info({table_name})"
        return self.execute_query(query, db_name=db_name)

    def table_exists(
        self,
        table_name: str,
        db_name: str = "office_agent"
    ) -> bool:
        """检查表是否存在"""
        tables = self.list_tables(db_name)
        return table_name in tables

    # ========================================================================
    # 市场监管智能体专用方法
    # ========================================================================

    def init_market_supervision_db(self):
        """初始化市场监管数据库"""
        db_name = "market_supervision"
        conn = self.get_connection(db_name)

        # 创建经营户表
        conn.execute('''
            CREATE TABLE IF NOT EXISTS operators (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                -- 基本信息
                operator_name TEXT NOT NULL,
                id_card TEXT UNIQUE NOT NULL,
                phone TEXT,
                email TEXT,
                gender TEXT,
                nation TEXT,
                address TEXT,

                -- 经营信息
                business_name TEXT,
                business_address TEXT,
                business_scope TEXT,
                credit_code TEXT,

                -- 场所信息
                property_owner TEXT,
                lease_start DATE,
                lease_end DATE,
                rent_amount TEXT,

                -- 文件路径
                id_card_front_path TEXT,
                id_card_back_path TEXT,
                business_license_path TEXT,
                lease_contract_path TEXT,
                property_cert_path TEXT,

                -- 归档信息
                archive_path TEXT,

                -- 状态
                status TEXT DEFAULT 'active',

                -- 元数据（JSON格式）
                metadata TEXT
            )
        ''')

        # 创建索引
        conn.execute('CREATE INDEX IF NOT EXISTS idx_id_card ON operators(id_card)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_business_name ON operators(business_name)')

        conn.commit()
        print(f"[INFO] 市场监管数据库初始化完成")

    def get_operator_by_id_card(self, id_card: str) -> Optional[Dict[str, Any]]:
        """根据身份证号查询经营户"""
        query = "SELECT * FROM operators WHERE id_card = ?"
        results = self.execute_query(query, (id_card,), "market_supervision")
        return results[0] if results else None

    def list_operators(
        self,
        limit: int = 100,
        offset: int = 0,
        status: str = None
    ) -> List[Dict[str, Any]]:
        """列出经营户"""
        if status:
            query = "SELECT * FROM operators WHERE status = ? ORDER BY id DESC LIMIT ? OFFSET ?"
            return self.execute_query(query, (status, limit, offset), "market_supervision")
        else:
            query = "SELECT * FROM operators ORDER BY id DESC LIMIT ? OFFSET ?"
            return self.execute_query(query, (limit, offset), "market_supervision")

    # ========================================================================
    # 记忆助手专用方法
    # ========================================================================

    def init_memory_db(self):
        """初始化记忆数据库"""
        db_name = "memory"
        conn = self.get_connection(db_name)

        # 创建笔记表
        conn.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                title TEXT NOT NULL,
                content TEXT,
                tags TEXT,
                category TEXT,
                importance INTEGER DEFAULT 0,

                -- 向量相关信息
                embedding_id TEXT,

                -- 复习信息
                review_count INTEGER DEFAULT 0,
                last_reviewed_at TIMESTAMP,
                next_review_at TIMESTAMP,

                -- 状态
                archived BOOLEAN DEFAULT 0
            )
        ''')

        conn.commit()
        print(f"[INFO] 记忆数据库初始化完成")

    def add_note(
        self,
        title: str,
        content: str,
        tags: str = None,
        category: str = None
    ) -> int:
        """添加笔记"""
        query = '''
            INSERT INTO notes (title, content, tags, category)
            VALUES (?, ?, ?, ?)
        '''
        conn = self.get_connection("memory")
        cursor = conn.execute(query, (title, content, tags, category))
        conn.commit()
        return cursor.lastrowid

    def search_notes(self, keyword: str) -> List[Dict[str, Any]]:
        """搜索笔记"""
        query = '''
            SELECT * FROM notes
            WHERE title LIKE ? OR content LIKE ?
            AND archived = 0
            ORDER BY created_at DESC
        '''
        pattern = f"%{keyword}%"
        return self.execute_query(query, (pattern, pattern), "memory")

    # ========================================================================
    # 通用统计方法
    # ========================================================================

    def get_database_stats(self, db_name: str) -> Dict[str, Any]:
        """获取数据库统计信息"""
        tables = self.list_tables(db_name)
        stats = {
            "database": db_name,
            "tables": [],
            "total_tables": len(tables)
        }

        for table in tables:
            count_query = f"SELECT COUNT(*) as count FROM {table}"
            result = self.execute_query(count_query, db_name=db_name)
            stats["tables"].append({
                "name": table,
                "rows": result[0]["count"]
            })

        return stats

    def close_all(self):
        """关闭所有数据库连接"""
        for conn in self.connections.values():
            conn.close()
        self.connections.clear()
        print("[INFO] 所有数据库连接已关闭")


# ============================================================================
# MCP 协议接口（简化版）
# ============================================================================

class MCPSqliteProtocol:
    """
    MCP 协议接口 - 提供 JSON-RPC 2.0 接口
    """

    def __init__(self):
        self.server = MCPSqliteServer()

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理 MCP 请求

        参数:
            request: JSON-RPC 2.0 请求

        返回:
            JSON-RPC 2.0 响应
        """
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")

        try:
            # 路由到对应的处理方法
            if method == "tools/list":
                result = self.list_tools()
            elif method == "tools/call":
                result = self.call_tool(params.get("name"), params.get("arguments", {}))
            elif method == "resources/list":
                result = self.list_resources()
            elif method == "resources/read":
                result = self.read_resource(params.get("uri"))
            else:
                raise ValueError(f"未知方法: {method}")

            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }

        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -1,
                    "message": str(e)
                }
            }

    def list_tools(self) -> Dict[str, Any]:
        """列出可用的工具"""
        return {
            "tools": [
                {
                    "name": "execute_query",
                    "description": "执行 SQL 查询",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"},
                            "db_name": {"type": "string", "default": "office_agent"}
                        }
                    }
                },
                {
                    "name": "list_tables",
                    "description": "列出所有表",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "db_name": {"type": "string", "default": "office_agent"}
                        }
                    }
                },
                {
                    "name": "get_operator_by_id_card",
                    "description": "查询经营户信息",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "id_card": {"type": "string"}
                        }
                    }
                },
                {
                    "name": "add_note",
                    "description": "添加笔记",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "content": {"type": "string"},
                            "tags": {"type": "string"},
                            "category": {"type": "string"}
                        }
                    }
                }
            ]
        }

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """调用工具"""
        if name == "execute_query":
            return self.server.execute_query(
                arguments.get("query"),
                arguments.get("params", ()),
                arguments.get("db_name", "office_agent")
            )
        elif name == "list_tables":
            return {"tables": self.server.list_tables(arguments.get("db_name", "office_agent"))}
        elif name == "get_operator_by_id_card":
            return self.server.get_operator_by_id_card(arguments["id_card"])
        elif name == "add_note":
            note_id = self.server.add_note(
                arguments["title"],
                arguments.get("content", ""),
                arguments.get("tags"),
                arguments.get("category")
            )
            return {"note_id": note_id, "status": "created"}
        else:
            raise ValueError(f"未知工具: {name}")

    def list_resources(self) -> Dict[str, Any]:
        """列出可用资源"""
        return {
            "resources": [
                {
                    "uri": "db:///office_agent/stats",
                    "name": "数据库统计",
                    "description": "获取所有数据库的统计信息",
                    "mimeType": "application/json"
                },
                {
                    "uri": "db:///market_supervision/operators",
                    "name": "经营户列表",
                    "description": "市场监管 - 经营户数据",
                    "mimeType": "application/json"
                }
            ]
        }

    def read_resource(self, uri: str) -> Dict[str, Any]:
        """读取资源"""
        if uri == "db:///office_agent/stats":
            return {
                "blob": json.dumps({
                    "office_agent": self.server.get_database_stats("office_agent"),
                    "market_supervision": self.server.get_database_stats("market_supervision"),
                    "memory": self.server.get_database_stats("memory")
                }, ensure_ascii=False)
            }
        elif uri == "db:///market_supervision/operators":
            operators = self.server.list_operators(limit=50)
            return {
                "blob": json.dumps(operators, ensure_ascii=False, default=str)
            }
        else:
            raise ValueError(f"未知资源: {uri}")


# ============================================================================
# 命令行接口
# ============================================================================

def main():
    """主函数 - 提供命令行接口"""
    print("=" * 60)
    print("MCP SQLite 服务器 - Office Agent Workspace")
    print("=" * 60)

    server = MCPSqliteServer()

    # 初始化数据库
    print("\n[1/3] 初始化数据库...")
    server.init_market_supervision_db()
    server.init_memory_db()

    # 显示统计信息
    print("\n[2/3] 数据库统计...")
    for db_name in ["office_agent", "market_supervision", "memory"]:
        try:
            stats = server.get_database_stats(db_name)
            print(f"\n  📊 {db_name}:")
            print(f"     表数量: {stats['total_tables']}")
            for table in stats["tables"]:
                print(f"     - {table['name']}: {table['rows']} 行")
        except Exception as e:
            print(f"     ⚠️  {db_name}: {e}")

    # 交互式查询
    print("\n[3/3] 交互式查询 (输入 'quit' 退出)")
    protocol = MCPSqliteProtocol()

    while True:
        try:
            user_input = input("\n> ").strip()

            if user_input.lower() in ['quit', 'exit', 'q']:
                break

            # 简单命令解析
            if user_input.startswith("SELECT ") or user_input.startswith("select "):
                results = server.execute_query(user_input)
                print(f"✅ 查询返回 {len(results)} 行")
                for i, row in enumerate(results[:5], 1):
                    print(f"  [{i}] {row}")
                if len(results) > 5:
                    print(f"  ... 还有 {len(results) - 5} 行")

            elif user_input == "tables":
                tables = server.list_tables()
                print(f"✅ 表列表: {', '.join(tables)}")

            elif user_input == "stats":
                stats = server.get_database_stats("office_agent")
                print(json.dumps(stats, ensure_ascii=False, indent=2))

            elif user_input == "operators":
                operators = server.list_operators(limit=10)
                print(f"✅ 最近 10 条经营户记录:")
                for op in operators:
                    print(f"  - {op['operator_name']} ({op['business_name']})")

            else:
                print("❓ 未知命令")
                print("   可用命令: SELECT ..., tables, stats, operators, quit")

        except KeyboardInterrupt:
            print("\n\n👋 再见!")
            break
        except Exception as e:
            print(f"❌ 错误: {e}")

    server.close_all()


if __name__ == "__main__":
    main()
