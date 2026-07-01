# Python

## 参考资料

- 流畅的 Python
- Codex

## 工具

### Python Install Manager

- Windows 上官方推荐从 python.org 或 Microsoft Store 安装 Python Install Manager

```powershell
py # 启动默认 Python
py -V:3.14 # 指定运行 Python 3.14
py list # 查看已安装运行时
py list --online # 查看可安装运行时
py install 3.14 # 安装指定版本
py install --update # 更新由 install manager 管理的运行时
py uninstall 3.13 # 卸载指定版本
py -m pip --version # 用指定解释器运行模块
```

### `venv` 与 `pip`

- `venv` 是标准库模块, 用来创建轻量虚拟环境
- `pip` 是包安装器, 最稳的调用方式是 `python -m pip`, 这样能确保操作的是当前解释器

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install rich
python -m pip freeze > requirements.txt
deactivate
```

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install rich
python -m pip freeze > requirements.txt
deactivate
```

### uv

#### 安装

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
uv --version
```

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version
```

#### 项目管理

```bash
uv init demo # 创建项目
cd demo
uv python pin 3.14 # 固定项目 Python 版本
uv add rich # 写入依赖并同步环境
uv add --dev pytest ruff pyright # 写入开发依赖
uv run python -m demo
uv run pytest
uv lock # 生成 uv.lock
uv sync # 按锁文件重建环境

uv remove rich # 删除依赖
uv tree # 查看依赖树
```

#### Python 版本管理

```bash
uv python list
uv python install 3.12 3.13 3.14
uv python pin 3.14
uv venv --python 3.14
uv run --python 3.14 python -V
uv run --python pypy@3.10 python -V
```

#### 工具机制

```bash
uvx ruff check .
uv tool run black --check .
uv tool install ruff
uv tool install pyright
uv tool list
uv tool uninstall ruff
```

#### `pip` 兼容层

```bash
uv venv
uv pip install -r requirements.txt
uv pip compile requirements.in -o requirements.txt
uv pip sync requirements.txt
```

#### 构建与发布

```bash
uv build
uv publish
```

### Conda 家族

- Anaconda: 大而全, 适合教学和开箱即用, 但默认安装体积大
- Miniconda: Anaconda 官方的最小 conda 安装器, 只带 conda, Python 和少量基础包
- Miniforge3: conda-forge 社区的最小安装器
- Mamba: conda 环境管理 CLI, 命令大多和 conda 接近, 解析速度通常更快
- `conda` 是命令, `conda-forge` 是包源, 当前默认源可以用 `conda config --show channels` 看

```bash
conda create -n py314 python=3.14
conda activate py314
conda install -c conda-forge rich # 指定源安装
conda env export > environment.yml # 导出环境
conda env list
conda deactivate
conda env remove -n py314
```

- `environment.yml` 用来描述环境:

```yaml
name: demo
channels:
  - conda-forge
dependencies:
  - python=3.14
  - rich
  - pip
  - pip:
      - typer
```

### Pixi

- Pixi 是基于 conda-forge / prefix.dev 生态的项目环境工具
- 相比 conda, Pixi 更项目化, 相比 uv, Pixi 更擅长非 Python 依赖和多语言依赖

```powershell
powershell -ExecutionPolicy ByPass -c "irm -useb https://pixi.sh/install.ps1 | iex"
pixi --version
```

```bash
pixi init demo
cd demo
pixi add python rich
pixi task add start "python -c \"import rich, print('ok')\"" # 添加任务
pixi run start # 运行任务
pixi shell # 进入环境
pixi global install ripgrep fd # 安装全局命令
```

### 常用工具

- Ruff: lint, format, import 排序和一部分自动修复
- Pyright: 静态类型检查器
- pre-commit: 管 Git hook
- nox: 跑测试矩阵, 比如同一套测试在 Python 3.12/3.13/3.14 上都跑一遍
- httpie: 命令行 HTTP 客户端
- pip-audit: 检查依赖里有没有已知安全漏洞
- py-spy: Python 采样分析器
    - 火焰图
    - 打印线程栈
    - 函数调用次数和耗时
- direnv: 进目录自动加载环境变量, 比如自动设置 `VIRTUAL_ENV`, API key, 私有源地址

## 模块, 包与打包

### 模块与包

#### 模块

- 一个 `.py` 文件就是一个模块, 文件名就是模块名
- 模块可以被 `import` 导入, 也可以作为脚本直接运行
- `if __name__ == "__main__":` 用来区分当前文件是被导入, 还是被直接运行
- 不要把文件命名为 `json.py`, `typing.py`, `requests.py` 这类容易遮蔽标准库或三方库的名字

#### 包

- 一个目录包含 `__init__.py` 时就是常规包
- `__init__.py` 的作用:
    - 导入包时会先执行它, 比如 `import package` 会执行 `package/__init__.py`
    - 可以在里面整理包的对外 API, 比如 `from .core import Client`, 让用户可以写 `from package import Client`
    - 可以定义 `__all__`, `__version__` 等包级别信息
- 没有 `__init__.py` 的目录也可能作为 namespace package 工作
    - namespace package 的意思是: 同一个顶层导入包名可以分散在多个安装位置里
    - 常见场景是多个发行包共同贡献同一个顶层包名
    - 比如 `pip install acme-core` 提供 `acme/core.py`, `pip install acme-auth` 提供 `acme/auth.py`, 它们都挂在同一个 `acme` 顶层包下面
    - 用户使用时可以分别导入 `import acme.core` 和 `import acme.auth`

#### 运行与导入规则

- `sys.path` 决定 Python 从哪里找模块和包, 通常包括脚本目录, 环境变量 `PYTHONPATH`, 标准库和 `site-packages`
- shell 当前目录主要影响两件事: Python 从哪里找顶层包, 以及 `open("file.txt")` 这种普通相对文件路径
- `python -m package.module` 会先从 `sys.path` 中找到 `package`, 再把 `module` 当作包内模块执行
    - 显式相对导入, 如 `from . import sibling`, 不是按 shell 当前目录算, 而是按 `__package__` 这个包上下文算
    - 直接运行 `python package/module.py` 时, 这个文件常常只被当作普通脚本, `__package__` 为空, `from . import sibling` 就容易失败

### `src` 布局

- `src` 布局能避免测试时误导入项目根目录里的源码, 更接近真实安装后的状态
- distribution package 是发布到 PyPI 的包名, import package 是 `import` 的模块名, 两者可以不同
    - `pip install beautifulsoup4`
    - `from bs4 import BeautifulSoup`

### `pyproject.toml`

```toml
# 声明构建后端和构建依赖
[build-system]
requires = ["hatchling >= 1.26"]
build-backend = "hatchling.build"

# 声明标准项目元数据
[project]
name = "demo-pkg"
version = "0.1.0"
description = "A small Python package"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
  "rich>=13",
]

# 声明用户可安装的 extra
[project.optional-dependencies]
cli = ["typer>=0.12"]

# 声明开发依赖组, 不会进入构建后的包元数据
[dependency-groups]
dev = ["pytest>=8", "ruff>=0.5", "pyright>=1.1"]

# 声明可执行脚本, 让用户安装后能直接在 shell 里运行
[project.scripts]
demo = "demo_pkg.cli:main"

# 声明工具配置
[tool.ruff]
line-length = 100
```

- build backend 常见选择:
    - Hatchling: 新项目友好, 纯 Python 包很顺
    - Setuptools: 兼容最广, 历史项目和 C 扩展常见
    - Flit: 简洁发布纯 Python 库
    - PDM backend: PDM 生态
    - `uv_build`: uv 生态的新构建后端

### 构建一个包

```bash
python -m pip install -U build twine
python -m build
twine check dist/*
twine upload dist/*
```

- `python -m build` 通常产出两个文件:
    - sdist: `dist/name-version.tar.gz`, 源码分发包
    - wheel: `dist/name-version-py3-none-any.whl`, 构建分发包, 安装更快
- 库项目的 `dependencies` 不要锁死全部间接依赖, 否则会让使用者无法组合

## 标准库

### 诊断

- `inspect`: 运行时观测函数, 类, 签名, 源码
- `traceback`: 异常堆栈
- `warnings`: 发出不中断程序的警告, 常用于库的兼容提示
- `tracemalloc`: 跟踪内存分配
- `logging`: 日志系统

### 性能

- `cProfile` -> `pstats`: 性能分析 -> 展示, 找程序慢在哪里
- `timeit`: 给小段代码计时, 做微基准测试
- `time`: 时间戳, 睡眠, 性能计时, 重点知道 `perf_counter()`

### 功能

- `pickle`: Python 对象序列化, 只反序列化可信数据 (因为本质是按指令重建对象)
- `importlib`: 动态导入模块
- `pkgutil`: 包发现和模块遍历, 常见于插件系统
- `decimal`: 十进制定点数, 适合金额等不能接受二进制浮点误差的场景
- `copy`: 浅拷贝和深拷贝, 重点知道 `copy.deepcopy()`
- `sqlite3`: 嵌入式 SQLite 数据库

### 类型

- `typing`: 类型标注
- `collections`: 增强容器
- `types`: 运行时创建类型
- `itertools`: 惰性迭代工具, 被调用时生成
- `functools`: 函数工具, 主要是一堆装饰器和高阶函数, 比如 `lru_cache`, `partial`, `wraps`
- `dataclasses`: 数据类, 自动生成 `__init__`, `repr`, `eq`
- `enum`: 枚举

## 常用三方库

- tqdm: 进度条
- python-dotenv: 从 `.env` 加载环境变量
- PyInstaller: 把 Python 应用打包成单目录或单文件可执行程序
- pytest: 测试框架

## 并发与并行

并发这一章先不要从 API 名字开始背。先抓住一个模型:

- 任务: 要做的一段工作, 可以是函数, 协程, 外部命令, 网络连接
- 执行单元: 让任务向前跑的东西, 比如 task, thread, process, interpreter
- 调度器: 决定现在推进谁, 比如 event loop, OS scheduler, executor
- 等待点: 当前任务主动或被动停下来的地方, 比如 `await`, `join()`, `Future.result()`, `Queue.get()`
- 通信方式: 任务之间传递结果和状态, 比如返回值, queue, pipe, shared memory, context variable
- 生命周期: 任务怎么启动, 怎么等它结束, 怎么取消, 怎么处理异常, 怎么清理资源

并发是多个任务的生命周期重叠。并行是多个任务在同一时刻真的占用多个 CPU 核执行。异步 I/O, 多线程, 多进程都能做并发, 但它们的基本模型完全不同。

### GIL

- GIL 是 CPython 的全局解释器锁
- GIL 不阻止线程并发等待 I/O, 因为阻塞 I/O 和很多 C 扩展会释放 GIL
- 多进程可以绕过 GIL, 因为每个进程有自己的解释器和自己的 GIL
- Python 3.14 的 `InterpreterPoolExecutor` 使用多个子解释器, 每个解释器有自己的 GIL
- CPython 3.13 开始提供 free-threaded 构建作为关闭 GIL 的实验方向

### `asyncio`

- `async def` 定义的是可暂停函数
- 调用 `async def` 不会立即运行函数体, 只会得到 coroutine object
- `await` 是暂停点, 当前协程把控制权交还给 event loop
- event loop 是调度器, 负责推进已经就绪的协程
- `Task` 是协程的运行包装, 把 coroutine 交给 event loop 推进

#### API

- `asyncio.run(coro)`: 创建 event loop, 跑入口协程, 结束后关闭 loop
- `asyncio.create_task(coro)`: 把协程包装成 Task, 让它开始被 event loop 调度
- `Task`: 正在运行或即将运行的协程任务, 能取结果, 取消, 查看状态
- `asyncio.TaskGroup`: 结构化并发, 一组任务作为一个生命周期单元
- `asyncio.gather()`: 并发等待多个 awaitable, 通常按输入顺序返回结果
- `asyncio.wait()`: 等一批任务达到某个条件, 返回 done 和 pending 两组
- `asyncio.as_completed()`: 谁先完成就先处理谁
- `asyncio.sleep()`: 非阻塞睡眠, 让 event loop 去跑别的任务
- `asyncio.Queue`: 协程之间传消息, `put()` 放入, `get()` 取出, `task_done()` 标记完成, `join()` 等所有任务完成
- `asyncio.Lock`: 协程互斥锁, 保护共享状态
- `asyncio.Event`: 一次性或可反复设置的通知信号
- `asyncio.Condition`: 条件变量, 用来等共享状态满足某个条件
- `asyncio.Semaphore`: 限制同时进入某段代码的任务数量
- `asyncio.Barrier`: 等固定数量任务都到达后一起放行
- `asyncio.to_thread()`: 在默认线程池中跑同步阻塞函数, 避免卡住 event loop
- `loop.run_in_executor()`: 指定线程池或进程池执行同步函数
- `asyncio.create_subprocess_exec()`: 异步启动和等待子进程

#### 常见坑

- 在 async 函数里调用 `time.sleep()` 会阻塞整个 event loop
- 调用 async 函数但忘记 `await` 或 `create_task()`, 协程不会真正运行
- 无限创建 task 会把内存, 连接池, 下游服务打满
- 捕获 `CancelledError` 后不继续抛出, 会破坏取消语义
- `gather()` 很方便, 但复杂任务树更推荐 `TaskGroup`

### `threading`: 线程与共享内存

线程是操作系统调度的执行流。一个 Python 进程里可以有多个线程, 它们共享同一份进程内存。共享内存让通信很方便, 也让竞态条件很容易出现。

`threading` 的基本流程是:

- 把一个普通函数交给 `Thread(target=...)`
- 调用 `start()` 后, 目标函数在新线程里执行
- 主线程调用 `join()` 等它结束
- 多线程读写共享对象时用锁, 条件变量, 事件, 信号量等同步原语协调

#### API 先解释

- `Thread`: 创建线程对象
- `start()`: 真正启动线程, 目标函数开始运行
- `join()`: 等线程结束
- `Lock`: 互斥锁, 同一时间只允许一个线程进入临界区
- `RLock`: 可重入锁, 同一线程可以重复获得同一把锁
- `Condition`: 条件变量, 让线程等某个共享状态满足条件
- `Semaphore`: 计数信号量, 限制同时访问某资源的线程数
- `BoundedSemaphore`: 带上界检查的信号量, 多释放会报错
- `Event`: 一个布尔信号, `set()` 后唤醒等待者
- `Barrier`: 等固定数量线程都到达某点后一起继续
- `Timer`: 延迟一段时间后在线程里执行函数
- `local`: 线程本地存储, 每个线程看到自己的值
- `current_thread()`: 当前线程对象
- `get_ident()`: 当前线程的 Python 线程标识
- `get_native_id()`: 当前线程的系统线程 ID

#### 最小闭环代码

```python
import threading
import time

counter = 0
lock = threading.Lock()
rlock = threading.RLock()
condition = threading.Condition()
event = threading.Event()
barrier = threading.Barrier(3)
sem = threading.Semaphore(2)
bounded = threading.BoundedSemaphore(1)
local_data = threading.local()
items: list[str] = []


def nested() -> None:
    with rlock:
        print("RLock can be acquired again by the same thread")


def worker(i: int) -> None:
    global counter
    local_data.name = f"worker-{i}"  # 每个线程都有自己的 local_data.name

    print(
        local_data.name,
        threading.current_thread().name,
        threading.get_ident(),
        threading.get_native_id(),
    )

    pos = barrier.wait()  # 三个 worker 都到这里之后一起继续
    print(local_data.name, "passed barrier", pos)

    event.wait()  # 等 Timer 调用 event.set()

    with sem:  # 同时最多两个线程进入
        time.sleep(0.03)
        print(local_data.name, "entered semaphore")

    with lock:
        old = counter
        time.sleep(0)  # 故意制造切换机会
        counter = old + 1

    with rlock:
        nested()

    with condition:
        items.append(local_data.name)
        condition.notify()  # 通知主线程状态变了


timer = threading.Timer(0.1, event.set)  # 0.1 秒后放行所有 event.wait()
threads = [
    threading.Thread(target=worker, args=(i,), name=f"T{i}")
    for i in range(3)
]

bounded.acquire()
bounded.release()
try:
    bounded.release()  # BoundedSemaphore 检查释放次数是否超过初始值
except ValueError as exc:
    print("bounded catches over-release:", exc)

timer.start()
for t in threads:
    t.start()

with condition:
    condition.wait_for(lambda: len(items) >= 3)  # 自动重复检查条件
    print("condition collected:", items)

for t in threads:
    t.join()
timer.join()
print("counter =", counter)
```

#### 底层意义

- 线程由操作系统调度, Python 不能精确控制切换点
- 线程共享进程地址空间, 所以全局变量和堆对象都能被多个线程访问
- 共享可变对象必须设计同步, 否则会出现竞态
- 常规 CPython 中线程受 GIL 限制, 不适合纯 Python CPU 密集并行
- I/O 阻塞时通常会释放 GIL, 所以线程对阻塞 I/O 有用

#### 什么时候用

适合:

- 同步 HTTP SDK, 数据库 SDK, 文件 I/O 等阻塞调用
- 后台日志刷新, 指标上报, 文件轮询
- 和现有同步代码集成
- 少量共享状态明确的 worker 模型

不适合:

- 大量复杂共享状态
- 纯 Python CPU 密集计算
- 希望强隔离或防止第三方库崩溃污染主进程
- 不可控长任务塞进长期线程池

#### 常见坑

- 以为 GIL 能保护业务不出竞态
- 拿锁顺序不一致导致死锁
- 线程没有退出信号, 进程关闭时卡住
- daemon thread 被强行结束, 清理逻辑没机会执行
- 在持锁状态下调用不可控外部函数

### `queue`: 线程安全队列与背压

`queue` 解决的是线程之间怎么交接任务。生产者 `put()` 任务, 消费者 `get()` 任务。队列内部已经用锁和条件变量保证线程安全。

队列里有一个非常重要的计数: unfinished tasks。

- 每次 `put()` 一个任务, 计数加一
- 消费者处理完一个 `get()` 出来的任务后调用 `task_done()`, 计数减一
- `join()` 阻塞直到计数归零

这就是 `Queue.join()` 的意义: 等所有放进去的任务都被处理完。

#### API 先解释

- `Queue(maxsize=0)`: FIFO 队列, 可用 `maxsize` 做背压
- `LifoQueue`: 后进先出队列, 像栈
- `PriorityQueue`: 优先级队列, 取出最小优先级项
- `SimpleQueue`: 简化队列, 没有任务完成跟踪
- `put()`: 放入元素, 满时可阻塞
- `put_nowait()`: 不等待, 满了就抛 `Full`
- `get()`: 取出元素, 空时可阻塞
- `get_nowait()`: 不等待, 空了就抛 `Empty`
- `task_done()`: 标记一个取出的任务处理完成
- `join()`: 等所有任务都被 `task_done()`
- `Full`: 非阻塞放入失败
- `Empty`: 非阻塞取出失败
- `shutdown()`: Python 3.13+ 的队列关闭机制

#### 最小闭环代码

```python
import queue
import threading
import time

work: queue.Queue[int | None] = queue.Queue(maxsize=2)


def worker() -> None:
    while True:
        try:
            item = work.get(timeout=0.5)
        except queue.Empty:
            print("no work for a while")
            continue

        try:
            if item is None:
                print("stop worker")
                return
            print("process", item)
            time.sleep(0.02)
        finally:
            work.task_done()


t = threading.Thread(target=worker)
t.start()

for i in range(3):
    work.put(i)  # maxsize=2, consumer 慢时 producer 会被背压

try:
    work.put_nowait(99)
except queue.Full:
    print("queue full")

work.put(None)
work.join()
t.join()

lifo: queue.LifoQueue[str] = queue.LifoQueue()
lifo.put("first")
lifo.put("last")
print(lifo.get())  # last

priority: queue.PriorityQueue[tuple[int, str]] = queue.PriorityQueue()
priority.put((10, "low"))
priority.put((1, "high"))
print(priority.get())  # (1, 'high')

simple: queue.SimpleQueue[str] = queue.SimpleQueue()
simple.put("no task_done/join")
print(simple.get())

if hasattr(work, "shutdown"):
    work.shutdown()  # Python 3.13+, 关闭队列后继续 put/get 会进入关闭语义
```

#### 什么时候用

适合:

- 一个线程生产任务, 多个线程消费任务
- 限制任务积压, 用 `maxsize` 给系统背压
- 清晰表达任务处理完成的边界

不适合:

- 协程之间通信, 用 `asyncio.Queue`
- 进程之间通信, 用 `multiprocessing.Queue`
- 需要复杂路由, 重试, 持久化的生产级任务系统

### `concurrent.futures`: 提交函数, 拿 Future

`concurrent.futures` 把线程池, 进程池, 解释器池统一成一个模型:

- Executor 管一组 worker
- `submit(fn, *args)` 把函数交给 worker 执行
- 立刻返回 `Future`
- `Future` 是未来结果的占位对象
- 主线程可以 `result()` 等结果, `cancel()` 取消未开始的任务, `as_completed()` 谁先结束就处理谁

这个模块适合把普通同步函数并发执行, 不要求你自己管理线程或进程生命周期。

#### API 先解释

- `Executor.submit()`: 提交一个函数调用, 返回 Future
- `Executor.map()`: 类似内置 `map`, 但并发执行
- `Executor.shutdown()`: 关闭池, `with` 会自动调用
- `Future.result()`: 等任务完成并返回结果, 任务抛异常则这里重新抛
- `Future.exception()`: 取任务异常
- `Future.cancel()`: 尝试取消还没开始的任务
- `Future.done()`: 是否结束
- `Future.running()`: 是否正在运行
- `Future.add_done_callback()`: 完成时回调
- `wait()`: 等一批 Future 达到条件
- `as_completed()`: 按完成顺序迭代 Future
- `ThreadPoolExecutor`: 线程池, 适合同步 I/O
- `ProcessPoolExecutor`: 进程池, 适合 CPU 密集
- `InterpreterPoolExecutor`: Python 3.14+ 解释器池, 隔离性强于线程, 通信成本类似序列化

#### 最小闭环代码

```python
from concurrent.futures import (
    FIRST_COMPLETED,
    ProcessPoolExecutor,
    ThreadPoolExecutor,
    as_completed,
    wait,
)
import time


def io_job(x: int) -> int:
    time.sleep(0.05)
    return x * 10


def cpu_job(x: int) -> int:
    return x * x


def on_done(fut) -> None:
    print("callback result:", fut.result())


def thread_pool_demo() -> None:
    with ThreadPoolExecutor(max_workers=2, thread_name_prefix="io") as ex:
        future = ex.submit(io_job, 1)
        future.add_done_callback(on_done)
        print("running/done:", future.running(), future.done())
        print("single result:", future.result(timeout=1))

        bad = ex.submit(lambda: 1 / 0)
        try:
            bad.result()
        except ZeroDivisionError:
            print("exception object:", type(bad.exception()).__name__)

        print("map keeps input order:", list(ex.map(io_job, [2, 3, 4])))

        futures = [ex.submit(io_job, i) for i in [5, 6, 7]]
        done, pending = wait(futures, return_when=FIRST_COMPLETED)
        print("first completed:", [f.result() for f in done])

        for f in as_completed(pending):
            print("later completed:", f.result())

    with ThreadPoolExecutor(max_workers=1) as ex:
        blocker = ex.submit(time.sleep, 0.1)
        queued = ex.submit(io_job, 99)
        print("cancel queued before it starts:", queued.cancel())
        blocker.result()
        print("queued cancelled/done:", queued.cancelled(), queued.done())


def process_pool_demo() -> None:
    with ProcessPoolExecutor(max_workers=2) as ex:
        print("process results:", list(ex.map(cpu_job, [1, 2, 3])))


if __name__ == "__main__":
    thread_pool_demo()
    process_pool_demo()
```

Python 3.14+ 可以这样尝试解释器池:

```python
from concurrent.futures import InterpreterPoolExecutor


def square(x: int) -> int:
    return x * x


with InterpreterPoolExecutor(max_workers=2) as ex:
    print(list(ex.map(square, [1, 2, 3])))
```

#### 底层意义

- `ThreadPoolExecutor` 的 worker 是线程, 共享内存, 受 GIL 影响
- `ProcessPoolExecutor` 的 worker 是进程, 参数和结果需要 pickle
- `InterpreterPoolExecutor` 的 worker 是线程里的独立解释器, 可多核并行, 但解释器之间隔离
- `Future` 是结果通道, 也是异常传播通道

#### 常见坑

- 在线程池 worker 里等待同一个线程池的新任务, 容易死锁
- 进程池任务函数必须能被子进程导入
- lambda, 局部函数, REPL 里定义的函数不适合交给进程池
- 进程池传大对象会有序列化和复制成本
- `Future.result()` 不设置超时可能永久卡住

### `multiprocessing`: 进程级并行与隔离

进程是操作系统的资源隔离单位。每个进程有自己的地址空间, 自己的 Python 解释器, 自己的 GIL。多进程能让纯 Python CPU 密集任务真正使用多个核心, 但通信比线程重得多。

`multiprocessing` 的基本流程是:

- 主进程创建子进程
- 子进程导入模块并运行目标函数
- 进程之间不能直接共享普通 Python 对象
- 参数和结果通常通过 pickle 序列化
- 需要用 Queue, Pipe, Value, Array, Manager, shared memory 等机制通信

#### API 先解释

- `Process`: 创建进程
- `start()`: 启动进程
- `join()`: 等进程结束
- `Queue`: 进程间任务或消息队列
- `Pipe`: 两端连接的管道, 适合两个进程通信
- `Pool`: 进程池, 批量执行函数
- `Manager`: 管理器进程, 提供共享 dict/list 等代理对象
- `Value`: 共享单个 ctypes 值
- `Array`: 共享 ctypes 数组
- `Lock`: 跨进程锁
- `Event`: 跨进程信号
- `get_context()`: 选择启动方式并得到上下文
- `set_start_method()`: 设置全局启动方式, 只能早期调用一次
- `spawn`: 启动全新 Python 解释器, 跨平台, 干净但慢
- `fork`: POSIX 复制当前进程, 快但多线程程序里危险
- `forkserver`: POSIX 上通过单线程 server fork, Python 3.14 起是很多 POSIX 平台默认方式

#### 最小闭环代码

```python
import multiprocessing as mp


def square(x: int) -> int:
    return x * x


def worker(q, conn, value, arr, lock, event) -> None:
    event.wait()  # 等主进程发开始信号

    with lock:
        value.value += 1
        arr[0] = 42

    q.put("message from child")
    conn.send("pipe from child")
    conn.close()


def main() -> None:
    # 也可以用 mp.set_start_method("spawn") 做全局设置, 但它只能在程序早期调用一次
    ctx = mp.get_context("spawn")

    q = ctx.Queue()
    parent_conn, child_conn = ctx.Pipe()
    value = ctx.Value("i", 0)
    arr = ctx.Array("i", [0, 0])
    lock = ctx.Lock()
    event = ctx.Event()

    p = ctx.Process(
        target=worker,
        args=(q, child_conn, value, arr, lock, event),
    )
    p.start()
    event.set()

    print(q.get())
    print(parent_conn.recv())
    p.join()
    print("shared:", value.value, list(arr), "exit:", p.exitcode)

    with ctx.Pool(2) as pool:
        print(pool.map(square, [1, 2, 3]))

    with ctx.Manager() as manager:
        d = manager.dict()
        d["x"] = 1
        print(dict(d))


if __name__ == "__main__":
    main()
```

#### 底层意义

- 每个进程都有独立地址空间, 所以不会像线程那样随便共享对象
- 进程间通信通常是序列化 + 管道/队列
- 进程崩溃一般不会直接带崩主进程
- 创建进程和跨进程通信都比线程重

#### 什么时候用

适合:

- 纯 Python CPU 密集任务
- 任务彼此独立
- 需要隔离第三方库崩溃
- 子任务足够重, 能摊平启动和序列化成本

不适合:

- 高频小任务
- 大量共享复杂对象
- Web 请求路径里临时创建进程
- 需要低延迟交互的任务

### `multiprocessing.shared_memory`: 共享大块原始内存

`shared_memory` 只解决一个问题: 大块数据不要在进程间复制来复制去。

它共享的是一段原始 bytes, 不是共享 Python 对象。你需要自己决定这段 bytes 表示什么, 谁写, 谁读, 何时释放, 是否需要锁。

#### API 先解释

- `SharedMemory(create=True, size=n)`: 创建共享内存块
- `SharedMemory(name=...)`: 在另一个进程 attach 到已有共享内存
- `shm.buf`: memoryview, 读写原始字节
- `shm.name`: 跨进程传递的名字
- `close()`: 当前进程关闭句柄
- `unlink()`: 删除共享内存对象, 通常创建者最后调用

#### 最小闭环代码

```python
from multiprocessing import Process
from multiprocessing.shared_memory import SharedMemory


def child(name: str) -> None:
    shm = SharedMemory(name=name)
    try:
        n = int.from_bytes(shm.buf[:4], "little")
        shm.buf[4:8] = (n + 1).to_bytes(4, "little")
    finally:
        shm.close()


if __name__ == "__main__":
    shm = SharedMemory(create=True, size=8)
    try:
        shm.buf[:4] = (41).to_bytes(4, "little")

        p = Process(target=child, args=(shm.name,))
        p.start()
        p.join()

        print(int.from_bytes(shm.buf[4:8], "little"))  # 42
    finally:
        shm.close()
        shm.unlink()
```

#### 常见坑

- 忘记 `unlink()` 会泄漏系统共享内存资源
- 只共享内存不等于同步安全, 并发读写仍要加锁或设计协议
- 复杂 Python 对象不要硬塞进 shared memory
- 大数组场景通常搭配 NumPy 的 `ndarray(buffer=shm.buf, ...)`

### `contextvars`: 异步上下文隔离

`contextvars` 解决的是: 同一个线程里交错跑很多协程时, 如何保存当前请求的上下文。

`threading.local()` 是按线程隔离。async 程序里一个线程可能同时处理很多请求, 按线程隔离不够。`ContextVar` 是按逻辑上下文隔离。每个 asyncio Task 会带着自己的 context 继续执行。

#### API 先解释

- `ContextVar(name, default=...)`: 定义一个上下文变量, 应放在模块顶层
- `get()`: 读取当前 context 中的值
- `set(value)`: 设置当前 context 的值, 返回 token
- `reset(token)`: 恢复到 set 之前的值
- `copy_context()`: 复制当前 context, 可手动在这个 context 里运行函数
- `Token`: `set()` 返回的恢复凭据, Python 3.14+ 也支持作为 context manager 使用

#### 最小闭环代码

```python
import asyncio
from contextvars import ContextVar, copy_context

request_id: ContextVar[str] = ContextVar("request_id", default="-")


def log(message: str) -> None:
    print(f"[{request_id.get()}] {message}")


async def handle(rid: str) -> None:
    token = request_id.set(rid)
    try:
        log("start")
        await asyncio.sleep(0.01)
        log("end")  # 两个 task 交错执行, 但 request_id 不串
    finally:
        request_id.reset(token)


async def main() -> None:
    await asyncio.gather(handle("req-A"), handle("req-B"))

    request_id.set("manual")
    ctx = copy_context()
    ctx.run(log, "run inside copied context")


asyncio.run(main())
```

#### 什么时候用

适合:

- request id, trace id
- 当前用户, tenant id
- 日志上下文字段
- async Web 框架中间件
- 数据库 session 或 transaction context

不适合:

- 普通业务参数, 能显式传参就显式传参
- 大对象
- 生命周期不清楚的状态
- 用全局上下文偷懒代替清晰的数据流

### `subprocess`: 外部子进程管理

`subprocess` 启动的是外部程序, 不一定是 Python。它处理的是当前 Python 进程和外部进程之间的边界:

- 怎么启动命令
- 怎么传 stdin
- 怎么收 stdout/stderr
- 怎么拿退出码
- 超时怎么杀
- 失败时是否抛异常

它和 `multiprocessing` 的区别是: `multiprocessing` 通常启动 Python 子进程跑 Python 函数, `subprocess` 启动任意可执行程序。

#### API 先解释

- `subprocess.run()`: 推荐的高层接口, 启动, 等待, 返回 `CompletedProcess`
- `capture_output=True`: 捕获 stdout/stderr
- `text=True`: 用字符串而不是 bytes
- `check=True`: 非零退出码抛 `CalledProcessError`
- `timeout=`: 超时抛 `TimeoutExpired`
- `Popen`: 更底层接口, 适合流式交互或长生命周期进程
- `PIPE`: 建立管道
- `communicate()`: 和子进程交换输入输出并等待结束
- `returncode`: 退出码

#### 最小闭环代码

```python
import subprocess
import sys

cmd = [sys.executable, "-c", "print('hello from child')"]
completed = subprocess.run(
    cmd,
    capture_output=True,
    text=True,
    check=True,
    timeout=5,
)
print(completed.returncode, completed.stdout.strip())

p = subprocess.Popen(
    [sys.executable, "-c", "print(input().upper())"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)
out, err = p.communicate("hello\n", timeout=5)
print(p.returncode, out.strip(), err.strip())
```

#### 常见坑

- 参数来自用户时不要拼字符串后 `shell=True`
- 使用 `Popen(stdout=PIPE, stderr=PIPE)` 又不读取, 可能管道满后死锁
- 必须检查退出码, 否则命令失败可能被当成成功
- 每次调用外部命令都有进程启动成本

### `sched`: 进程内小型事件调度器

`sched` 是一个按时间排序的函数调用队列。它不是 cron, 不是后台任务系统, 也不负责持久化。它只是在当前进程里等时间到了就调用某个函数。

#### API 先解释

- `sched.scheduler(timefunc, delayfunc)`: 创建调度器
- `enter(delay, priority, action, argument=(), kwargs={})`: 延迟一段时间执行
- `enterabs(time, priority, action, ...)`: 在绝对时间执行
- `cancel(event)`: 取消还没执行的事件
- `run()`: 开始运行调度器
- `queue`: 查看排队事件

#### 最小闭环代码

```python
import sched
import time

s = sched.scheduler(time.monotonic, time.sleep)


def job(name: str) -> None:
    print(round(time.monotonic(), 2), name)


e1 = s.enter(0.05, priority=2, action=job, argument=("later",))
e2 = s.enter(0.05, priority=1, action=job, argument=("earlier priority",))
e3 = s.enterabs(time.monotonic() + 1, priority=1, action=job, argument=("cancelled",))

print("queued:", len(s.queue))
s.cancel(e3)
s.run()
```

### `_thread`: 底层线程 API

`_thread` 是 `threading` 的底层基础。它只提供原始线程启动和锁。业务代码几乎总是应该用 `threading`, 因为 `threading.Thread` 有对象生命周期, `join()`, 名字, daemon, local, 条件变量等高层能力。

#### API 先解释

- `start_new_thread(function, args)`: 启动一个底层线程
- `allocate_lock()`: 创建底层锁
- `get_ident()`: 当前线程标识
- `get_native_id()`: 当前系统线程 ID
- `interrupt_main()`: 从子线程请求主线程收到 `KeyboardInterrupt`

#### 最小闭环代码

```python
import _thread
import time

lock = _thread.allocate_lock()
done = _thread.allocate_lock()
done.acquire()


def worker() -> None:
    with lock:
        print("low-level thread", _thread.get_ident(), _thread.get_native_id())
    done.release()


_thread.start_new_thread(worker, ())
done.acquire()  # 用锁临时模拟 join, 这就是为什么业务代码该用 threading
time.sleep(0.01)
```

### `selectors`: I/O 多路复用基础

`selectors` 不是帮你创建线程, 而是帮你问操作系统: 这些 fd 里, 哪些现在可以读或写?

事件循环的底层就需要这个能力。没有它, 你可能要给每个 socket 一个线程。用 selector 后, 一个线程可以管理很多 socket, 只有某个 socket 就绪时才处理它。

#### API 先解释

- `DefaultSelector`: 当前平台上合适的 selector 实现
- `register(fileobj, events, data=None)`: 注册要监听的 fd
- `select(timeout=None)`: 等待就绪事件
- `unregister(fileobj)`: 取消监听
- `EVENT_READ`: 可读事件
- `EVENT_WRITE`: 可写事件
- `SelectorKey`: `select()` 返回的 key, 包含 fileobj, fd, events, data

#### 最小闭环代码

```python
import selectors
import socket

sel = selectors.DefaultSelector()
left, right = socket.socketpair()

try:
    left.setblocking(False)
    right.setblocking(False)

    sel.register(left, selectors.EVENT_READ, data="left socket")
    right.send(b"hello")

    for key, mask in sel.select(timeout=1):
        print(key.data, "ready", mask)
        data = key.fileobj.recv(100)
        print(data)

    sel.unregister(left)
finally:
    left.close()
    right.close()
    sel.close()
```

#### 底层意义

- Linux 上可能是 epoll
- macOS/BSD 上可能是 kqueue
- 老平台可能是 poll/select
- Windows 上 selector 对 socket 支持更好, 对普通 pipe 支持有限
- 普通业务代码通常不直接用 selectors, 但理解它能帮你理解 `asyncio`

### `concurrent.interpreters`: 同进程多解释器

Python 3.14 提供了 `concurrent.interpreters` 高层接口。一个 interpreter 可以理解成同一进程里的一个 Python 运行时状态:

- 每个解释器有自己的模块导入状态
- 每个解释器有自己的全局变量和 `sys`, `builtins`, `__main__`
- 每个解释器有自己的 GIL
- 多个解释器之间不能随便共享可变 Python 对象
- 传参数和返回结果通常需要复制或 pickle

它介于线程和进程之间: 比进程轻一些, 比线程隔离强很多, 但不是安全沙箱。

#### API 先解释

- `interpreters.create()`: 创建新解释器
- `interpreters.list_all()`: 列出已有解释器
- `interpreters.get_current()`: 当前解释器
- `interpreters.get_main()`: 主解释器
- `interpreters.create_queue()`: 创建跨解释器队列
- `Interpreter.exec(code)`: 在解释器里执行代码字符串
- `Interpreter.call(fn, *args)`: 在解释器里调用函数并返回结果
- `Interpreter.call_in_thread(fn, *args)`: 新线程中进入该解释器调用函数
- `Interpreter.close()`: 销毁解释器
- `ExecutionFailed`: 另一个解释器中的代码未捕获异常
- `NotShareableError`: 对象不能传给另一个解释器

#### 最小闭环代码

```python
from concurrent import interpreters


def echo(value: str) -> str:
    return value.upper()


interp = interpreters.create()
try:
    print("main:", interpreters.get_main().id)
    print("current:", interpreters.get_current().id)
    print("all:", [i.id for i in interpreters.list_all()])

    interp.exec("x = 41")
    interp.exec("x += 1")
    print(interp.call(echo, "hello"))  # HELLO

    t = interp.call_in_thread(print, "running in another interpreter thread")
    t.join()
finally:
    interp.close()
```

跨解释器队列适合显式传消息:

```python
from concurrent import interpreters

q = interpreters.create_queue()
q.put("message")
print(q.get())
```

#### 什么时候用

适合探索:

- 希望同进程内获得更强隔离
- 任务边界清楚, 参数和结果容易复制或序列化
- 希望尝试 Python 3.14+ 的多核并行方向
- 依赖库确认支持多解释器

不适合:

- 新手默认并发方案
- 依赖大量不确定是否支持多解释器的 C 扩展
- 需要安全隔离, 解释器不是安全沙箱
- 需要共享大量复杂可变对象

### 三种典型架构

#### 同步 I/O 并发: 线程池

```python
from concurrent.futures import ThreadPoolExecutor, as_completed


def call_api(x: int) -> str:
    return f"result-{x}"


with ThreadPoolExecutor(max_workers=32) as ex:
    futures = [ex.submit(call_api, x) for x in range(100)]
    for fut in as_completed(futures):
        print(fut.result())
```

特点:

- 改造成本低
- 适合已有同步库
- 要限制最大 worker 和下游并发
- 不适合纯 Python CPU 密集

#### 大量网络连接: asyncio

```python
import asyncio

sem = asyncio.Semaphore(100)


async def call_downstream(x: int) -> str:
    async with sem:
        await asyncio.sleep(0.01)
        return f"result-{x}"


async def main() -> None:
    async with asyncio.TaskGroup() as tg:
        for x in range(1000):
            tg.create_task(call_downstream(x))


asyncio.run(main())
```

特点:

- 单线程管理大量等待中的 I/O
- 取消和超时语义重要
- 不能混入阻塞调用
- 不能无限制创建任务

#### CPU 密集并行: 进程池

```python
from concurrent.futures import ProcessPoolExecutor


def compute(x: int) -> int:
    return x * x


if __name__ == "__main__":
    with ProcessPoolExecutor() as ex:
        for y in ex.map(compute, range(100), chunksize=16):
            print(y)
```

特点:

- 能利用多个 CPU 核
- 任务函数和参数需要可 pickle
- 进程启动和数据传输有成本
- 适合粗粒度任务

### 选型决策树

先问: 任务是在等 I/O, 还是在烧 CPU?

如果主要等 I/O:

- 依赖库有 async 版本, 并且项目愿意 async 化: 用 `asyncio`
- 依赖库只有同步版本: 用 `ThreadPoolExecutor`
- 需要长期 worker 和任务队列: 用 `threading` + `queue.Queue`
- 要调外部命令: 用 `subprocess`
- 要同时管理很多外部子进程: 用 `asyncio` subprocess API

如果主要烧 CPU:

- 纯 Python 计算: 用 `ProcessPoolExecutor`
- 任务边界清楚且 Python 3.14+ 可用: 可以探索 `InterpreterPoolExecutor`
- 数据巨大, 传输成本高: 考虑 `shared_memory`
- 计算在 NumPy/PyTorch 等 C 扩展里且会释放 GIL: 线程也可能有效

如果主要是隔离:

- 防止崩溃污染主进程: 用进程
- async 请求上下文隔离: 用 `contextvars`
- 线程内上下文隔离: 用 `threading.local()`
- 同进程运行时状态隔离: 探索 `concurrent.interpreters`

如果主要是任务调度:

- async 程序中延时和超时: 用 `asyncio.sleep()`, `asyncio.timeout()`
- 小脚本中定时调用函数: 用 `sched`
- 生产级周期任务: 考虑 cron, systemd timer, APScheduler, Celery beat, Kubernetes CronJob

### 工程实践建议

- 每个跨边界调用都要有超时
- 每个长期任务都要有退出路径
- 队列最好有最大长度, 否则内存会替你承担所有压力
- 线程和协程不是越多越好, 下游服务也有极限
- 用消息传递代替共享可变状态
- 进程池和线程池要在应用启动时创建, 不要每个请求临时创建
- worker 里不要反向等待同一个池的新任务
- async 函数里发现阻塞代码, 要换 async 版本或放进 `to_thread()`
- 进程间传大对象前先想清楚复制成本
- 能用高层抽象就不要直接从 `_thread` 或 `selectors` 开始
