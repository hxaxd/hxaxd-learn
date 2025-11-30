# Python 后端开发

## 参考资料

- 官方文档 - ... - 5

## Pydantic

- 定义模型, 以供类型检查
- 模型还具有许多高级特性, 例如:
    - 模板
    - 动态创建
    - const
    - 默认值

```python
from pydantic import BaseModel


class User(BaseModel):
    id: int # 类型
    name: str = 'Jane Doe' # 默认值
    key = Column(String(63), unique=True) # 从实例属性中获取类型


user = User(id='123', name='John Doe')
User.model_validate({'id': 123, 'name': 'John Doe'}) # 类型检查
User.model_validate_json('{"id": 123, "name": "John Doe"}') # 类型检查
User.model_dump() # 转换为字典
User.model_dump_json() # 转换为 json
```

## FastAPI

- 依赖 OpenAPI 与 Pydantic 库实现
    - 数据验证
    - 自动生成交互式文档(可以自定义任何基于 OpenAPI 的文档)
- 可使用 `async` 与 `await` 实现异步
- 可以定义元数据, 提供给文档
- 集成 HTTPX 库进行测试

```python
from fastapi import FastAPI

app = FastAPI() # 创建一个 FastAPI 实例

@app.get("/") # 路由
async def root(): # 异步函数
    return {"message": "Hello World"} # 返回 json
```

- 一个 url `协议://主机:端口/路径` 路径亦称为端点 / 路由
- 使用 HTTP 方法来区分不同的操作
    - GET - 查询
    - POST - 创建
    - PUT - 更新
    - DELETE - 删除

### 路径参数

- 对于路径参数函数的类型重载, 注意声明顺序决定检查顺序
- 可以使用 `Path` 对象来声明路径参数类型, 默认值等

```python
@app.get("/items/{id}") # 路径参数
async def read_item(id: int): # fastapi 会进行类型检查
    return {"item_id": id}
from enum import Enum

# 声明一个枚举类进行检查
class ModelName(str, Enum): # 继承 str 的原因是为了兼容生成文档
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"
```

### 查询参数

- 形如 `/items/?skip=0&limit=10`
    - `/items/` 会使用默认值
    - 可使用 `None` 类型表示可选参数
    - 也可以是 `bool` 类型, 会自动转换为 `True` 和 `False`
- 这回不依赖声明顺序了, 检查查询参数来决定使用哪个函数
- 可以使用 `Query` 对象来声明查询参数类型, 默认值等
- `Annotated[FilterParams, Query()]` 用一个模型声明查询参数类型

```python
from fastapi import FastAPI

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10): # 没同名, 代表查询参数
    return fake_items_db[skip : skip + limit]
```

### 请求体

- 直接实现类型检查 + JSON
- 和上面的可以叠加
- 也可以用多个单独的参数来实现
- `Annotated[class, Cookie()]` 声明 Cookie 参数
    - Header / Cookie / Query / Path 同理
- 请求体不是 JSON 格式的, 而是表单格式的
    - 使用 `Form` 对象来声明表单参数
    - `Annotated[class, From()]` 亦可
    - 也可以使用 `File` 对象来声明文件参数
    - 也可以使用 `UploadFile` 对象来声明文件参数类型

```python
from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

wsl --set-default-version 2
1
app = FastAPI()


@app.post("/items/")
async def create_item(item: Item): # 请求体
    return item
```

#### 更新

- 可以单独定义需要更新的部分的模型, 这样就不会覆盖所有字段

### 响应

- `jsonable_encoder` 可以将任意类型转换为 JSON 格式兼容

```python
@app.post("/user/", response_model=UserOut) # 用装饰器声明响应模型
@app.post("/items/", status_code=201) # 声明状态码
```

#### 后台任务

- 可以使用 `BackgroundTasks` 对象来声明后台任务
    - 后台任务会在响应函数返回后执行

```python
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


def write_notification(email: str, message=""): # 后台任务
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification") # 进行后台任务
    return {"message": "Notification sent in the background"}
```

#### 静态文件

- 事实建立独立的 app 来处理静态文件请求

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static") # 挂载静态文件
# 指定路径, 实例, 名称
```

### 依赖注入

- 可以使用 `Depends` 对象来声明依赖
    - 依赖可以是任何可调用对象, 包括函数, 类, 协程函数
- 可以嵌套依赖, 菱形依赖自动处理
- 路径装饰器也可以声明依赖, 依赖会被调用 (比如用来判断请求头), 但依赖的值不会被传递给响应函数
    - 相应的 `app` 实例也可以声明依赖, 相当于为所有路由声明依赖

```python
async def get_db(): # 这么声明的依赖会停在 yield 处, 并将 db 传递给响应函数
    db = DBSession()
    try:
        yield db
    finally: # 直到响应函数返回后, 才会执行 finally 块
        db.close()
```

```python
from typing import Union

from fastapi import Depends, FastAPI

app = FastAPI()


async def common_parameters(
    q: Union[str, None] = None, skip: int = 0, limit: int = 100
):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons
```

### 中间件

- 自己的装饰器

```python
import time

from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

### 安全

- 可以使用 `CORSMiddleware` 来添加 CORS 支持 (指定允许的域名, 方法等)
- 基于 OAuth2 规范实现安全认证
- fastapi 会接收账号密码, 验证后返回 token
    - 前端保存 token, 每次请求时在请求头添加 Authorization : "Bearer+token"
    - 后端验证 token, 并返回用户信息
- 使用 passlib 库来哈希密码
- 使用 pyJWT 库来生成 JWT 令牌

```python
from typing import Union

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # 验证器


class User(BaseModel): # 声明用户模型
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


def fake_decode_token(token): # 返回用户
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


async def get_current_user(token: str = Depends(oauth2_scheme)): # 验证函数, 依赖于验证器
    user = fake_decode_token(token)
    return user


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)): # 依赖于验证函数
    return current_user
```

```python
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()): # 登陆函数, 表单依赖于 OAuth2PasswordRequestForm
    # 注意, 表单模型不能自定义, 是 OAuth2 规范约定的模型
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password) # 哈希密码, 一般使用 passlib 库
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}
```

### 架构

- 可以使用 `APIRouter` 来声明本文件的路由组 (app 的分身)
    - `router = APIRouter()`
    - `@router.get("/")`
- app 用 `include_router` 来包含路由组
- 可以使用 `prefix` 和 `tags` 来声明路由组的前缀和标签
    - `router = APIRouter(prefix="/users", tags=["users"])`
    - 亦可 `app.include_router(router, prefix="/admin", tags=["admin"])`

```python
from fastapi import Depends, FastAPI

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

## mysql-connector-python

- 一个 mysql 数据库的 python 驱动程序
- 几乎是 sql 语句的一对一实现

## SQLAlchemy

- 一个 ORM 框架, 在连接库上抽象了操作接口

### 连接

```python
from sqlalchemy import create_engine
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True) # 内存中的 sqlite
# 数据库+驱动://用户名:密码@主机:端口/数据库名
# echo=True 打印 sql 语句

# 不多介绍文本 SQL
with engine.connect() as conn: # 通过连接对数据库进行操作
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"), 
        [{"x": 1, "y": 1}, {"x": 2, "y": 4}], 
    ) # 操作会被缓存, 直到 commit 才会被执行
    conn.commit()

result = conn.execute(...).all # 结果作为元组返回

with Session(engine) as session: # 对 connect 的封装
    result = session.execute(...)
    session.commit() # 提交事务
```

### 对象关系映射

```python
from sqlalchemy import MetaData
metadata_obj = MetaData() # 元数据对象

from sqlalchemy import Table, Column, Integer, String
user_table = Table( # 声明表结构
    "user_account", # 表名
    metadata_obj, # 元数据对象
    Column("id", Integer, primary_key=True), # 声明列
    Column("name", String(30)), 
    Column("fullname", String), 
)
print(user_table.c.keys) # 列名

Column("user_id", ForeignKey("user_account.id"), nullable=False) # 外键

# 更好的方法
from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase): # 声明基类
    pass

class User(Base): # 声明模型
    __tablename__ = "user_account" # 表名

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String)

    addresses = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    ) # 关系

some_table = Table("some_table", metadata_obj, autoload_with=engine) # 自动加载表结构
```

### 操作

```python
from sqlalchemy import insert, select, update, delete
stmt = insert(user_table).values(x=6, y=8, z=10) # 插入语句

stmt = select(user_table).where(...) # 查询语句
stmt = select(user_table).where(...).join_from(another_table) # 查询语句

stmt = update(user_table).where(...).values(x=6, y=8) # 更新语句
stmt = delete(user_table).where(...) # 删除语句
# 还有很多, 大体与 SQL 语句对应

with Session(engine) as session: # 操作
    session.execute(stmt)
    session.commit()
```

### ORM 操作

```python
from sqlalchemy.orm import Session

with Session(engine) as session: # 操作
    session.add_all([User(name="spongebob", fullname="Spongebob Squarepants"), ...]) # 插入
    session.flush() # 缓存
    session.commit() # 提交

    session.query(User).filter(User.name.in_(["sandy", "susan"])).all() # 查询
    session.query(User).filter(User.name == "sandy").first() # 查询
    session.query(User).filter(User.name.like("%ed")).all() # 查询

    session.query(User).filter(User.name == "sandy").name = "666" # 更新
    session.delete(result) # 删除
    session.commit() # 提交

    session.rollback() # 回滚
    session.close() # 关闭
```

### `relationship`

- 可以定义延迟加载, 预加载, 级联删除等特性
    - `cascade="all, delete-orphan"` 级联删除
- 正常声明一对多
    - `uselist=False` 表示单个对象而非列表
    - 辅以外键约束, 实现其它关系

```python
class Parent(Base):
    __tablename__ = 'parents'
    id = Column(Integer, primary_key=True)
    children = relationship("Child", back_populates="parent")

class Child(Base):
    __tablename__ = 'children'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parents.id'))
    parent = relationship("Parent", back_populates="children")
```

- 多对多关系需要使用关联模型定义 (中间表)

```python
class Enrollment(Base):
    __tablename__ = 'enrollments'
    student_id = Column(Integer, ForeignKey('students.id'), primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), primary_key=True)
    enrollment_date = Column(DateTime)
    # 定义与 Student 和 Course 的关系
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    enrollments = relationship("Enrollment", back_populates="student")

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    enrollments = relationship("Enrollment", back_populates="course")
```

## Uvicorn

- 基于 ASGI 协议的异步 web 服务器 (不同于 WSGI)

```bash
uvicorn filename:objname # 启动服务器

# --reload 热重载
# --port 端口
# --host IP
# --workers 进程数
# --log-level 日志级别
# --log-config 日志文件位置
# --ssl-keyfile=SSL 密钥文件 --ssl-certfile=SSL 证书文件
```
