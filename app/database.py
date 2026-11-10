"""数据库连接配置。

用 SQLite 起步，不用装 MySQL 服务，先跑通再说。
后面想换 MySQL 时，只需要改这一处 URL 即可，其余代码不用动。
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 数据库文件会生成在项目根目录下，叫 todo.db
SQLALCHEMY_DATABASE_URL = "sqlite:///./todo.db"

# check_same_thread=False 是 SQLite 在 FastAPI 多线程下的必要配置
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

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
