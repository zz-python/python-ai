# config.py
# pip install python-dotenv
import os
from dotenv import load_dotenv

# 在模块导入时加载一次
load_dotenv()

class Config:
    """应用配置类"""
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # @classmethod
    # def validate(cls):
    #     """可选：验证必需的配置是否存在"""
    #     required_vars = ["DATABASE_URL"]
    #     missing = [var for var in required_vars if not getattr(cls, var)]
    #     if missing:
    #         raise EnvironmentError(f"Missing required env vars: {', '.join(missing)}")

# 实例化配置对象，方便导入
config = Config()
# config.validate()