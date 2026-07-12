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

- 并发: 生命周期重叠
- 并行: 同时执行
- 任务: 要做的一段工作
- 执行单元: 维护任务状态和调度的东西, 比如线程, 协程, 进程
- 调度器: 决定现在推进谁, 比如协程的 event loop
- 等待点: 当前任务主动或被动停下来的地方, 协程 `await`, 线程不可控

### GIL

- GIL 是 CPython 的全局解释器锁
- GIL 不阻止线程并发等待 I/O, 因为阻塞 I/O 和很多 C 扩展会释放 GIL
- 多进程可以绕过 GIL, 因为每个进程有自己的解释器和自己的 GIL
- Python 3.14 的 `InterpreterPoolExecutor` 使用多个子解释器, 每个解释器有自己的 GIL
- CPython 3.13 开始提供 free-threaded 构建作为关闭 GIL 的实验方向
    - 本质是为了保护 Python 中的对象 (引用计数 / 内部结构)
    - 解决办法是对象乐观锁 + 偏向引用计数
    - 部分 C 拓展需要适配一下

### `asyncio`

```py
async def coro():
    await asyncio.sleep(1)
    return

async def fun1():
    result1 = await coro()
    result2 = await coro() # 顺序等待, 不是并发, 2s

async def fun2():
    task1 = asyncio.create_task(coro())
    task2 = asyncio.create_task(coro()) # 创建两个 task, 塞进 event loop
    result1 = await task1
    result2 = await task2 # 并发等待, 大约 1s

```

- `Future` 是代替回调的机制, 创建一个 `Future` 对象, 让它在某个时刻被设置结果, 其他协程可以 `await` 它
    - `Task` 是 `Future` 的子类

#### `asyncio` API

- `Task.cancel()`: 取消任务, 让它在下一个等待点抛 `CancelledError`
    - `finally` 块仍然会执行, 可以在里面做清理
    - 如果捕获 `CancelledError`, 务必 `raise`
- 事件循环
    - `asyncio.run(coro)`: 创建 event loop, 跑入口协程, 结束后关闭 loop
    - `asyncio.create_task(coro)`: 把协程包装成 Task, 让它开始被 event loop 调度
- 并发控制
    - `asyncio.TaskGroup`: 结构化并发, 一组任务作为一个生命周期单元
        - `3.11` 引入, 失败请求取消全部任务, 并把异常聚合成 `ExceptionGroup`
    - `asyncio.gather()`: 并发等待多个子任务, 通常按输入顺序返回结果
        - 一个失败, 其它不会自动取消
        - `return_exceptions=True` 能把异常当结果返回
    - `asyncio.wait()`: 等一批任务达到某个条件, 返回 done 和 pending 两组
        - 设定条件是超时, 不会自动取消任务
        - `asyncio.wait_for()` 可以指定超时取消
    - `asyncio.as_completed()`: 谁先完成就先处理谁
    - `asyncio.sleep()`: 非阻塞睡眠, 让 event loop 去跑别的任务
- 工具
    - `asyncio.Queue`: 协程之间传消息, `put()` 放入, `get()` 取出, `task_done()` 标记完成, `join()` 等所有任务完成
- 卸载
    - `asyncio.to_thread()`: 在默认线程池中跑同步阻塞函数, 避免卡住 event loop
        - `loop.run_in_executor()`: 指定线程池或进程池执行同步函数
    - `asyncio.create_subprocess_exec()`: 异步启动和等待子进程

### `threading`

```py
import threading


def worker(name: str) -> None:
    print("开始:", name)


thread = threading.Thread(
    target=worker,
    args=("worker-1",),
)

thread.start()
thread.join() # 等待线程结束
```

#### `threading` API

- `Lock`: 互斥锁, 同一时间只允许一个线程进入临界区
- `RLock`: 可重入锁, 同一线程可以重复获得同一把锁
- `Condition`: 条件变量
- `Semaphore`: 计数信号量
- `BoundedSemaphore`: 带上界检查的信号量, 多释放会报错
- `Event`: 一个布尔信号, `set()` 后唤醒等待者
- `Barrier`: 等固定数量线程都到达某点后一起继续
- `Timer`: 延迟一段时间后在线程里执行函数
- `local`: 线程本地存储, 每个线程看到自己的值
- `current_thread()`: 当前线程对象
- `get_ident()`: 当前线程的 Python 线程标识
- `get_native_id()`: 当前线程的系统线程 ID

#### `queue`

- 就是正常的线程安全队列

### `concurrent.futures`

- Executor 管一组 worker
- `submit(fn, *args)` 把函数交给 worker 执行
- 立刻返回 `Future`
- 主线程可以 `result()` 等结果, `cancel()` 取消未开始的任务, `as_completed()` 谁先结束就处理谁

#### API 先解释

- `Executor.submit()`: 提交一个函数调用, 返回 Future
- `Executor.shutdown()`: 关闭池, `with` 会自动调用
- `Future.result()`: 等任务完成并返回结果, 任务抛异常则这里重新抛
- `Future.exception()`: 取任务异常
- `Future.cancel()`: 尝试取消还没开始的任务
- `Future.done()`: 是否结束
- `Future.running()`: 是否正在运行
- `Future.add_done_callback()`: 完成时回调
- `ThreadPoolExecutor`: 线程池
- `ProcessPoolExecutor`: 进程池
- `InterpreterPoolExecutor`: Python 3.14+ 解释器池, 隔离性强于线程, 通信成本类似序列化
    - 可多核并行

### `multiprocessing`

- 独立的进程, 每个进程有自己的 Python 解释器和 GIL, 可以多核并行
- 参数和结果通常通过 pickle 序列化

#### `multiprocessing.shared_memory`: 共享大块原始内存

### `contextvars` 异步上下文隔离

- `threading.local()` 是按线程隔离
- `ContextVar` 是按逻辑上下文隔离

#### `contextvars` API

- `ContextVar(name, default=...)`: 定义一个上下文变量, 应放在模块顶层
- `get()`: 读取当前 context 中的值
- `set(value)`: 设置当前 context 的值, 返回 token
- `reset(token)`: 恢复到 set 之前的值
- `copy_context()`: 复制当前 context, 可手动在这个 context 里运行函数
- `Token`: `set()` 返回的恢复凭据, Python 3.14+ 也支持作为 context manager 使用

### `subprocess` 外部子进程

### `concurrent.interpreters` 同进程多解释器

- 每个解释器有自己的模块导入状态
- 每个解释器有自己的全局变量和 `sys`, `builtins`, `__main__`
- 每个解释器有自己的 GIL
- 多个解释器之间不能随便共享可变 Python 对象
- 传参数和返回结果通常需要复制或 pickle
