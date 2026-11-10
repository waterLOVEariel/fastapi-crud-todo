"""数据模型：定义待办事项和分类的表结构。"""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)          # 待办标题
    done = Column(Boolean, default=False)           # 是否完成
    priority = Column(Integer, default=1)           # 优先级（数字越大越优先）
    category_id = Column(Integer, ForeignKey("categories.id"))  # 所属分类
    category = relationship("Category", back_populates="todos")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)           # 分类名
    todos = relationship("Todo", back_populates="category")
