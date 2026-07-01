# Python 数据处理与计算框架

## 参考资料

- [Jupyter 官方文档](https://docs.jupyter.org/)
- [JupyterLab 官方文档](https://jupyterlab.readthedocs.io/)
- [NumPy 官方文档](https://numpy.org/doc/stable/)
- [pandas 官方文档](https://pandas.pydata.org/docs/)
- [Matplotlib 官方文档](https://matplotlib.org/stable/)
- [seaborn 官方文档](https://seaborn.pydata.org/)
- [SciPy 官方文档](https://docs.scipy.org/doc/scipy/)
- [OpenCV Python 官方教程](https://docs.opencv.org/)
- [Pillow 官方文档](https://pillow.readthedocs.io/)
- [scikit-learn 官方文档](https://scikit-learn.org/stable/)
- [PyTorch 官方文档](https://docs.pytorch.org/)
- [Polars 官方文档](https://docs.pola.rs/)
- [Dask 官方文档](https://docs.dask.org/)
- [DuckDB Python 官方文档](https://duckdb.org/docs/clients/python/overview.html)
- [Numba 官方文档](https://numba.pydata.org/)

## 生态地图

数据处理不是一个库解决所有问题, 而是按数据形态和计算方式分层:

- `NumPy`: 多维同类型数组, 是大部分科学计算库的底座
- `pandas`: 带行列标签的表格数据, 适合清洗, 聚合, 连接, 时间序列
- `SciPy`: 基于 NumPy 的科学计算算法库, 如优化, 统计, 稀疏矩阵, 信号处理
- `Matplotlib`: 底层绘图库, 控制力强
- `seaborn`: 基于 Matplotlib 的统计图接口, 更适合 EDA
- `Pillow`: 图片文件读写和基础图像处理, 偏工程处理
- `OpenCV`: 图像和视频处理, 偏计算机视觉算法
- `scikit-learn`: 传统机器学习统一接口, 重点是特征工程, 训练, 评估, Pipeline
- `PyTorch`: 张量计算, 自动求导, 深度学习训练
- `Jupyter`: 交互式实验环境, 不是计算框架本身

常见数据对象:

| 对象 | 主要库 | 适合什么 | 注意点 |
| --- | --- | --- | --- |
| `ndarray` | NumPy | 数值矩阵, 图像数组, 向量化计算 | 同一个数组通常只有一个 `dtype` |
| `Series` / `DataFrame` | pandas | 表格, 标签索引, 缺失值, 聚合连接 | 索引对齐会影响结果 |
| sparse matrix | SciPy | 大量零元素的矩阵 | 不要轻易转成 dense |
| `Image` | Pillow | 图片文件对象 | 读写格式和颜色模式清晰 |
| `Tensor` | PyTorch | GPU 张量, 自动求导 | 设备, dtype, batch 维度要统一 |
| estimator | scikit-learn | 传统机器学习模型 | 避免数据泄漏, 用 Pipeline |

性能模型的优先级:

- NumPy 要懂底层: `dtype`, `shape`, `strides`, view/copy, broadcasting, contiguous memory
- pandas 要懂表模型: `Index` 对齐, 列类型, groupby/merge 的代价, `apply` 的边界
- scikit-learn 要懂流程: 训练集/测试集隔离, Pipeline, 交叉验证
- PyTorch 要懂训练闭环: Tensor, autograd, `Module`, loss, optimizer, `DataLoader`
- SciPy/绘图/图像算法通常先懂接口和边界, 不必一开始深挖每个算法实现

## jupyter

Jupyter 的基本模型:

- Notebook 是文档, 由 Markdown 单元格和代码单元格组成
- Kernel 是真正执行代码的进程
- 单元格运行顺序不一定等于文件从上到下顺序
- 变量存在 Kernel 内存里, 重启 Kernel 后变量会消失

```python
x = 1
x += 1
x
```

上面单元格多运行几次, `x` 会不断变化. 所以 Notebook 最大的问题不是语法, 而是隐藏状态.

常用命令:

```bash
uv run jupyter lab
uv run jupyter notebook
uv run python -m ipykernel install --user --name data-demo
```

建议:

- 做实验时可以乱跑单元格, 但提交前执行一次 `Restart Kernel and Run All`
- 复杂函数写到 `.py` 文件, Notebook 只负责调用和展示
- 数据清洗步骤要保留输入, 输出和关键中间结果
- 需要版本管理时, 大型输出尽量清掉, 避免 `.ipynb` diff 失控

```python
# Notebook 里适合写这种轻量入口
from pathlib import Path

import pandas as pd

DATA_DIR = Path("../data/raw")
df = pd.read_csv(DATA_DIR / "sales.csv")
df.head()
```

## numpy

NumPy 是 Python 数值计算的底座. 它的核心不是“数组语法更短”, 而是:

- 数据放在连续或规则跳跃的内存块里
- 元素类型固定, 不需要每个元素都是 Python 对象
- 大量运算进入 C/Fortran 层循环
- 用 `shape` / `strides` 解释同一块内存

### ndarray 模型

一个 `ndarray` 至少要理解四个东西:

- `dtype`: 每个元素是什么类型, 占多少字节
- `shape`: 每个维度有多长
- `strides`: 沿某个维度走一步, 内存地址跳多少字节
- `data`: 底层数据缓冲区

```python
import numpy as np

a = np.array(
    [[1, 2, 3],
     [4, 5, 6]],
    dtype=np.int32,
)

print(a.dtype)    # int32, 每个元素 4 字节
print(a.shape)    # (2, 3), 2 行 3 列
print(a.ndim)     # 2, 二维
print(a.strides)  # 常见为 (12, 4): 下一行跳 12 字节, 下一列跳 4 字节
```

为什么这重要:

```python
python_list = [1, 2, 3]
numpy_array = np.array([1, 2, 3], dtype=np.int64)
```

Python list 存的是一组对象引用, 每个整数还是 Python 对象. NumPy 数组存的是紧凑的原始数值块. 所以对大量数值做同一种操作时, NumPy 可以更快, 也更省内存.

### 创建数组

```python
import numpy as np

np.array([1, 2, 3])                 # 从 Python 数据创建
np.zeros((2, 3), dtype=np.float32)  # 全 0
np.ones((2, 3))                     # 全 1
np.arange(0, 10, 2)                 # 类似 range, 生成 [0, 2, 4, 6, 8]
np.linspace(0, 1, 5)                # 在 0 到 1 之间均匀取 5 个点
np.eye(3)                           # 3x3 单位矩阵
```

常见属性:

```python
a = np.arange(12).reshape(3, 4)

print(a)
print(a.size)       # 元素总数 12
print(a.itemsize)   # 单个元素字节数
print(a.nbytes)     # 总字节数
print(a.T)          # 转置视图
```

### dtype

`dtype` 会直接影响内存, 精度和速度.

```python
a = np.array([1, 2, 3], dtype=np.int64)
b = np.array([1, 2, 3], dtype=np.int8)

print(a.nbytes)  # 24
print(b.nbytes)  # 3
```

常见选择:

- `float64`: 默认浮点, 精度高, 内存大
- `float32`: 深度学习, 图像, 大矩阵常用
- `int64`: 默认整数, 计数和索引常见
- `bool`: mask
- `object`: 尽量避免, 这会退化成装 Python 对象

```python
bad = np.array([1, "2", object()], dtype=object)
# object 数组通常不能发挥 NumPy 的核心性能优势
```

### 索引, 切片, view/copy

切片通常返回 view, 也就是共享底层数据.

```python
a = np.arange(10)
b = a[2:6]

b[0] = 99
print(a)  # a 也会变, 因为 b 是 view
```

高级索引通常返回 copy.

```python
a = np.arange(10)
b = a[[2, 4, 6]]

b[0] = 99
print(a)  # a 不变, 因为 b 是 copy
```

判断是否共享内存:

```python
a = np.arange(10)
view = a[1:5]
copy = a[[1, 3, 5]]

print(np.shares_memory(a, view))  # True
print(np.shares_memory(a, copy))  # False
```

工程上要注意:

- 对 view 修改会影响原数组
- 对 copy 修改不会影响原数组
- 大数组上的意外 copy 会造成内存暴涨

### 布尔 mask

```python
a = np.array([1, 5, 10, 20])
mask = a >= 10

print(mask)       # [False False  True  True]
print(a[mask])    # [10 20]
print(a[a >= 10]) # 常用简写
```

修改符合条件的元素:

```python
a = np.array([1, 5, 10, 20])
a[a >= 10] = 0
print(a)  # [1 5 0 0]
```

### broadcasting

Broadcasting 是 NumPy 自动扩展形状的规则. 它不是简单复制数据, 而是按规则解释较小数组.

```python
a = np.array(
    [[1, 2, 3],
     [4, 5, 6]],
)

b = np.array([10, 20, 30])

print(a + b)
# [[11 22 33]
#  [14 25 36]]
```

规则从尾部维度对齐:

```text
a.shape = (2, 3)
b.shape =    (3,)
结果     = (2, 3)
```

如果维度不同, 长度必须相等或其中一个是 1.

```python
x = np.ones((3, 1))
y = np.arange(4)

print((x + y).shape)  # (3, 4)
```

典型用途: 对每列标准化.

```python
x = np.array(
    [[1.0, 10.0],
     [2.0, 20.0],
     [3.0, 30.0]]
)

mean = x.mean(axis=0)
std = x.std(axis=0)
z = (x - mean) / std

print(z)
```

### ufunc 与向量化

`ufunc` 是逐元素函数, 如 `np.add`, `np.sqrt`, `np.exp`. 它把循环放到底层执行.

```python
a = np.arange(5)

print(a + 1)        # np.add(a, 1)
print(np.sqrt(a))   # 逐元素开方
print(np.exp(a))    # 逐元素指数
```

不要为了“Python 写法直观”在大数组上手写循环:

```python
a = np.arange(1_000_000, dtype=np.float64)

out = a * 2 + 1  # 底层批量计算
```

但向量化也不是无限好. 这句会产生中间数组:

```python
out = (a * 2 + 1) / 3
```

如果数组极大, 中间数组会占内存. 可以用 `out=` 减少临时分配:

```python
a = np.arange(1_000_000, dtype=np.float64)
out = np.empty_like(a)

np.multiply(a, 2, out=out)
np.add(out, 1, out=out)
np.divide(out, 3, out=out)
```

### axis

`axis` 表示沿哪个维度压缩.

```python
a = np.array(
    [[1, 2, 3],
     [4, 5, 6]],
)

print(a.sum())        # 所有元素求和: 21
print(a.sum(axis=0))  # 压掉行维度, 得到每列和: [5 7 9]
print(a.sum(axis=1))  # 压掉列维度, 得到每行和: [6 15]
```

记法:

```text
axis=0: 沿着行方向往下聚合, 结果按列留下
axis=1: 沿着列方向往右聚合, 结果按行留下
```

保留维度:

```python
a = np.arange(6).reshape(2, 3)
row_sum = a.sum(axis=1, keepdims=True)

print(row_sum.shape)  # (2, 1), 方便后续 broadcasting
```

### 线性代数

```python
import numpy as np

x = np.array([[1, 2], [3, 4]])
y = np.array([[10], [20]])

print(x @ y)                  # 矩阵乘法
print(np.linalg.inv(x))       # 逆矩阵
print(np.linalg.solve(x, y))  # 解线性方程 x * a = y
```

一般不要手写求逆再乘:

```python
# 不推荐
coef = np.linalg.inv(x) @ y

# 推荐
coef = np.linalg.solve(x, y)
```

### 随机数

新代码优先用 `default_rng`.

```python
rng = np.random.default_rng(seed=42)

x = rng.normal(loc=0, scale=1, size=(3, 2))
idx = rng.choice([0, 1, 2, 3], size=2, replace=False)

print(x)
print(idx)
```

### 性能边界

优先检查:

- 是否用了 `object` dtype
- 是否在 Python 循环里逐元素操作
- 是否频繁产生大临时数组
- 是否发生了不必要 copy
- 数组是否连续, 是否需要 `np.ascontiguousarray`
- 是否可以先减少数据量再计算

```python
a = np.arange(12).reshape(3, 4)
b = a.T

print(a.flags["C_CONTIGUOUS"])  # True
print(b.flags["C_CONTIGUOUS"])  # False, 转置通常只是改变 strides

c = np.ascontiguousarray(b)     # 必要时复制成连续内存
```

## pandas

pandas 的核心是带标签的一维/二维数据:

- `Series`: 一列数据 + 一个 `Index`
- `DataFrame`: 多列 `Series` 组成的表
- `Index`: 行标签, 会参与对齐

NumPy 更像矩阵, pandas 更像表.

### Series, DataFrame, Index

```python
import pandas as pd

s = pd.Series([10, 20, 30], index=["a", "b", "c"], name="score")
print(s["a"])

df = pd.DataFrame(
    {
        "name": ["alice", "bob", "carol"],
        "age": [18, 20, 19],
        "score": [90.0, 85.5, 88.0],
    }
)

print(df.head())
print(df.dtypes)
```

索引对齐是 pandas 很重要的模型:

```python
a = pd.Series([1, 2], index=["x", "y"])
b = pd.Series([10, 20], index=["y", "z"])

print(a + b)
# x     NaN
# y    12.0
# z     NaN
```

不是按位置相加, 而是按标签对齐.

### 读写数据

```python
from pathlib import Path

import pandas as pd

path = Path("data/sales.csv")

df = pd.read_csv(path)
df.to_csv("data/sales_clean.csv", index=False)
df.to_parquet("data/sales_clean.parquet", index=False)
```

常见格式:

- CSV: 通用, 慢, 类型信息弱
- Excel: 适合业务交互, 不适合大规模流水线
- Parquet: 列式存储, 保留类型更好, 适合分析数据
- JSON: 接口常见, 表格分析前常要规范化

```python
df = pd.read_csv(
    "data/sales.csv",
    usecols=["date", "region", "amount"],
    parse_dates=["date"],
)
```

### 观察数据

```python
df.head()
df.tail()
df.info()
df.describe()
df.shape
df.columns
df.isna().sum()
```

### 选择数据

```python
df["name"]              # 一列, Series
df[["name", "score"]]   # 多列, DataFrame

df.loc[0, "name"]       # 按标签
df.iloc[0, 0]           # 按位置
```

布尔筛选:

```python
high_score = df[df["score"] >= 88]
adult = df[(df["age"] >= 18) & (df["score"] >= 85)]
```

注意 `&` 和 `|` 两边要加括号.

### 新增和修改列

```python
df = df.assign(
    passed=df["score"] >= 60,
    score_level=lambda x: pd.cut(
        x["score"],
        bins=[0, 60, 80, 100],
        labels=["bad", "ok", "good"],
    ),
)
```

尽量优先用列运算, 少用逐行 `apply`.

```python
# 推荐
df["amount_with_tax"] = df["amount"] * 1.13

# 数据很大时谨慎
df["amount_with_tax"] = df.apply(lambda row: row["amount"] * 1.13, axis=1)
```

### 缺失值

```python
df.isna()
df.dropna(subset=["name"])
df.fillna({"score": 0})
```

pandas 有多种缺失值表示:

- `np.nan`: 传统浮点缺失值
- `None`: Python 空值
- `pd.NA`: pandas nullable dtype 的缺失值

如果整数列有缺失值, 可以使用 nullable integer:

```python
s = pd.Series([1, None, 3], dtype="Int64")
print(s)
```

### dtype

```python
df = pd.DataFrame(
    {
        "id": pd.Series([1, 2, 3], dtype="Int64"),
        "region": pd.Series(["east", "west", "east"], dtype="category"),
        "amount": pd.Series([10.5, 20.0, 7.5], dtype="float64"),
    }
)

print(df.dtypes)
```

常见建议:

- 类别少的字符串列可以转 `category`
- 日期列用 `datetime64`
- 布尔缺失可以用 nullable boolean
- 避免无意义的 `object` 列

### groupby

`groupby` 是 split-apply-combine:

- split: 按键拆分数据
- apply: 对每组计算
- combine: 合并结果

```python
sales = pd.DataFrame(
    {
        "region": ["east", "east", "west", "west"],
        "product": ["A", "B", "A", "B"],
        "amount": [100, 80, 120, 90],
    }
)

summary = (
    sales
    .groupby("region", as_index=False)
    .agg(
        total_amount=("amount", "sum"),
        avg_amount=("amount", "mean"),
        orders=("amount", "size"),
    )
)

print(summary)
```

多字段分组:

```python
summary = (
    sales
    .groupby(["region", "product"], as_index=False)
    .agg(total=("amount", "sum"))
)
```

组内变换:

```python
sales["region_total"] = sales.groupby("region")["amount"].transform("sum")
sales["ratio"] = sales["amount"] / sales["region_total"]
```

`agg` 会把每组压缩成更少的行, `transform` 会保持原行数.

### merge, join, concat

```python
orders = pd.DataFrame(
    {"order_id": [1, 2, 3], "user_id": [10, 20, 10], "amount": [99, 30, 50]}
)

users = pd.DataFrame(
    {"user_id": [10, 20], "name": ["alice", "bob"]}
)

df = orders.merge(users, on="user_id", how="left")
print(df)
```

常见连接方式:

- `left`: 保留左表全部行
- `inner`: 只保留两边匹配的行
- `outer`: 两边都保留
- `right`: 保留右表全部行

建议用 `validate` 检查关系:

```python
orders.merge(users, on="user_id", how="left", validate="many_to_one")
```

纵向拼接:

```python
all_sales = pd.concat([sales_2024, sales_2025], ignore_index=True)
```

### 时间序列

```python
df = pd.DataFrame(
    {
        "date": pd.to_datetime(["2026-01-01", "2026-01-02", "2026-01-10"]),
        "amount": [10, 20, 30],
    }
)

df = df.set_index("date")
weekly = df.resample("W").sum()
```

常用:

- `pd.to_datetime(...)`: 转日期
- `.dt.year`, `.dt.month`, `.dt.day`: 日期字段
- `set_index("date")`: 设置时间索引
- `resample("D" / "W" / "M")`: 按时间重采样

### 透视表

```python
pivot = sales.pivot_table(
    index="region",
    columns="product",
    values="amount",
    aggfunc="sum",
    fill_value=0,
)

print(pivot)
```

长宽表转换:

```python
wide = pd.DataFrame(
    {
        "name": ["alice", "bob"],
        "math": [90, 80],
        "english": [85, 88],
    }
)

long = wide.melt(
    id_vars="name",
    var_name="subject",
    value_name="score",
)
```

### pandas 性能边界

优先规则:

- 列运算优于 `apply(axis=1)`
- `groupby.agg` / `transform` 优于手写循环
- 减少不必要的 `object` dtype
- 读文件时用 `usecols`, `dtype`, `parse_dates`
- 大表优先 Parquet
- 先过滤再 join/groupby
- 单机内存不够时考虑 Polars, DuckDB, Dask, Spark

```python
# 分块读取大 CSV
chunks = pd.read_csv("big.csv", chunksize=100_000)

total = 0
for chunk in chunks:
    total += chunk["amount"].sum()
```

## matplotlib

Matplotlib 的核心模型:

- `Figure`: 整张图
- `Axes`: 一块具体绘图区域, 通常就是一个子图
- `pyplot`: 便捷状态机接口

新代码建议优先用面向对象写法:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(x, y, label="sin(x)")
ax.set_title("Sine Wave")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.legend()
fig.tight_layout()
plt.show()
```

多个子图:

```python
fig, axes = plt.subplots(1, 2, figsize=(8, 3))

axes[0].plot(x, np.sin(x))
axes[0].set_title("sin")

axes[1].plot(x, np.cos(x))
axes[1].set_title("cos")

fig.tight_layout()
```

保存图片:

```python
fig.savefig("outputs/figures/sine.png", dpi=200, bbox_inches="tight")
```

常见图:

```python
fig, ax = plt.subplots()

ax.scatter([1, 2, 3], [2, 4, 3])
ax.bar(["A", "B", "C"], [10, 20, 15])
ax.hist(np.random.default_rng(42).normal(size=1000), bins=30)
```

选择建议:

- 要控制每个细节: Matplotlib
- 要快速看统计关系: seaborn
- 要交互式网页图: Plotly, Bokeh, Altair

## seaborn

seaborn 是统计可视化接口, 建在 Matplotlib 之上. 它更偏 EDA:

- 用 DataFrame 长表直接画图
- 自动处理颜色, 分组, 置信区间等统计展示
- 图好看, 但底层仍可以拿到 Matplotlib 对象继续调

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame(
    {
        "day": ["Mon", "Mon", "Tue", "Tue", "Wed", "Wed"],
        "group": ["A", "B", "A", "B", "A", "B"],
        "value": [10, 12, 15, 13, 18, 17],
    }
)

ax = sns.lineplot(data=df, x="day", y="value", hue="group", marker="o")
ax.set_title("Daily Value")
plt.show()
```

常见图:

```python
sns.scatterplot(data=df, x="x", y="y", hue="group")
sns.lineplot(data=df, x="date", y="value", hue="group")
sns.histplot(data=df, x="value", hue="group", kde=True)
sns.boxplot(data=df, x="group", y="value")
sns.heatmap(corr, annot=True, cmap="coolwarm")
```

figure-level 接口会自己创建整张图:

```python
sns.relplot(data=df, x="day", y="value", hue="group", kind="line")
sns.catplot(data=df, x="group", y="value", kind="box")
sns.displot(data=df, x="value", kde=True)
```

使用建议:

- seaborn 假设数据整理成长表更舒服
- 分组维度多时用 `hue`, `row`, `col`
- 最终论文级细节可以回到 Matplotlib 调整

## scipy

SciPy 是科学计算算法库. 它通常接收 NumPy 数组, 返回 NumPy 数组或专用结果对象.

常用模块:

| 模块 | 用途 |
| --- | --- |
| `scipy.linalg` | 线性代数, 比 `numpy.linalg` 更完整 |
| `scipy.optimize` | 优化, 方程求解, 最小二乘 |
| `scipy.stats` | 概率分布, 统计检验 |
| `scipy.sparse` | 稀疏矩阵 |
| `scipy.sparse.linalg` | 稀疏线性代数 |
| `scipy.signal` | 信号处理 |
| `scipy.fft` | 快速傅里叶变换 |
| `scipy.integrate` | 数值积分, ODE |
| `scipy.interpolate` | 插值 |

这里不需要一开始掌握每个算法怎么实现, 重点是知道:

- 输入数据形状是什么
- 返回结果对象里有什么
- 算法对数据规模和条件有什么限制
- dense 和 sparse 不能混着乱用

### optimize

```python
import numpy as np
from scipy.optimize import minimize


def loss(x):
    # 最小值在 x=[1, -2]
    return (x[0] - 1) ** 2 + (x[1] + 2) ** 2


result = minimize(loss, x0=np.array([0.0, 0.0]))

print(result.x)       # 最优参数
print(result.fun)     # 最小损失
print(result.success) # 是否收敛
```

### stats

```python
from scipy import stats

x = [1.2, 1.5, 1.7, 1.4]
y = [2.0, 2.2, 1.9, 2.4]

result = stats.ttest_ind(x, y)

print(result.statistic)
print(result.pvalue)
```

统计检验不要只背 API. 至少要确认:

- 样本是否独立
- 分布假设是否合理
- p-value 回答的是什么问题
- 多重检验是否需要修正

### sparse

稀疏矩阵适合大部分元素为 0 的场景, 如文本特征, 图结构, 推荐系统.

```python
import numpy as np
from scipy import sparse

row = np.array([0, 0, 1, 2])
col = np.array([0, 2, 2, 1])
data = np.array([1.0, 2.0, 3.0, 4.0])

mat = sparse.coo_matrix((data, (row, col)), shape=(3, 3)).tocsr()

print(mat)
print(mat.toarray())  # 小矩阵调试可以转 dense, 大矩阵不要这么做
```

## opencv

OpenCV 主要处理图像和视频, Python 里通常导入为 `cv2`.

基本模型:

- 图片读进来是 NumPy 数组
- 灰度图形状通常是 `(height, width)`
- 彩色图形状通常是 `(height, width, channels)`
- OpenCV 默认颜色顺序是 BGR, 不是 RGB

```python
import cv2

img = cv2.imread("data/image.jpg")

print(type(img))   # numpy.ndarray
print(img.shape)   # (height, width, 3)
print(img.dtype)   # 常见 uint8
```

颜色转换:

```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
```

如果用 Matplotlib 显示 OpenCV 读入的彩色图, 要先 BGR 转 RGB.

```python
import matplotlib.pyplot as plt

plt.imshow(rgb)
plt.axis("off")
```

常见操作:

```python
resized = cv2.resize(img, (224, 224))
blurred = cv2.GaussianBlur(img, (5, 5), 0)
edges = cv2.Canny(gray, threshold1=50, threshold2=150)

_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
```

保存:

```python
cv2.imwrite("outputs/edges.png", edges)
```

什么时候用 OpenCV:

- 传统图像处理, 视频帧处理, 轮廓, 阈值, 几何变换
- 需要和 NumPy 高效配合
- 需要摄像头或视频流

什么时候用 Pillow:

- 简单打开, 裁剪, 缩放, 转格式
- Web 后端处理上传图片
- 处理 EXIF, mode, 文件格式细节

## pillow

Pillow 是 PIL 的维护版本, 更偏图片文件和基础变换.

```python
from PIL import Image

img = Image.open("data/image.jpg")

print(img.size)  # (width, height)
print(img.mode)  # RGB, RGBA, L 等
```

基础操作:

```python
img = Image.open("data/image.jpg").convert("RGB")

small = img.resize((224, 224))
crop = img.crop((0, 0, 200, 200))
gray = img.convert("L")

small.save("outputs/image_224.jpg", quality=90)
```

保持比例缩略:

```python
img = Image.open("data/image.jpg").convert("RGB")
img.thumbnail((512, 512))
img.save("outputs/thumb.jpg")
```

和 NumPy 转换:

```python
import numpy as np
from PIL import Image

img = Image.open("data/image.jpg").convert("RGB")
arr = np.asarray(img)

print(arr.shape)  # (height, width, 3), RGB

img2 = Image.fromarray(arr)
```

注意:

- Pillow 的尺寸是 `(width, height)`
- NumPy/OpenCV 图像形状是 `(height, width, channel)`
- Pillow 通常是 RGB, OpenCV 通常是 BGR

## scikit-learn

scikit-learn 的核心不是某个算法, 而是一套统一接口.

基本对象:

- estimator: 有 `fit(...)`, 如 `LogisticRegression`
- predictor: 有 `predict(...)`
- transformer: 有 `fit(...)` 和 `transform(...)`, 如 `StandardScaler`
- pipeline: 把预处理和模型串起来

### 最小训练流程

```python
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

X, y = load_iris(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

pred = model.predict(X_test)
print(accuracy_score(y_test, pred))
```

### fit, transform, predict

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

scaler.fit(X_train)              # 只在训练集上学习均值和方差
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

不要对全量数据先 `fit_transform`, 再切训练/测试. 这会让测试集信息泄漏到训练过程.

### Pipeline

Pipeline 把“预处理”和“模型”绑定成一个整体, 防止训练和预测不一致.

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipe = Pipeline(
    steps=[
        ("scale", StandardScaler()),
        ("model", LogisticRegression(max_iter=1000)),
    ]
)

pipe.fit(X_train, y_train)
pred = pipe.predict(X_test)
```

对表格数据, 常见做法是 `ColumnTransformer`.

```python
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

df = pd.DataFrame(
    {
        "age": [18, 20, None, 30],
        "city": ["bj", "sh", "bj", "gz"],
        "label": [0, 1, 0, 1],
    }
)

X = df[["age", "city"]]
y = df["label"]

preprocess = ColumnTransformer(
    transformers=[
        (
            "num",
            Pipeline(
                steps=[
                    ("impute", SimpleImputer(strategy="median")),
                    ("scale", StandardScaler()),
                ]
            ),
            ["age"],
        ),
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            ["city"],
        ),
    ]
)

model = Pipeline(
    steps=[
        ("preprocess", preprocess),
        ("clf", RandomForestClassifier(random_state=42)),
    ]
)

model.fit(X, y)
```

### 交叉验证和调参

```python
from sklearn.model_selection import cross_val_score, GridSearchCV

scores = cross_val_score(pipe, X, y, cv=5, scoring="accuracy")
print(scores.mean())

params = {
    "model__C": [0.1, 1.0, 10.0],
}

search = GridSearchCV(pipe, params, cv=5, scoring="accuracy")
search.fit(X, y)

print(search.best_params_)
print(search.best_score_)
```

`model__C` 里的双下划线表示 Pipeline 中 `model` 这个步骤的参数 `C`.

### 评估

```python
from sklearn.metrics import classification_report, confusion_matrix

pred = pipe.predict(X_test)

print(confusion_matrix(y_test, pred))
print(classification_report(y_test, pred))
```

回归常用:

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
```

分类常用:

```python
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
```

### 常见坑

- 数据泄漏: 在切分前对全量数据做标准化, 缺失值填充, 特征选择
- 指标选错: 类别极不平衡时只看 accuracy 可能误导
- 随机性不可复现: 不设 `random_state`
- 训练/线上预处理不一致: 没有用 Pipeline
- 把深度学习问题硬塞进 scikit-learn: scikit-learn 不是 mini-batch GPU 训练框架

## torch

PyTorch 的核心模型:

- `Tensor`: 类似 NumPy 数组, 但可以放到 GPU
- autograd: 根据 Tensor 运算自动构建计算图, 反向传播求梯度
- `nn.Module`: 模型层和参数的容器
- loss: 衡量预测和目标差距
- optimizer: 根据梯度更新参数
- `Dataset` / `DataLoader`: 数据集和批量加载

### Tensor

```python
import torch

x = torch.tensor([[1.0, 2.0], [3.0, 4.0]])

print(x.shape)
print(x.dtype)
print(x.device)
```

设备:

```python
device = "cuda" if torch.cuda.is_available() else "cpu"

x = x.to(device)
```

NumPy 转 Tensor:

```python
import numpy as np
import torch

arr = np.array([1, 2, 3], dtype=np.float32)
t = torch.from_numpy(arr)

print(t)
```

### autograd

```python
import torch

x = torch.tensor([2.0], requires_grad=True)
y = x ** 2 + 3 * x

y.backward()

print(x.grad)  # dy/dx = 2x + 3, x=2 时为 7
```

训练时一般流程:

```python
optimizer.zero_grad()  # 清空上一轮梯度
loss.backward()        # 反向传播, 计算梯度
optimizer.step()       # 用梯度更新参数
```

如果忘了 `zero_grad()`, 梯度会累积.

### nn.Module

```python
import torch
from torch import nn


class LinearModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Linear(2, 1)

    def forward(self, x):
        return self.net(x)


model = LinearModel()
x = torch.randn(4, 2)
y = model(x)

print(y.shape)  # (4, 1)
```

### Dataset 和 DataLoader

```python
import torch
from torch.utils.data import DataLoader, TensorDataset

X = torch.randn(100, 2)
y = (X[:, 0] + X[:, 1] > 0).float().unsqueeze(1)

dataset = TensorDataset(X, y)
loader = DataLoader(dataset, batch_size=16, shuffle=True)

for batch_x, batch_y in loader:
    print(batch_x.shape, batch_y.shape)
    break
```

自定义数据集:

```python
from torch.utils.data import Dataset


class MyDataset(Dataset):
    def __init__(self, xs, ys):
        self.xs = xs
        self.ys = ys

    def __len__(self):
        return len(self.xs)

    def __getitem__(self, idx):
        return self.xs[idx], self.ys[idx]
```

### 最小训练闭环

```python
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

device = "cuda" if torch.cuda.is_available() else "cpu"

X = torch.randn(1000, 2)
y = (X[:, 0] * 2 + X[:, 1] * -1 > 0).float().unsqueeze(1)

loader = DataLoader(TensorDataset(X, y), batch_size=32, shuffle=True)

model = nn.Sequential(
    nn.Linear(2, 8),
    nn.ReLU(),
    nn.Linear(8, 1),
).to(device)

loss_fn = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

for epoch in range(5):
    model.train()
    total_loss = 0.0

    for batch_x, batch_y in loader:
        batch_x = batch_x.to(device)
        batch_y = batch_y.to(device)

        logits = model(batch_x)
        loss = loss_fn(logits, batch_y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    print(epoch, total_loss / len(loader))
```

推理:

```python
model.eval()

with torch.no_grad():
    logits = model(X[:5].to(device))
    prob = torch.sigmoid(logits)
    pred = prob >= 0.5

print(pred)
```

### PyTorch 性能边界

优先检查:

- 数据和模型是否在同一个 device
- dtype 是否匹配, 常见训练用 `float32`
- batch size 是否过小导致 GPU 吃不满
- `DataLoader` 是否成为瓶颈
- 推理时是否用了 `model.eval()` 和 `torch.no_grad()`
- 是否频繁 CPU/GPU 来回拷贝

```python
# 不要在训练循环里频繁 .cpu().numpy(), 这会打断 GPU 流水线
```

## 常见扩展

### Polars

Polars 是高性能 DataFrame 库, 核心用 Rust 实现, 支持 eager 和 lazy.

```python
import polars as pl

df = pl.DataFrame(
    {
        "region": ["east", "east", "west"],
        "amount": [10, 20, 30],
    }
)

out = (
    df.lazy()
    .filter(pl.col("amount") >= 20)
    .group_by("region")
    .agg(pl.col("amount").sum().alias("total"))
    .collect()
)

print(out)
```

适合:

- 单机大表
- 想要更快的 DataFrame 计算
- 可以接受和 pandas 不完全一样的 API

### DuckDB

DuckDB 是嵌入式分析数据库, 适合在本地直接用 SQL 查 CSV, Parquet, pandas, Arrow, Polars.

```python
import duckdb
import pandas as pd

df = pd.DataFrame({"region": ["east", "west"], "amount": [10, 20]})

result = duckdb.sql(
    """
    select region, sum(amount) as total
    from df
    group by region
    """
).df()

print(result)
```

适合:

- 很多数据在 Parquet/CSV 里
- 你更习惯 SQL
- 单机分析, 不想搭数据库服务

### Dask

Dask 把 NumPy/pandas 风格计算拆成任务图, 可以本机多进程或分布式执行.

```python
import dask.dataframe as dd

df = dd.read_csv("data/*.csv")
result = df.groupby("region")["amount"].sum().compute()
```

适合:

- 数据比内存大, 但仍希望用类似 pandas 的接口
- 需要并行处理多个文件
- 已经理解 pandas, 但需要扩展到更大数据

注意:

- Dask 是懒执行, 最后 `.compute()` 才真正计算
- 不是所有 pandas 操作都能高效迁移
- 任务切得太碎会有调度开销

### Numba

Numba 是 JIT 编译器, 适合把部分 NumPy + Python 循环编译成机器码.

```python
import numpy as np
from numba import njit


@njit
def sum_square(x):
    total = 0.0
    for i in range(x.shape[0]):
        total += x[i] * x[i]
    return total


x = np.arange(1_000_000, dtype=np.float64)
print(sum_square(x))
```

适合:

- NumPy 很难向量化的循环
- 数值计算热点明确
- 数据结构比较简单

不适合:

- 大量 Python 对象, 字符串, 复杂 pandas 操作
- 业务逻辑频繁变化, 编译收益不明显

## 选型

按问题选工具:

| 问题 | 首选 |
| --- | --- |
| 数值数组, 矩阵, 图像像素 | NumPy |
| 表格清洗, 聚合, join | pandas |
| 表格很大, 单机性能不够 | Polars / DuckDB |
| 数据超过内存, 多文件并行 | Dask |
| 数值优化, 统计检验, 稀疏矩阵 | SciPy |
| 传统机器学习 | scikit-learn |
| 深度学习, GPU, 自动求导 | PyTorch |
| 基础画图和精细控制 | Matplotlib |
| 快速统计图 | seaborn |
| 图片文件处理 | Pillow |
| 图像/视频算法 | OpenCV |

按性能问题排查:

```text
慢在 Python 循环逐元素计算 -> NumPy 向量化或 Numba
慢在 pandas apply(axis=1) -> 列运算 / groupby / merge
慢在 CSV 读取 -> usecols / dtype / Parquet / DuckDB
慢在单机内存 -> Polars / Dask / Spark
慢在模型训练 -> batch, device, DataLoader, mixed precision
慢在图像处理 -> OpenCV / 批处理 / 减少格式转换
```

## 工程检查清单

- 数据是否有明确 schema: 列名, dtype, 缺失值规则
- 原始数据是否只读保存
- 清洗逻辑是否可以从头重跑
- 随机过程是否固定 seed
- 训练/测试是否严格隔离
- 预处理是否放进 Pipeline
- 大文件是否避免提交到 Git
- 图表是否保存到固定输出目录
- 模型和数据版本是否能对应
- 性能瓶颈是否用采样和 profiling 证明过
