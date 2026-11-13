"""数据库连接配置：通过 SQLAlchemy engine 连接 MySQL。"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# .env 在项目根目录；显式指定路径，避免从别的目录启动时找不到
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# 连接串从环境变量读，代码里不出现密码
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
if not SQLALCHEMY_DATABASE_URL:
    raise RuntimeError("未找到 DATABASE_URL,请复制 .env.example 为 .env 并填写")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 每个请求创建一个独立的数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 所有数据模型都继承这个 Base，方便统一建表
Base = declarative_base()


def get_db():
    """FastAPI 依赖注入：每个请求拿一个会话，用完关闭。"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
