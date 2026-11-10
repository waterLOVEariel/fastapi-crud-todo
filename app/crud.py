"""CRUD 操作：增删改查的具体实现。"""
from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import models, schemas


def get_todos(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    done: bool | None = None,
    min_priority: int | None = None,
    sort_by: str | None = None,
):
    """动态拼装查询：按需加筛选、排序、分页。"""
    query = db.query(models.Todo)
    if done is not None:
        query = query.filter(models.Todo.done == done)
    if min_priority is not None:
        query = query.filter(models.Todo.priority >= min_priority)
    if sort_by == "priority":
        query = query.order_by(models.Todo.priority.desc())
    elif sort_by == "id":
        query = query.order_by(models.Todo.id)
    return query.offset(skip).limit(limit).all()


def get_todo(db: Session, todo_id: int):
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()


def create_todo(db: Session, todo: schemas.TodoCreate):
    # 如果传了 category_id，先校验分类是否存在，避免脏外键
    if todo.category_id is not None:
        category = (
            db.query(models.Category)
            .filter(models.Category.id == todo.category_id)
            .first()
        )
        if category is None:
            raise HTTPException(status_code=404, detail="Category not found")

    db_todo = models.Todo(
        title=todo.title,
        done=todo.done,
        priority=todo.priority,
        category_id=todo.category_id,
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo(db: Session, todo_id: int, todo: schemas.TodoCreate):
    db_todo = get_todo(db, todo_id)
    if db_todo:
        db_todo.title = todo.title
        db_todo.done = todo.done
        db_todo.priority = todo.priority
        db_todo.category_id = todo.category_id
        db.commit()
        db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int):
    db_todo = get_todo(db, todo_id)
    if db_todo:
        db.delete(db_todo)
        db.commit()
    return db_todo


def get_categories(db: Session):
    return db.query(models.Category).all()


def get_category(db: Session, category_id: int):
    return (
        db.query(models.Category)
        .filter(models.Category.id == category_id)
        .first()
    )


def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_todos_by_category(db: Session, category_id: int):
    return (
        db.query(models.Todo)
        .filter(models.Todo.category_id == category_id)
        .all()
    )
