"""应用入口：定义接口路由。"""
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

# 用 FastAPIOffline 替代 FastAPI：Swagger UI 的 js/css 走本地文件，
# 不依赖外网 CDN（默认的 cdn.jsdelivr.net 在国内常打不开，导致 /docs 白屏）
from fastapi_offline import FastAPIOffline as FastAPI

from . import crud, models, schemas
from .database import engine, get_db

# 启动时自动建表（只建不存在的表，已有表结构不会自动迁移）
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo API", description="一个待办事项的 CRUD 示例")


@app.get("/")
def root():
    return {"message": "Todo API 运行中，访问 /docs 查看接口文档"}


@app.get("/todos", response_model=list[schemas.TodoOut])
def read_todos(
    skip: int = 0,
    limit: int = 100,
    done: bool | None = None,
    min_priority: int | None = None,
    sort_by: str | None = None,
    db: Session = Depends(get_db),
):
    """查所有待办，支持筛选（done / min_priority）、排序（sort_by）、分页（skip / limit）。"""
    return crud.get_todos(
        db, skip=skip, limit=limit, done=done,
        min_priority=min_priority, sort_by=sort_by,
    )


@app.post("/todos", response_model=schemas.TodoOut, status_code=201)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    """新增一条待办。"""
    return crud.create_todo(db, todo)


@app.get("/todos/{todo_id}", response_model=schemas.TodoOut)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    """按 id 查询单条待办。"""
    db_todo = crud.get_todo(db, todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@app.put("/todos/{todo_id}", response_model=schemas.TodoOut)
def update_todo(todo_id: int, todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    """按 id 更新待办。"""
    db_todo = crud.update_todo(db, todo_id, todo)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@app.delete("/todos/{todo_id}", response_model=schemas.TodoOut)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """按 id 删除待办。"""
    db_todo = crud.delete_todo(db, todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@app.get("/categories", response_model=list[schemas.CategoryOut])
def read_categories(db: Session = Depends(get_db)):
    """查所有分类，附带每个分类下的 todo 数量。"""
    categories = crud.get_categories(db)
    for c in categories:
        c.todo_count = len(c.todos)  # 用 relationship 数一下有多少条
    return categories


@app.post("/categories", response_model=schemas.CategoryOut, status_code=201)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    """新增一个分类。"""
    return crud.create_category(db, category)


@app.get("/categories/{category_id}", response_model=schemas.CategoryOut)
def read_category(category_id: int, db: Session = Depends(get_db)):
    """按 id 查询单个分类。"""
    db_category = crud.get_category(db, category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@app.get("/categories/{category_id}/todos", response_model=list[schemas.TodoOut])
def read_category_todos(category_id: int, db: Session = Depends(get_db)):
    """查某个分类下的所有待办。"""
    return crud.get_todos_by_category(db, category_id)
