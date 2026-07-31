# main.py
# 自然语言 → SQL 查询工具（命令行交互）
# 用法: python main.py
import sys
from db import (
    get_connection,
    get_table_names,
    get_table_schema,
    get_all_schemas,
    is_safe_sql,
    execute_select,
    format_results,
)
from sql_generator import create_sql_chain, generate_sql, clean_sql_output
from config import config


# ============================================================
# 帮助信息
# ============================================================


def print_welcome(db_name: str, table_names: list):
    """打印欢迎信息。"""
    print("=" * 60)
    print("  Natural Language → SQL Query Tool")
    print("  用自然语言描述需求，自动生成 SQL 并执行")
    print("=" * 60)
    print(f"已连接到数据库: {db_name}")
    print(f"发现 {len(table_names)} 张表: {', '.join(table_names)}")
    print()
    print("命令:")
    print("  <自然语言需求>    描述你想查询的内容")
    print("  /tables, /t       列出所有表")
    print("  /schema <表名>    查看某张表的结构")
    print("  /help, /h         显示帮助")
    print("  /exit, /quit      退出程序")
    print("=" * 60)


def print_help():
    """打印帮助信息。"""
    print("""
内置命令:
  /tables, /t         - 列出数据库中所有表名
  /schema <表名>      - 查看指定表的 CREATE TABLE 语句
  /help, /h           - 显示此帮助信息
  /exit, /quit        - 退出程序

使用示例:
  > 查询所有用户
  > 查找2024年之后注册的用户，显示姓名和注册日期
  > 统计每个分类下的商品数量
  > 查询订单金额大于1000的用户姓名和订单号
  > 按注册时间倒序显示最近10个用户
  > 查询名字中包含"张"的员工
""")


# ============================================================
# 主循环
# ============================================================


def main():
    # 1. 连接数据库
    print("正在连接数据库...")
    try:
        conn = get_connection()
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        print("\n请检查 lang-chain-sql/.env 中的 MySQL 配置是否正确。")
        sys.exit(1)

    try:
        # 2. 获取表结构
        print("正在获取表结构...")
        try:
            table_names = get_table_names(conn)
            if not table_names:
                print(f"⚠️  数据库 '{config.MYSQL_DATABASE}' 中没有任何表。")
                print("请先创建表后再使用本工具。")
                return
            table_schemas = get_all_schemas(conn)
        except Exception as e:
            print(f"❌ 获取表结构失败: {e}")
            return

        # 3. 创建 LLM 链（只创建一次，复用）
        print("正在初始化 LLM...")
        try:
            chain = create_sql_chain()
        except Exception as e:
            print(f"❌ LLM 初始化失败: {e}")
            return

        print()
        print_welcome(config.MYSQL_DATABASE, table_names)

        # 4. 交互循环
        while True:
            try:
                user_input = input("\n请输入需求 > ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n\n👋 再见！")
                break

            # 空输入
            if not user_input:
                continue

            # 处理内置命令
            if user_input.lower() in ("/exit", "/quit", "exit", "quit"):
                print("👋 再见！")
                break

            if user_input.lower() in ("/tables", "/t"):
                print(f"\n数据库中的表 ({len(table_names)} 张):")
                for t in table_names:
                    print(f"  - {t}")
                continue

            if user_input.lower().startswith("/schema "):
                table_name = user_input.split(" ", 1)[1].strip().strip("`")
                try:
                    schema = get_table_schema(conn, table_name)
                    print(f"\n{schema}")
                except Exception as e:
                    print(f"❌ 获取表结构失败: {e}")
                continue

            if user_input.lower() in ("/help", "/h"):
                print_help()
                continue

            # 5. 生成 SQL
            print("\n⏳ 正在生成 SQL...")
            try:
                raw_sql = generate_sql(chain, table_schemas, user_input)
            except Exception as e:
                print(f"❌ SQL 生成失败: {e}")
                continue

            # 6. 清洗 SQL 输出
            sql = clean_sql_output(raw_sql)

            print(f"\n📝 [生成的 SQL]\n{sql}")

            # 7. 安全检查
            safe, reason = is_safe_sql(sql)
            if not safe:
                print(f"\n⚠️  [安全检查未通过] {reason}")
                print("该 SQL 不会被执行。")
                continue

            # 8. 执行 SQL
            try:
                rows = execute_select(conn, sql)
            except Exception as e:
                print(f"\n❌ [SQL 执行错误] {e}")
                continue

            # 9. 显示结果
            if not rows:
                print("\n📊 [结果] (0 行) — 未查询到数据。")
            else:
                print(f"\n📊 [结果] ({len(rows)} 行)")
                print(format_results(rows, max_rows=50))

    finally:
        conn.close()


if __name__ == "__main__":
    main()