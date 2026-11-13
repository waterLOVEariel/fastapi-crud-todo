# Todo API — FastAPI + SQLAlchemy 待办事项后端

一个分层清晰的 FastAPI 后端示例项目，实现待办事项（Todo）与分类（Category）的一对多关系，支持完整 CRUD、筛选、排序、分页和关联查询。数据库使用 MySQL 8。

## 功能

- 待办事项的增删改查（CRUD）
- 分类管理：创建、查询分类，以及按分类查待办
- 一对多关系：每个分类下挂多条待办，返回时自动嵌套分类信息
- 查询进阶：按完成状态 / 最低优先级筛选、按优先级或 id 排序、分页
- 外键校验：创建待办时校验分类是否存在，不存在返回 404
- 自动生成交互式接口文档（Swagger UI，走本地离线资源，不依赖外网 CDN）

## 技术栈

| 组件 | 版本 / 说明 |
| --- | --- |
| FastAPI | 0.115，Web 框架 |
| SQLAlchemy | 2.0，ORM，声明式模型 + 关系映射 |
| Pydantic | 2.x，请求 / 响应数据校验 |
| MySQL | 8.0，字符集 `utf8mb4`（完整支持 emoji 与生僻字） |
| PyMySQL | MySQL 驱动 |
| python-dotenv | 从 `.env` 加载数据库配置 |

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
├── .env.example      # 环境变量模板（复制为 .env 后填写）
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

### 1. 准备数据库

先启动 MySQL 服务，然后用 root 创建专用库和专用账号（遵循最小权限原则，应用不使用 root）：

```sql
CREATE DATABASE IF NOT EXISTS todo_db
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'todo_app'@'localhost' IDENTIFIED BY '你的密码';

GRANT ALL PRIVILEGES ON todo_db.* TO 'todo_app'@'localhost';

FLUSH PRIVILEGES;
```

> 字符集必须用 `utf8mb4`。MySQL 里的 `utf8` 最多只存 3 字节，存不了 emoji。

### 2. 配置环境变量

```bash
# 复制模板，然后把里面的用户名和密码改成你自己的
cp .env.example .env        # Windows: copy .env.example .env
```

`.env` 内容形如：

```
DATABASE_URL=mysql+pymysql://todo_app:你的密码@127.0.0.1:3306/todo_db?charset=utf8mb4
```

`.env` 已被 `.gitignore` 排除，不会提交到仓库。

### 3. 安装依赖并启动

```bash
# 创建并激活虚拟环境
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS / Linux

# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn app.main:app --reload
```

首次启动会自动建表。打开 <http://127.0.0.1:8000/docs> 即可在页面上直接调接口。

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

## 关于数据库迁移

本项目用 `Base.metadata.create_all()` 建表，它只创建**不存在的表**，不会修改已有表的结构。改动模型字段后，需要手动 `ALTER TABLE` 或使用 Alembic 管理迁移。
