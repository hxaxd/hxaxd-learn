# Python 数据处理与计算框架

## 参考资料

- Codex

## Jupyter

- Notebook 由 Markdown 单元格和代码单元格组成
- Kernel 是真正执行代码的进程
- 单元格运行顺序不一定等于文件从上到下顺序
- 变量存在 Kernel 内存里, 重启 Kernel 后变量会消失

```python
# 隐藏状态
x += 1
x # 每运行一次, x 都会加 1
```

## NumPy

- 数据放在连续或规则跳跃的内存块里
- 元素类型固定, 不需要每个元素都是 Python 对象
- 大量运算进入 C 层循环
- 用 `shape` / `strides` 解释同一块内存

### ndarray 模型

- `dtype`: 每个元素是什么类型, 占多少字节
    - `np.float64`: 默认浮点
    - `np.float32`
    - `np.int64`: 默认整数
    - `np.bool_`: 1 字节
    - `np.object_`: 8 字节, 存的是 Python 对象引用
    - `np.str_`: 8 字节, 存的是 Python 字符串引用
- `shape`: 每个维度有多长
    - `arr.reshape((2, 3))` : 2 行 3 列
- `strides`: 沿某个维度走一步, 内存地址跳多少字节
- `data`: 底层数据缓冲区

### 创建数组

```python
import numpy as np

np.array([1, 2, 3]) # 从 Python 数据创建
np.zeros((2, 3), dtype=np.float32) # 全 0
np.ones((2, 3)) # 全 1
np.arange(0, 10, 2) # 类似 range, 生成 [0, 2, 4, 6, 8]
np.linspace(0, 1, 5) # 在 0 到 1 之间均匀取 5 个点
np.eye(3) # 3x3 单位矩阵


print(a.size) # 元素总数 12
print(a.itemsize) # 单个元素字节数
print(a.nbytes) # 总字节数
print(a.T) # 转置视图
```

### 切片

```python
a = np.arange(10)
b1 = a[2:6]
b2 = a[[2, 4, 6]]

b1[0] = 99
print(a) # a 也会变, 因为 b 是视图


b2[0] = 99
print(a) # a 不变, 因为 b 是副本

b3 = a.T # 转置视图, 不复制数据, 不连续
# 如果被转置的数组太复杂, 可能自动复制数据, 变成连续数组
np.ascontiguousarray(b) # 转为连续
```

### 掩码

```python
a = np.array([1, 5, 10, 20])
mask = a >= 10

print(mask) # [False False True True]
print(a[mask]) # [10 20]

a[a >= 10] = 0
print(a) # [1 5 0 0]
```

### 广播

- Broadcasting 是自动扩展形状的规则

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

print((x + y).shape) # (3, 4)
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

- 逐元素函数, 如 `np.add` (逐元素相加) , `np.sqrt` (逐元素开方) , `np.exp` (逐元素指数) . 它把循环放到底层执行.

```python
a = np.arange(5)

print(a + 1) # np.add(a, 1)
print(np.sqrt(a)) # 逐元素开方
print(np.exp(a)) # 逐元素指数
```

不要为了“Python 写法直观”在大数组上手写循环:

```python
a = np.arange(1_000_000, dtype=np.float64)

out = a * 2 + 1 # 底层批量计算
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

### axis (轴)

`axis` (轴) 表示沿哪个维度压缩.

```python
a = np.array(
    [[1, 2, 3],
     [4, 5, 6]],
)

print(a.sum()) # 所有元素求和: 21
print(a.sum(axis=0)) # 压掉行维度, 得到每列和: [5 7 9]
print(a.sum(axis=1)) # 压掉列维度, 得到每行和: [6 15]
```

记法:

```text
axis=0 (第 0 轴) : 沿着行方向往下聚合, 结果按列留下
axis=1 (第 1 轴) : 沿着列方向往右聚合, 结果按行留下
```

保留维度:

```python
a = np.arange(6).reshape(2, 3)
row_sum = a.sum(axis=1, keepdims=True)

print(row_sum.shape) # (2, 1), 方便后续 broadcasting (广播) 
```

### 线性代数

```python
import numpy as np

x = np.array([[1, 2], [3, 4]])
y = np.array([[10], [20]])

print(x @ y) # 矩阵乘法
print(np.linalg.inv(x)) # 逆矩阵
print(np.linalg.solve(x, y)) # 解线性方程 x * a = y
```

一般不要手写求逆再乘:

```python
# 不推荐
coef = np.linalg.inv(x) @ y

# 推荐
coef = np.linalg.solve(x, y)
```

### 随机数

```python
rng = np.random.default_rng(seed=42)

x = rng.normal(loc=0, scale=1, size=(3, 2)) # 在正态分布上采样
idx = rng.choice([0, 1, 2, 3], size=2, replace=False) # 随机采样, 不放回

print(x)
print(idx)
```

## pandas (表格数据处理库)

pandas (表格数据处理库) 的核心是带标签的一维/二维数据:

- `Series` (带标签的一维数据) : 一列数据 + 一个 `Index` (索引)
- `DataFrame` (带标签的二维表格) : 多列 `Series` (一维数据) 组成的表
- `Index` (索引) : 行标签, 会参与对齐

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

索引对齐是 pandas (表格数据处理库) 很重要的模型:

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
df["name"] # 一列, Series (带标签的一维数据) 
df[["name", "score"]] # 多列, DataFrame (带标签的二维表格) 

df.loc[0, "name"] # 按标签
df.iloc[0, 0] # 按位置
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

尽量优先用列运算, 少用逐行 `apply` (逐行应用函数) .

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

- `np.nan` (非数值) : 传统浮点缺失值
- `None` (空值) : Python (编程语言) 空值
- `pd.NA` (缺失值标记) : pandas (表格数据处理库) nullable (可空) dtype (数据类型) 的缺失值

如果整数列有缺失值, 可以使用 nullable integer (可空整数) :

```python
s = pd.Series([1, None, 3], dtype="Int64")
print(s)
```

### dtype (数据类型)

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

- 类别少的字符串列可以转 `category` (分类类型)
- 日期列用 `datetime64` (日期时间类型)
- 布尔缺失可以用 nullable boolean (可空布尔类型)
- 避免无意义的 `object` (对象类型) 列

### groupby (分组计算)

`groupby` (分组计算) 是 split (拆分) -apply (应用) -combine (合并) :

- split (拆分) : 按键拆分数据
- apply (应用) : 对每组计算
- combine (合并) : 合并结果

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

`agg` (聚合) 会把每组压缩成更少的行, `transform` (变换) 会保持原行数.

### merge (连接) , join (连接) , concat (拼接)

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

- `left` (左连接) : 保留左表全部行
- `inner` (内连接) : 只保留两边匹配的行
- `outer` (外连接) : 两边都保留
- `right` (右连接) : 保留右表全部行

建议用 `validate` (关系校验) 检查关系:

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

- `pd.to_datetime(...)` (转为日期时间) : 转日期
- `.dt.year`, `.dt.month`, `.dt.day` (日期字段) : 取出日期字段
- `set_index("date")` (设置索引) : 设置时间索引
- `resample("D" / "W" / "M")` (重采样) : 按时间重采样

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

- 列运算优于 `apply(axis=1)` (逐行应用函数)
- `groupby.agg` (分组聚合) / `transform` (变换) 优于手写循环
- 减少不必要的 `object` (对象类型) dtype (数据类型)
- 读文件时用 `usecols` (仅读取指定列) , `dtype` (数据类型) , `parse_dates` (解析日期)
- 大表优先 Parquet (列式存储文件)
- 先过滤再 join (连接) /groupby (分组计算)
- 单机内存不够时考虑 Polars (高性能表格库) , DuckDB (嵌入式分析数据库) , Dask (并行计算库) , Spark (分布式计算引擎)

```python
# 分块读取大 CSV
chunks = pd.read_csv("big.csv", chunksize=100_000)

total = 0
for chunk in chunks:
    total += chunk["amount"].sum()
```

## Matplotlib

- `Figure`: 整张图
- `Axes`: 一块具体绘图区域, 通常就是一个子图
- `pyplot`: 便捷状态机接口
- 多子图时, `plt.subplots()` 会返回 `Figure` 和 `Axes` 数组

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(6, 4)) # 创建 Figure 和 Axes
ax.plot(x, y, label="sin(x)") # 绘制曲线
ax.set_title("Sine Wave")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.legend() # 根据 label 创建并显示 legend
fig.tight_layout() # 自动调整 layout
plt.show()

fig.savefig("outputs/figures/sine.png", dpi=200, bbox_inches="tight") # 保存
```

### seaborn

- 统计可视化接口, 建在 Matplotlib 之上
- 用 DataFrame 长表直接画图
- 自动处理颜色, 分组, 置信区间等统计展示
- 图好看, 但底层仍可以拿到 Matplotlib 对象继续调

## SciPy

| 模块 | 用途 |
| --- | --- |
| `scipy.linalg` | 线性代数 |
| `scipy.optimize` | 优化, 方程求解, 最小二乘 |
| `scipy.stats` | 概率分布, 统计检验 |
| `scipy.sparse` | 稀疏矩阵 |
| `scipy.sparse.linalg` | 稀疏线性代数 |
| `scipy.signal` | 信号处理 |
| `scipy.fft` | 快速傅里叶变换 |
| `scipy.integrate` | 数值积分, 常微分方程 |
| `scipy.interpolate` | 插值 |

- 稠密矩阵和稀疏矩阵不能混着乱用
- 压缩行稀疏矩阵有三个一维数组
    - `data`: 非零元素
    - `indices`: 非零元素对应的列索引
    - `indptr`: 每行非零元素在 `data` 中的起止位置

### OpenCV

- 将图像视作矩阵, 提供算子

```python
image.shape == (height, width, channels)
image.dtype == np.uint8
```

- channels 中的顺序默认是 BGR
    - BGR: OpenCV 默认
    - RGB: Pillow 默认
    - RGBA: A 表示透明度
    - GRAY: 单通道灰度图
    - HSV: 颜色易于分离
    - LAB: 更符合人眼感知的颜色空间
    - YUV: 视频常用

```python
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
```

- shape 中是 (H, W, C), 但很多几何 API 用 (W, H)
    - 本质是矩阵语义与几何语义的区别

```python
h, w = image.shape[:2]
resized = cv2.resize(image, (new_w, new_h)) # 注意 resize 的 size 是 (width, height)

point = (x, y) # 用 (x, y) 表示点
pixel = image[y, x] # 用 (y, x) 访问像素
```

#### 数据运算

- OpenCV 的数据类型和数值范围
    - uint8: 0~255
    - uint16: 0~65535
    - float32: 通常约定为 0~1 (颜色转换中是的), 但不一定

```python
image.astype(np.float32) # 转为 float32, 但数值范围仍然是 0~255

image.astype(np.float32) / 255.0 # 归一化到 0~1
```

- OpenCV 的加法和 NumPy 的加法不同
    - NumPy 的无符号整数加法是模运算, 会溢出回绕
    - OpenCV 的加法是饱和运算, 会饱和到最大值

#### 插值

- 所有变换都会将原始坐标映射到输出坐标, 但输出坐标通常不是整数
    - INTER_NEAREST: 最近邻插值, 直接取最近的像素
    - INTER_LINEAR: 双线性插值, 根据四个邻居加权平均
    - INTER_CUBIC: 双三次插值, 根据 16 个邻居加权平均
    - INTER_AREA: 面积重采样, 适合缩小图像
    - INTER_LANCZOS4: Lanczos 插值, 根据 8 个邻居加权平均

```python
mask = cv2.resize(mask, size, interpolation=cv2.INTER_NEAREST)
# mask 不可以线性插值, 否则类别 0 和类别 2 之间可能被插值出类别 1
```

#### 卷积

- 用一个局部邻域或 kernel 检查每个像素
    - kernel: 卷积核
    - kernel size: 卷积核大小
    - anchor: 锚点, 卷积核中心点
    - stride: 步幅, 卷积核移动的步长
    - padding: 填充, 卷积核超出边界时的处理
    - output depth: 输出通道数
- 图像边缘没有足够邻居, 所以必须决定边界之外是什么 (borderType)
    - `cv2.BORDER_CONSTANT`: 常数填充, 用指定值填充
    - `cv2.BORDER_REPLICATE`: 复制边缘像素
    - `cv2.BORDER_REFLECT`: 镜像填充, 反射
    - `cv2.BORDER_WRAP`: 循环填充, 从另一边取

#### 处理能力

- 颜色空间转换
- 几何变换
- 图像滤波
    - 均值滤波
    - 高斯滤波: 近的像素权重大, 远的像素权重小
    - 中值滤波: 取邻域中值, 去除椒盐噪声
    - 双边滤波: 高斯 + 亮度差值越小权重越大, 保边缘
- 阈值 / 掩码
- 形态学
    - 腐蚀: 让前景变小, 去除噪点
    - 膨胀: 让前景变大, 填充空洞
    - 开运算: 先腐蚀再膨胀, 去除小物体
    - 闭运算: 先膨胀再腐蚀, 填充小孔洞
- 边缘检测: 找颜色变化明显的地方
- 仿射与透视变换:
    - 仿射变换: 保持平行线, 但不保持角度和长度
    - 透视变换: 可以改变平行线, 适合透视校正
- 其它
    - 特征点
    - 光流
    - 模板匹配
    - 深度恢复
    - PnP: 通过已知 3D 点和对应的 2D 点, 求解相机位姿
    - 单应矩阵: 通过已知 4 个点的对应关系, 求解透视变换矩阵
    - 相机标定: 通过已知的棋盘格图像, 求解相机内参和畸变参数

### Pillow

- 模式表达颜色空间 / 通道数 / 位深
    - 默认 RGB
- `size` 是 `(width, height)`
- `PIL.Image.Image`
- `Image.open()` 是惰性解码, 只有访问像素或调用 `load()` 时才真正解码
    - `image = image.convert("RGB")` 会返回新对象, 原始文件不需要保持打开

#### `mode`

- `1` 二值图
- `L` 8 位灰度图
- `P` 调色板图
    - `P` 模式的像素值是调色板索引
- `RGB` 三通道彩色图
- `RGBA` RGB + Alpha
- `CMYK` 印刷颜色
- `I` 32 位整数
- `F` 32 位浮点

#### 操作

```python
# 返回新对象
image.resize(...) # 调整图像尺寸
image.crop(...) # 裁剪指定区域
image.rotate(...) # 旋转图像
image.convert(...) # 转换图像模式
image.transpose(...) # 翻转或旋转图像

# 原地修改
image.paste(...) # 将另一张图像或颜色粘贴到指定区域
image.thumbnail(...) # 按比例生成缩略图, 不超过指定尺寸
image.putpixel(...) # 修改指定坐标处的单个像素
```

#### Alpha 影响操作行为

```python
Image.blend(...) # 使用全局固定比例混合两张图
Image.composite(...) # 使用 Mask 决定每个位置选哪张图
Image.alpha_composite(...) # 按照两张 RGBA 图像自身的 Alpha 做合成
image.paste(..., mask=...) # 把内容写进目标图, 可以提供 Mask
```

#### EXIF Orientation

- 旋转是个麻烦事, 许多图像格式用 EXIF Orientation 标签声明显示时旋转, 但底层像素数据没有旋转

```python
from PIL import ImageOps

image = ImageOps.exif_transpose(image) # 根据 EXIF Orientation 实际旋转或翻转像素
```

#### 模型预处理

```python
image = Image.open(path) # 打开文件
image = ImageOps.exif_transpose(image) # 根据 EXIF Orientation 实际旋转或翻转像素
image = image.convert("RGB") # 转为 RGB 模式
image = image.resize((width, height)) # 调整图像尺寸

array = np.asarray(image) # 三通道, 8 位无符号整数
tensor = torch.from_numpy(array) # 转为张量, 维度顺序仍为 (W, H, C)
tensor = tensor.permute(2, 0, 1) # 调整为 (C, H, W) 顺序
tensor = tensor.float() / 255.0 # 归一化到 [0, 1] 范围
tensor = tensor.unsqueeze(0) # 增加 batch 维度, 变为 (1, C, H, W)
```

## scikit-learn

TODO

## PyTorch

PyTorch (深度学习框架) 的核心模型:

- `Tensor` (张量) : 类似 NumPy (数值计算库) 数组, 但可以放到 GPU (图形处理器)
- autograd (自动求导) : 根据 Tensor (张量) 运算自动构建计算图, 反向传播求梯度
- `nn.Module` (神经网络模块) : 模型层和参数的容器
- loss (损失) : 衡量预测和目标差距
- optimizer (优化器) : 根据梯度更新参数
- `Dataset` (数据集) / `DataLoader` (数据加载器) : 数据集和批量加载

### Tensor (张量)

```python
import torch

x = torch.tensor([[1.0, 2.0], [3.0, 4.0]])

print(x.shape)
print(x.dtype)
print(x.device)
```

device (设备) :

```python
device = "cuda" if torch.cuda.is_available() else "cpu" # cuda (英伟达 GPU 计算平台) / cpu (中央处理器) 

x = x.to(device)
```

NumPy (数值计算库) 转 Tensor (张量) :

```python
import numpy as np
import torch

arr = np.array([1, 2, 3], dtype=np.float32)
t = torch.from_numpy(arr)

print(t)
```

### autograd (自动求导)

```python
import torch

x = torch.tensor([2.0], requires_grad=True)
y = x ** 2 + 3 * x

y.backward()

print(x.grad) # dy/dx = 2x + 3, x=2 时为 7
```

训练时一般流程:

```python
optimizer.zero_grad() # 清空上一轮梯度
loss.backward() # 反向传播, 计算梯度
optimizer.step() # 用梯度更新参数
```

如果忘了 `zero_grad()`, 梯度会累积.

### nn.Module (神经网络模块)

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

print(y.shape) # (4, 1)
```

### Dataset (数据集) 和 DataLoader (数据加载器)

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

device = "cuda" if torch.cuda.is_available() else "cpu" # cuda (英伟达 GPU 计算平台) / cpu (中央处理器) 

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

### PyTorch (深度学习框架) 性能边界

优先检查:

- 数据和模型是否在同一个 device (设备)
- dtype (数据类型) 是否匹配, 常见训练用 `float32` (32 位浮点数)
- batch size (批量大小) 是否过小导致 GPU (图形处理器) 吃不满
- `DataLoader` (数据加载器) 是否成为瓶颈
- 推理时是否用了 `model.eval()` (切换评估模式) 和 `torch.no_grad()` (关闭梯度计算)
- 是否频繁 CPU (中央处理器) /GPU (图形处理器) 来回拷贝

```python
# 不要在训练循环里频繁 .cpu().numpy(), 这会打断 GPU (图形处理器) 流水线
```
