# db.py
# 数据库操作层：连接管理、表结构获取、SQL 执行、安全校验
# pip install pymysql
import re
import pymysql
from config import config

# ============================================================
# SQL 安全校验
# ============================================================

# 允许的 SQL 语句开头关键字（只读操作）
ALLOWED_STARTS = {"SELECT", "WITH", "EXPLAIN", "DESCRIBE", "SHOW", "DESC"}

# 危险关键字（正则模式，大小写不敏感）
DANGEROUS_PATTERNS = [
    r"\bINSERT\b",
    r"\bUPDATE\b",
    r"\bDELETE\b",
    r"\bDROP\b",
    r"\bCREATE\b",
    r"\bALTER\b",
    r"\bTRUNCATE\b",
    r"\bRENAME\b",
    r"\bREPLACE\b",
    r"\bGRANT\b",
    r"\bREVOKE\b",
    r"\bLOAD\b",
    r"\bINTO\s+(OUTFILE|DUMPFILE)\b",
    r"\bEXEC\b",
    r"\bEXECUTE\b",
    r"\bCALL\b",
    r"\bLOCK\b",
    r"\bUNLOCK\b",
    r"\bSET\b",
    r"\bHANDLER\b",
    r"\bPURGE\b",
    r"\bRESET\b",
    r"\bFLUSH\b",
    r"\bKILL\b",
    r"\bSHUTDOWN\b",
]


def is_safe_sql(sql: str) -> tuple:
    """
    校验 SQL 语句是否安全（只允许 SELECT 等只读操作）。

    返回 (is_safe: bool, reason: str)
    """
    if not sql or not sql.strip():
        return False, "SQL 语句为空"

    cleaned = sql.strip()

    # 去掉尾部分号
    if cleaned.endswith(";"):
        cleaned = cleaned[:-1].strip()

    if not cleaned:
        return False, "SQL 语句为空"

    # 1. 检测多语句注入（分号在语句中间）
    if ";" in cleaned:
        return False, "不允许执行多条 SQL 语句（检测到分号）"

    # 2. 检测 SQL 注释（可能隐藏恶意代码）
    if "--" in cleaned or "/*" in cleaned or "*/" in cleaned:
        return False, "SQL 语句中不允许包含注释（-- 或 /* */）"

    # 3. 检查第一个关键字是否为允许的只读操作
    first_word = cleaned.split()[0].upper()
    if first_word not in ALLOWED_STARTS:
        return False, f"不允许的语句类型 '{first_word}'，仅支持 SELECT 查询"

    # 4. 检查危险关键字
    upper_sql = cleaned.upper()
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, upper_sql):
            # 提取匹配到的关键字用于提示
            keyword = pattern.replace(r"\b", "").replace(r"\s+", " ").split("|")[0]
            return False, f"检测到危险关键字: {keyword}"

    return True, ""


# ============================================================
# 数据库连接
# ============================================================


def get_connection() -> pymysql.Connection:
    """
    创建并返回 PyMySQL 数据库连接。
    使用 DictCursor，查询结果以字典形式返回。
    """
    return pymysql.connect(
        host=config.MYSQL_HOST,
        port=config.MYSQL_PORT,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        database=config.MYSQL_DATABASE,
        charset=config.MYSQL_CHARSET,
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=10,
    )


# ============================================================
# 表结构获取
# ============================================================


def get_table_names(conn: pymysql.Connection) -> list:
    """
    获取数据库中所有表名。
    """
    with conn.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        rows = cursor.fetchall()
        # SHOW TABLES 返回的 key 名格式为 Tables_in_<database>
        key = f"Tables_in_{config.MYSQL_DATABASE}"
        return [row[key] for row in rows]


def get_table_schema(conn: pymysql.Connection, table_name: str) -> str:
    """
    获取单张表的 CREATE TABLE 语句（DDL）。
    """
    with conn.cursor() as cursor:
        cursor.execute(f"SHOW CREATE TABLE `{table_name}`")
        row = cursor.fetchone()
        if row is None:
            raise ValueError(f"表 '{table_name}' 不存在")
        # SHOW CREATE TABLE 返回两列: Table, Create Table
        # 使用 values() 按位置取第二列，避免键名在不同 MySQL/PyMySQL 版本中不一致
        return list(row.values())[1]


def get_all_schemas(conn: pymysql.Connection) -> str:
    """
    获取数据库中所有表的 DDL，拼接成字符串作为 LLM 上下文。
    """
    tables = get_table_names(conn)
    parts = []
    for table in tables:
        schema = get_table_schema(conn, table)
        parts.append(f"-- Table: {table}\n{schema}")
    return "\n\n".join(parts)


# ============================================================
# SQL 执行
# ============================================================


def execute_select(conn: pymysql.Connection, sql: str) -> list:
    """
    执行 SELECT 查询并返回结果行列表。

    返回: list[dict] — 每行是一个字典，键为列名
    """
    with conn.cursor() as cursor:
        cursor.execute(sql)
        return cursor.fetchall()


# ============================================================
# 结果格式化
# ============================================================


def format_results(rows: list, max_rows: int = 50) -> str:
    """
    将查询结果格式化为可读的表格字符串。

    参数:
        rows: 查询结果行列表
        max_rows: 最多显示的行数
    """
    if not rows:
        return "(空结果)"

    # 获取列名
    columns = list(rows[0].keys())

    # 计算每列的最大宽度（列名 vs 数据）
    col_widths = {}
    for col in columns:
        col_widths[col] = len(str(col))
    for row in rows[:max_rows]:
        for col in columns:
            val_str = str(row[col]) if row[col] is not None else "NULL"
            col_widths[col] = max(col_widths[col], len(val_str))

    # 构建分隔线
    separator = "+" + "+".join("-" * (col_widths[col] + 2) for col in columns) + "+"

    # 表头
    header = "|" + "|".join(f" {col:<{col_widths[col]}} " for col in columns) + "|"

    # 构建输出
    lines = [separator, header, separator]

    # 数据行
    display_rows = rows[:max_rows]
    for row in display_rows:
        line = "|"
        for col in columns:
            val_str = str(row[col]) if row[col] is not None else "NULL"
            line += f" {val_str:<{col_widths[col]}} |"
        lines.append(line)

    lines.append(separator)

    # 如果结果被截断
    if len(rows) > max_rows:
        lines.append(f"\n(仅显示前 {max_rows} 行，共 {len(rows)} 行)")

    return "\n".join(lines)