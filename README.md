# Todo API — FastAPI + SQLAlchemy 待办事项后端

一个分层清晰的 FastAPI 后端示例项目，实现待办事项（Todo）与分类（Category）的一对多关系，支持完整 CRUD、筛选、排序、分页和关联查询。

## 功能

- 待办事项的增删改查（CRUD）
- 分类管理：创建、查询分类，以及按分类查待办
- 一对多关系：每个分类下挂多条待办，返回时自动嵌套分类信息
- 查询进阶：按完成状态 / 最低优先级筛选、按优先级或 id 排序、分页
- 外键校验：创建待办时校验分类是否存在，不存在返回 404
- 自动生成交互式接口文档（Swagger UI，走本地离线资源，不依赖外网 CDN）

## 技术栈

- FastAPI（异步 Web 框架）
- SQLAlchemy 2.0（ORM，声明式模型 + 关系映射）
- Pydantic 2.x（请求 / 响应数据校验）
- SQLite（零配置起步，换 MySQL 只需改连接串）

## 目录结构

```
fastapi-crud-todo/
├── app/
│   ├── __init__.py
│   ├── database.py   # 数据库连接、会话、Base 声明
│   ├── models.py     # 数据表结构（Todo / Category，一对多关系）
│   ├── schemas.py    # Pydantic 模型（接口收发格式）
│   ├── crud.py       # 增删改查 + 动态查询逻辑
│   └── main.py       # 接口路由
├── requirements.txt  # 依赖清单
├── .gitignore
└── README.md
```

分层说明：请求从 `main.py`（路由）进入 → 交给 `crud.py`（业务逻辑）→ 通过 `models.py`（表结构）操作数据库 → 用 `schemas.py` 校验入参、规范出参。

## 接口清单

| 方法   | 路径                          | 说明                                     |
| ------ | ----------------------------- | ---------------------------------------- |
| GET    | `/`                           | 健康检查                                 |
| GET    | `/todos`                      | 查所有待办（支持筛选 / 排序 / 分页）     |
| POST   | `/todos`                      | 新建待办（201）                          |
| GET    | `/todos/{todo_id}`            | 查单条待办                               |
| PUT    | `/todos/{todo_id}`            | 更新待办                                 |
| DELETE | `/todos/{todo_id}`            | 删除待办                                 |
| GET    | `/categories`                 | 查所有分类（附带 todo 数量）             |
| POST   | `/categories`                 | 新建分类（201）                          |
| GET    | `/categories/{category_id}`   | 查单个分类                               |
| GET    | `/categories/{category_id}/todos` | 查某分类下的所有待办                 |

## 快速开始

```bash
# 1. 创建并激活虚拟环境
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动服务
uvicorn app.main:app --reload

# 4. 打开接口文档，直接点按钮测试
# http://127.0.0.1:8000/docs
```

## 查询参数示例

```
GET /todos?done=false&min_priority=2&sort_by=priority&skip=0&limit=10
```

- `done`：过滤完成 / 未完成
- `min_priority`：只返回优先级 >= 该值的待办
- `sort_by`：`priority`（降序）或 `id`（升序）
- `skip` / `limit`：分页

## 数据模型

```
Category 1 ──── N Todo
（分类）        （待办）

Todo.category_id 是外键，指向 Category.id；
通过 relationship 双向绑定，查 Todo 时能直接拿到所属分类对象。
```
