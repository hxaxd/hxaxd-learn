# Python 后端开发

## 参考资料

- [Pydantic 官方文档](https://docs.pydantic.dev/latest/)
- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [SQLAlchemy 官方文档](https://docs.sqlalchemy.org/)
- [Alembic 官方文档](https://alembic.sqlalchemy.org/)
- [Uvicorn 官方文档](https://www.uvicorn.org/)

## Pydantic

- Pydantic 不是静态类型检查器, 它做的是运行时数据校验, 类型转换, 序列化和 JSON Schema 生成
- FastAPI 会读取 Pydantic 模型来校验请求体, 过滤响应字段, 并生成 OpenAPI 文档

### BaseModel

```python
from pydantic import BaseModel, ConfigDict, Field


class UserIn(BaseModel):
    model_config = ConfigDict(extra="forbid") # 禁止未声明字段

    id: int
    name: str = Field(min_length=1, max_length=50)
    age: int | None = Field(default=None, ge=0)
    password: str = Field(min_length=8)


user = UserIn.model_validate( # 将字典数据转换成 UserIn 对象
    {"id": "123", "name": "alice", "age": 18, "password": "secret123"}
)

assert user.id == 123 # 默认会做合理类型转换
```

### 校验器和序列化器

```python
from datetime import datetime, timezone

from pydantic import BaseModel, computed_field, field_serializer, field_validator


class Event(BaseModel):
    title: str
    starts_at: datetime
    ends_at: datetime

    @field_validator("title") # 校验单个字段, 也可以用 @model_validator 校验整个模型
    @classmethod
    def title_not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("title cannot be blank")
        return value

    @field_validator("ends_at")
    @classmethod
    def ends_after_start(cls, value: datetime, info):
        starts_at = info.data.get("starts_at")
        if starts_at is not None and value <= starts_at:
            raise ValueError("ends_at must be after starts_at")
        return value

    @computed_field # 修饰计算属性, 将其纳入序列化结果
    @property # 把方法变成属性
    def duration_seconds(self) -> int:
        return int((self.ends_at - self.starts_at).total_seconds())

    @field_serializer("starts_at", "ends_at")
    def serialize_dt(self, value: datetime) -> str:
        return value.astimezone(timezone.utc).isoformat()
```

### Settings

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "demo"
    database_url: str
    jwt_secret_key: str
    cors_origins: list[str] = []


settings = Settings()
```

## FastAPI

- FastAPI 基于 Starlette 和 Pydantic
- Starlette 提供 ASGI, 路由, 请求响应, 中间件等底层能力
- Pydantic 负责数据校验和序列化
- OpenAPI 文档是 FastAPI 根据路由, 类型标注和 Pydantic 模型生成出来的
- 可以使用 `async` / `await`, 但普通 `def` 路由也能用

```python
from fastapi import FastAPI

app = FastAPI(title="Demo API", version="0.1.0")


@app.get("/")
async def root():
    return {"message": "Hello World"}
```

### 路径参数

```python
from enum import Enum
from typing import Annotated

from fastapi import FastAPI, Path # Path 用来声明路径参数的约束, 标题, 描述等

app = FastAPI()


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/users/me") # 按声明顺序优先匹配 /users/me
async def read_current_user():
    return {"user": "current"}


@app.get("/users/{user_id}")
async def read_user(user_id: Annotated[int, Path(ge=1)]): # ge=1 表示 user_id 必须大于等于 1
    return {"user_id": user_id}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    return {"model_name": model_name}
```

### 查询参数

- 查询参数形如 `/items/?skip=0&limit=10`
- 查询参数不会决定使用哪个路由函数; 路由匹配主要看 HTTP 方法和路径
    - 路由匹配后, FastAPI 再解析查询参数, Cookie, Header, Body 等
- 可选参数写成 `str | None = None`
- `bool` 查询参数会识别 `true`, `false`, `1`, `0`, `yes`, `no`

```python
from typing import Annotated

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()


class FilterParams(BaseModel):
    q: str | None = None
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=20, ge=1, le=100)


@app.get("/items/")
async def read_items(filters: Annotated[FilterParams, Query()]):
    return filters
```

### 请求体

- 请求体通常是 JSON, 用 Pydantic 模型声明
- 路径参数, 查询参数和请求体可以同时出现
- `Body`, `Cookie`, `Header`, `Path`, `Query` 都可以和 `Annotated` 搭配使用
- 表单不是 JSON, 要用 `Form`
- 文件上传用 `File` 或 `UploadFile`

```python
from typing import Annotated

from fastapi import Body, Cookie, FastAPI, Header
from pydantic import BaseModel, Field

app = FastAPI()


class ItemCreate(BaseModel):
    name: str = Field(min_length=1)
    description: str | None = None
    price: float = Field(gt=0)
    tax: float | None = None


@app.post("/items/")
async def create_item(
    item: ItemCreate,
    importance: Annotated[int, Body(ge=1)] = 1,
    session_id: Annotated[str | None, Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None,
):
    return {"item": item, "importance": importance}
```

```python
from typing import Annotated

from fastapi import FastAPI, File, Form, UploadFile

app = FastAPI()


@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}


@app.post("/files/")
async def upload_file(file: Annotated[UploadFile, File()]):
    content = await file.read()
    return {"filename": file.filename, "size": len(content)}
```

### 更新

```python
from pydantic import BaseModel


class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None


stored_item = {"name": "Foo", "description": "old", "price": 10.0}


def apply_patch(patch: ItemUpdate):
    update_data = patch.model_dump(exclude_unset=True) # 避免未传字段覆盖原值
    return stored_item | update_data
```

### 响应

- 需要直接控制响应时, 可以返回 `Response`, `JSONResponse`, `FileResponse`, `StreamingResponse`

```python
from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()


class UserIn(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    username: str


@app.post("/users/", response_model=UserOut, status_code=status.HTTP_201_CREATED) # 这个码仅是成功时返回
async def create_user(user: UserIn):
    data = jsonable_encoder(user) # 转换成 JSON 兼容数据
    return data # password 会被 response_model 过滤掉
```

### 错误处理

- 全局错误格式可以用 exception handler 统一处理

```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 404:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id}


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})
```

### 后台任务

- FastAPI `BackgroundTasks` 只适合响应后顺手做的小事, 比如写日志, 发一个非关键通知, 调一个很短的 webhook
- 真正的任务队列要有独立 worker 和 broker, 不要占住 Web 进程
- 推荐顺序:
    - Celery: 默认生产选择, 生态最成熟, 适合重任务, 定时任务, 重试, 路由和监控
    - RQ: Redis + 普通 Python 函数, 心智负担最低, 适合中小项目
    - Dramatiq: 比 Celery 轻一些, 比 RQ 更像完整任务处理框架
    - ARQ: asyncio + Redis, 适合 async job, 但当前更适合能接受维护状态的项目

```python
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


def write_notification(email: str, message: str = ""):
    with open("log.txt", mode="a", encoding="utf-8") as email_file:
        email_file.write(f"notification for {email}: {message}\n")


@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    # 在响应返回后执行 write_notification
    # 适合小任务, 耗时任务应交给 Celery, RQ, Dramatiq, ARQ 等任务队列
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}
```

### 静态文件

- `StaticFiles` 会被挂载成一个独立的 ASGI 子应用

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
```

### 依赖注入

- 依赖可以是任何可调用对象
- 依赖可以嵌套, 重复依赖会被缓存, 菱形依赖通常只执行一次
- 路径装饰器, router, app 都可以声明依赖
    - 路径装饰器上的依赖会被执行, 但返回值不会传入路由函数
- FastAPI 0.121.0 之后
    - `Depends(scope="request")` 是默认行为, `yield` 后的清理在响应发送后执行
    - `scope="function"` 会在路由函数结束后, 响应发送前执行清理

```python
from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

app = FastAPI()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DbSession = Annotated[Session, Depends(get_db)]


@app.get("/items/")
def read_items(db: DbSession):
    return db.execute(...)
```

### 中间件

```python
import time

from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware("http") # 给所有请求添加处理时间响应头
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

### CORS

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 安全

- 核心流程:
    - 客户端把 `username` 和 `password` 提交给 `/token`
    - 服务端校验密码, 生成 token
    - 客户端之后请求受保护接口时带上请求头 `Authorization: Bearer <token>`
    - `OAuth2PasswordBearer` 只负责从请求头里取出 token 字符串
    - `get_current_user` 负责解析 token, 找到当前用户
    - 业务接口依赖 `current_user`, 不直接关心 token 怎么来

```python
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

SECRET_KEY = "change-me"
ALGORITHM = "HS256"

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str


def create_token(username: str) -> str:
    payload = {
        "sub": username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def parse_token(token: str) -> str:
    error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
    except jwt.InvalidTokenError as exc:
        raise error from exc

    if username is None:
        raise error

    return username


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    username = parse_token(token)
    return User(username=username)


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # 真实项目: 查数据库, 用哈希算法校验密码
    if form_data.username != "alice" or form_data.password != "secret":
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {
        "access_token": create_token(form_data.username),
        "token_type": "bearer",
    }


@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
```

### Lifespan

```python
from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager # 生命期事件可能有异步操作, 所以用 asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.cache = {}
    yield
    app.state.cache.clear()


app = FastAPI(lifespan=lifespan) # 注册生命期事件
```

### 架构

- `APIRouter` 用来声明一个模块内的路由组
- app 用 `include_router` 包含路由组
- router 和 app 都可以声明 `prefix`, `tags`, `dependencies`, `responses`
- 大项目常见目录:
    - `main.py`: 创建 app, 注册 middleware, router, lifespan
    - `routers/`: 路由层
    - `schemas/`: Pydantic 请求/响应模型
    - `models/`: SQLAlchemy ORM 模型
    - `services/`: 业务逻辑
    - `repositories/`: 数据访问逻辑
    - `dependencies.py`: 依赖注入函数
    - `settings.py`: 配置

```python
from fastapi import APIRouter, Depends, FastAPI

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users

app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
```

## 数据库驱动

- 数据库驱动负责和具体数据库通信
- SQLAlchemy 可以建立在不同驱动之上
- MySQL 常见驱动:
    - `mysql-connector-python`: MySQL 官方驱动, 写法接近 DB-API
    - `PyMySQL`: 纯 Python MySQL 驱动
- PostgreSQL 常见驱动:
    - `psycopg`: psycopg 3, 同步/异步都支持
    - `asyncpg`: 异步 PostgreSQL 驱动
- SQLite 标准库自带 `sqlite3`

## SQLAlchemy

- SQLAlchemy 2.0 推荐使用
    - `select(...)`: 创建对象化的 SQL 语句
    - `session.execute(...)`: 执行并获取原始结果
    - `session.scalars(...)`: 执行并获取每行第一列
- Core 偏 SQL 表达式, ORM 偏对象映射, 两者可以混用 (只是构建 SQL 语句对象的方式不同)
- Session 表示一次工作单元
    - identity map: 对象缓存, 同一行数据会映射成一个对象并缓存, 避免重复查询
    - flush, commit, rollback

### 连接与事务

```python
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

engine = create_engine("sqlite+pysqlite:///demo.db", echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False) # ORM 对象变换不会自动 flush, commit 后对象不会过期

with engine.begin() as conn: # begin() 会自动提交或回滚
    conn.execute(
        text("insert into note(text) values (:text)"),
        [{"text": "hello"}, {"text": "world"}],
    )

with engine.connect() as conn: # connect() 给连接, 要自己控制事务
    rows = conn.execute(text("select id, text from note")).all()

with SessionLocal() as session: # Session 面向 ORM, 也可以执行文本 SQL
    result = session.execute(text("select 1")).scalar_one()
```

### ORM 映射

```python
from sqlalchemy import ForeignKey, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True) # Mapped[int] 表示 ORM 映射的类型, mapped_column(...) 表示数据库列的定义
    name: Mapped[str] = mapped_column(String(30), unique=True)
    fullname: Mapped[str | None]
    addresses: Mapped[list["Address"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship(back_populates="addresses")


engine = create_engine("sqlite+pysqlite:///demo.db")
Base.metadata.create_all(engine) # create_all() 会创建所有映射类对应的表
```

### ORM 操作

```python
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session, selectinload

with Session(engine) as session:
    session.add(User(name="spongebob", fullname="Spongebob Squarepants"))
    session.commit()

with Session(engine) as session:
    users = session.scalars(select(User).where(User.name.in_(["spongebob", "sandy"]))).all()
    user = session.scalar(select(User).where(User.name == "spongebob"))

    if user is not None:
        user.fullname = "SpongeBob SquarePants"
        session.commit()

with Session(engine) as session:
    session.execute(
        update(User).where(User.name == "sandy").values(fullname="Sandy Cheeks")
    )
    session.commit()

with Session(engine) as session:
    session.execute(delete(User).where(User.name == "old-user"))
    session.commit()

with Session(engine) as session:
    users = session.scalars(select(User).options(selectinload(User.addresses))).all()
    # selectinload 会在查询 User 时, 预加载 addresses, 避免 N+1 查询
```

### relationship

```python
from sqlalchemy import Column, ForeignKey, Table

# 纯多对多: 学生选课, 中间表只记录 student_id 和 course_id
student_course = Table(
    "student_course",
    Base.metadata,
    Column("student_id", ForeignKey("student.id"), primary_key=True),
    Column("course_id", ForeignKey("course.id"), primary_key=True),
)


class Student(Base):
    __tablename__ = "student"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    # secondary 指向中间表; 访问 student.courses 时得到 Course 列表
    courses: Mapped[list["Course"]] = relationship(
        secondary=student_course,
        back_populates="students",
    )


class Course(Base):
    __tablename__ = "course"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]

    # 和 Student.courses 是同一段关系的反向访问
    students: Mapped[list[Student]] = relationship(
        secondary=student_course,
        back_populates="courses",
    )
```

```python
from datetime import datetime


# 关联对象: 选课关系本身有 enrollment_date, 所以中间表要建成类
class Student(Base):
    __tablename__ = "student"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    # 访问 student.enrollments 得到 Enrollment 列表, 再通过 e.course 找课程
    enrollments: Mapped[list["Enrollment"]] = relationship(back_populates="student")


class Course(Base):
    __tablename__ = "course"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]

    # 访问 course.enrollments 得到选这门课的所有关联记录
    enrollments: Mapped[list["Enrollment"]] = relationship(back_populates="course")


class Enrollment(Base):
    __tablename__ = "enrollment"

    # 两个外键共同组成主键: 同一个学生不能重复选择同一门课
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"), primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id"), primary_key=True)

    # 中间关系自己的业务字段
    enrollment_date: Mapped[datetime]

    # 多个 Enrollment 属于同一个 Student / Course
    student: Mapped[Student] = relationship(back_populates="enrollments")
    course: Mapped[Course] = relationship(back_populates="enrollments")
```

### Alembic

- Alembic 是数据库结构的版本控制工具, migration 描述数据库从版本 A 变到版本 B 要执行哪些操作
- 数据库里会有一张 `alembic_version` 表, 记录当前库跑到了哪个 revision

```bash
# 只在项目初始化时执行一次, 生成 alembic.ini 和 migrations/env.py
alembic init migrations
```

- `migrations/env.py` 要能拿到所有模型的 `Base.metadata`

```python
from app.db import Base
from app import models  # 确保 User / Order 等模型模块被导入, 否则 metadata 里没有表

target_metadata = Base.metadata
```

```bash
# 修改 SQLAlchemy 模型后, 让 Alembic 对比当前数据库结构和Base.metadata
alembic revision --autogenerate -m "create user tables"

# 人工检查生成的 migrations/versions/xxx_create_user_tables.py

# 执行 upgrade(), 把数据库升级到最新版本
alembic upgrade head

# 执行最近一个 revision 的 downgrade(), 回退一版
alembic downgrade -1
```

- 生成的 migration 文件就是两个函数

```python
def upgrade():
    # 正向变更: 加表, 加字段, 建索引
    op.add_column("user", sa.Column("email", sa.String(255), nullable=True))


def downgrade():
    # 反向变更: 撤销 upgrade 的操作
    op.drop_column("user", "email")
```

## 常用后端生态

- `redis`: Redis 客户端
- `loguru`: 日志增强
- `sentry-sdk`: 错误监控
- `opentelemetry-*`: 链路追踪和指标采集

## Uvicorn

```bash
uvicorn main:app --reload # 热重载, 开发用
uvicorn app.main:app --host 0.0.0.0 --port 8000
uvicorn app.main:app --workers 4 # 生产用, 多进程, 与 reload 不兼容
```
