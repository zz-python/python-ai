# config.py
# pip install python-dotenv
import os
from dotenv import load_dotenv

# 在模块导入时加载 .env 文件
load_dotenv()


class Config:
    """应用配置类"""

    # LLM 配置
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # MySQL 配置
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "test")
    MYSQL_CHARSET = os.getenv("MYSQL_CHARSET", "utf8mb4")


# 实例化配置对象，方便导入
config = Config()