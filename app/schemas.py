"""Pydantic 模型：定义接口收发的数据格式（入参校验 + 出参结构）。"""
from pydantic import BaseModel


class TodoBase(BaseModel):
    title: str
    done: bool = False
    priority: int = 1
    category_id: int | None = None  # 可选：允许 todo 暂时无分类


class TodoCreate(TodoBase):
    """创建 / 更新时用的入参结构。"""


class TodoOut(TodoBase):
    """返回给前端时带上的 id 和嵌套分类对象。"""
    model_config = {"from_attributes": True}

    id: int
    category: "CategoryOut | None" = None


class CategoryCreate(BaseModel):
    """创建分类的入参结构。"""
    name: str


class CategoryOut(BaseModel):
    """返回分类信息，附带该分类下的 todo 数量。"""
    model_config = {"from_attributes": True}

    id: int
    name: str
    todo_count: int = 0  # 由接口层用 len(category.todos) 手动填充，见 main.py
