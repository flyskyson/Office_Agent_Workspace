"""
数据库管理器 - 使用SQLite存储经营户档案

功能：
- 创建数据库和表结构
- 插入、更新、查询经营户数据
- 搜索和过滤
- 数据导出
"""

import sqlite3
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from contextlib import contextmanager
from loguru import logger


class DatabaseManager:
    """数据库管理器 - 管理经营户档案数据库"""

    def __init__(self, db_path: str = "data/operators_database.db"):
        """初始化数据库

        Args:
            db_path: 数据库文件路径
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # 初始化数据库
        self._init_database()
        logger.info(f"数据库初始化完成: {self.db_path}")

    @contextmanager
    def _get_connection(self):
        """获取数据库连接（上下文管理器）

        Yields:
            sqlite3.Connection: 数据库连接
        """
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row  # 返回字典格式
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"数据库操作失败: {e}")
            raise e
        finally:
            conn.close()

    def _init_database(self):
        """初始化数据库表结构"""
        with self._get_connection() as conn:
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
            conn.execute('CREATE INDEX IF NOT EXISTS idx_operator_name ON operators(operator_name)')

            # 创建操作日志表
            conn.execute('''
                CREATE TABLE IF NOT EXISTS operation_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operator_id INTEGER,
                    operation TEXT NOT NULL,
                    details TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (operator_id) REFERENCES operators(id)
                )
            ''')

            logger.info("数据库表结构初始化完成")

    def insert_operator(self, data: Dict) -> int:
        """插入经营户数据

        Args:
            data: 经营户数据字典

        Returns:
            插入记录的ID

        Raises:
            sqlite3.IntegrityError: 身份证号重复
        """
        with self._get_connection() as conn:
            try:
                cursor = conn.execute('''
                    INSERT INTO operators (
                        operator_name, id_card, phone, email, gender, nation, address,
                        business_name, business_address, business_scope, credit_code,
                        property_owner, lease_start, lease_end, rent_amount,
                        id_card_front_path, id_card_back_path,
                        business_license_path, lease_contract_path, property_cert_path,
                        archive_path, metadata
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    data.get('operator_name'),
                    data.get('id_card'),
                    data.get('phone'),
                    data.get('email'),
                    data.get('gender'),
                    data.get('nation'),
                    data.get('address'),
                    data.get('business_name'),
                    data.get('business_address'),
                    data.get('business_scope'),
                    data.get('credit_code'),
                    data.get('property_owner'),
                    data.get('lease_start'),
                    data.get('lease_end'),
                    data.get('rent_amount'),
                    data.get('id_card_front_path'),
                    data.get('id_card_back_path'),
                    data.get('business_license_path'),
                    data.get('lease_contract_path'),
                    data.get('property_cert_path'),
                    data.get('archive_path'),
                    json.dumps(data.get('metadata', {}), ensure_ascii=False)
                ))

                operator_id = cursor.lastrowid

                # 记录操作日志
                self._log_operation(conn, operator_id, 'insert', '新建经营户记录')

                logger.info(f"插入经营户记录: ID={operator_id}, 姓名={data.get('operator_name')}")
                return operator_id

            except sqlite3.IntegrityError as e:
                if 'UNIQUE constraint failed: operators.id_card' in str(e):
                    # 身份证号已存在，尝试更新
                    logger.warning(f"身份证号 {data.get('id_card')} 已存在，尝试更新记录")
                    existing = self.get_operator_by_id_card(data['id_card'])
                    if existing:
                        return self.update_operator(data['id_card'], data)
                raise e

    def get_operator_by_id(self, operator_id: int) -> Optional[Dict]:
        """根据ID查询经营户

        Args:
            operator_id: 记录ID

        Returns:
            经营户数据字典，不存在返回None
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                'SELECT * FROM operators WHERE id = ?',
                (operator_id,)
            )
            row = cursor.fetchone()
            if row:
                return self._row_to_dict(row)
            return None

    def get_operator_by_id_card(self, id_card: str) -> Optional[Dict]:
        """根据身份证号查询经营户

        Args:
            id_card: 身份证号

        Returns:
            经营户数据字典，不存在返回None
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                'SELECT * FROM operators WHERE id_card = ?',
                (id_card,)
            )
            row = cursor.fetchone()
            if row:
                return self._row_to_dict(row)
            return None

    def get_operator_by_name(self, operator_name: str) -> List[Dict]:
        """根据经营者姓名查询

        Args:
            operator_name: 经营者姓名

        Returns:
            匹配的经营户列表
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                'SELECT * FROM operators WHERE operator_name = ? AND status = "active"',
                (operator_name,)
            )
            return [self._row_to_dict(row) for row in cursor.fetchall()]

    def get_operator_by_business_name(self, business_name: str) -> List[Dict]:
        """根据店名查询

        Args:
            business_name: 个体工商户名称

        Returns:
            匹配的经营户列表
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                'SELECT * FROM operators WHERE business_name LIKE ? AND status = "active"',
                (f'%{business_name}%',)
            )
            return [self._row_to_dict(row) for row in cursor.fetchall()]

    def update_operator(self, id_card: str, updates: Dict) -> int:
        """更新经营户数据

        Args:
            id_card: 身份证号
            updates: 要更新的字段字典

        Returns:
            更新的记录ID
        """
        if not updates:
            return 0

        # 处理metadata字段
        if 'metadata' in updates:
            updates['metadata'] = json.dumps(updates['metadata'], ensure_ascii=False)

        set_clause = ', '.join(f'{k} = ?' for k in updates.keys())
        values = list(updates.values()) + [datetime.now().isoformat(), id_card]

        with self._get_connection() as conn:
            cursor = conn.execute(
                f'UPDATE operators SET {set_clause}, updated_at = ? WHERE id_card = ?',
                values
            )

            # 记录操作日志 - 在同一个连接上查询，避免事务隔离问题
            if cursor.rowcount > 0:
                # 直接在当前连接上查询，而不是调用get_operator_by_id_card
                cursor2 = conn.execute(
                    'SELECT id FROM operators WHERE id_card = ?',
                    (id_card,)
                )
                row = cursor2.fetchone()
                if row:
                    operator_id = row['id']
                    self._log_operation(
                        conn,
                        operator_id,
                        'update',
                        f'更新字段: {", ".join(updates.keys())}'
                    )
                    logger.info(f"更新经营户记录: ID={operator_id}, 更新字段={list(updates.keys())}")
                    return operator_id

        return 0

    def delete_operator(self, id_card: str, soft_delete: bool = True) -> bool:
        """删除经营户记录

        Args:
            id_card: 身份证号
            soft_delete: 是否软删除（仅标记status）

        Returns:
            是否成功
        """
        with self._get_connection() as conn:
            if soft_delete:
                cursor = conn.execute(
                    'UPDATE operators SET status = "deleted", updated_at = ? WHERE id_card = ?',
                    (datetime.now().isoformat(), id_card)
                )
            else:
                cursor = conn.execute(
                    'DELETE FROM operators WHERE id_card = ?',
                    (id_card,)
                )

            success = cursor.rowcount > 0
            if success:
                logger.info(f"删除经营户记录: id_card={id_card}, soft_delete={soft_delete}")
            return success

    def list_operators(
        self,
        limit: int = 100,
        offset: int = 0,
        status: str = 'active'
    ) -> List[Dict]:
        """列出所有经营户

        Args:
            limit: 返回数量限制
            offset: 偏移量
            status: 状态过滤

        Returns:
            经营户列表
        """
        with self._get_connection() as conn:
            cursor = conn.execute('''
                SELECT * FROM operators
                WHERE status = ?
                ORDER BY updated_at DESC
                LIMIT ? OFFSET ?
            ''', (status, limit, offset))

            return [self._row_to_dict(row) for row in cursor.fetchall()]

    def search_operators(self, keyword: str) -> List[Dict]:
        """搜索经营户

        Args:
            keyword: 搜索关键词（匹配姓名、店名、身份证号、手机号）

        Returns:
            匹配的经营户列表
        """
        with self._get_connection() as conn:
            cursor = conn.execute('''
                SELECT * FROM operators
                WHERE status = 'active'
                AND (
                    operator_name LIKE ?
                    OR business_name LIKE ?
                    OR id_card LIKE ?
                    OR phone LIKE ?
                )
                ORDER BY updated_at DESC
            ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))

            return [self._row_to_dict(row) for row in cursor.fetchall()]

    def get_record_count(self) -> int:
        """获取数据库记录总数

        Returns:
            记录总数
        """
        with self._get_connection() as conn:
            return conn.execute(
                'SELECT COUNT(*) FROM operators WHERE status = "active"'
            ).fetchone()[0]

    def get_statistics(self) -> Dict:
        """获取数据库统计信息

        Returns:
            统计信息字典
        """
        with self._get_connection() as conn:
            # 总记录数
            total = conn.execute(
                'SELECT COUNT(*) FROM operators WHERE status = "active"'
            ).fetchone()[0]

            # 本月新增
            this_month = conn.execute('''
                SELECT COUNT(*) FROM operators
                WHERE status = "active"
                AND strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now')
            ''').fetchone()[0]

            # 有营业执照的数量
            has_license = conn.execute('''
                SELECT COUNT(*) FROM operators
                WHERE status = "active" AND business_license_path IS NOT NULL
            ''').fetchone()[0]

            return {
                'total_operators': total,
                'this_month_new': this_month,
                'has_business_license': has_license,
            }

    def export_to_json(self, output_path: str) -> bool:
        """导出数据到JSON文件

        Args:
            output_path: 输出文件路径

        Returns:
            是否成功
        """
        try:
            operators = self.list_operators(limit=999999)

            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(operators, f, ensure_ascii=False, indent=2)

            logger.info(f"导出数据到: {output_path}")
            return True

        except Exception as e:
            logger.error(f"导出失败: {e}")
            return False

    def import_from_json(self, input_path: str) -> int:
        """从JSON文件导入数据

        Args:
            input_path: 输入文件路径

        Returns:
            导入的记录数
        """
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            count = 0
            for operator in data:
                try:
                    self.insert_operator(operator)
                    count += 1
                except sqlite3.IntegrityError:
                    # 跳过重复记录
                    continue

            logger.info(f"从 {input_path} 导入 {count} 条记录")
            return count

        except Exception as e:
            logger.error(f"导入失败: {e}")
            return 0

    def get_recent_logs(self, limit: int = 50) -> List[Dict]:
        """获取最近的操作日志

        Args:
            limit: 返回数量

        Returns:
            日志列表
        """
        with self._get_connection() as conn:
            cursor = conn.execute('''
                SELECT * FROM operation_logs
                ORDER BY created_at DESC
                LIMIT ?
            ''', (limit,))

            return [dict(row) for row in cursor.fetchall()]

    def _row_to_dict(self, row: sqlite3.Row) -> Dict:
        """将数据库行转换为字典"""
        data = dict(row)

        # 解析metadata JSON
        if data.get('metadata'):
            try:
                data['metadata'] = json.loads(data['metadata'])
            except:
                data['metadata'] = {}

        return data

    def _log_operation(
        self,
        conn: sqlite3.Connection,
        operator_id: int,
        operation: str,
        details: str = ""
    ):
        """记录操作日志

        Args:
            conn: 数据库连接
            operator_id: 经营户ID
            operation: 操作类型
            details: 详情
        """
        conn.execute('''
            INSERT INTO operation_logs (operator_id, operation, details)
            VALUES (?, ?, ?)
        ''', (operator_id, operation, details))

    def delete_operator(self, operator_id: int) -> bool:
        """删除经营户记录（软删除，设置 status 为 deleted）

        Args:
            operator_id: 经营户ID

        Returns:
            是否成功
        """
        try:
            with self._get_connection() as conn:
                # 软删除：设置 status 为 deleted
                conn.execute('''
                    UPDATE operators
                    SET status = 'deleted'
                    WHERE id = ?
                ''', (operator_id,))

                # 记录操作日志
                self._log_operation(conn, operator_id, 'delete', f'删除记录 ID={operator_id}')

            logger.info(f"删除经营户 ID={operator_id}")
            return True

        except Exception as e:
            logger.error(f"删除失败: {e}")
            return False


# 便捷函数
def get_db(db_path: str = "data/operators_database.db") -> DatabaseManager:
    """便捷函数：获取数据库管理器实例

    Args:
        db_path: 数据库路径

    Returns:
        DatabaseManager实例
    """
    return DatabaseManager(db_path)
