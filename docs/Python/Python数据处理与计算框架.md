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
    - `np.str_`: 存定长 Unicode 字符
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

b3 = a.T # 转置视图, 不复制数据, 不连续 (此时连续)
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
- 规则为
    - 如果两个数组的维度数不同, 低维的形状会在左边补 1 (`(3,) + (2, 3) -> (1, 3) + (2, 3)`)
    - 如果两个数组在某个维度上的长度不一样, 其中一个长度为 1, 那么它会被扩展成和另一个一样长 (`(1, 3) + (2, 3) -> (2, 3) + (2, 3)`)
    - 如果两个数组在某个维度上的长度不一样, 且都不为 1, 那么就报错

```python
x = np.array(
    [[1.0, 10.0],
     [2.0, 20.0],
     [3.0, 30.0]]
)

mean = x.mean(axis=0) # 按行聚合求均值 (列均值)
std = x.std(axis=0) # 按行聚合求标准差 (列标准差)
z = (x - mean) / std # 每列减去均值再除以标准差, 得到 z-score

print(z)
```

### ufunc 与向量化

- 逐元素函数
    - `np.add` 逐元素相加
    - `np.sqrt` 逐元素开方
    - `np.exp` 逐元素指数

```python
a = np.arange(1_000_000, dtype=np.float64)

out = (a * 2 + 1) / 3 # 会产生中间数组, 占内存


out = np.empty_like(a) # 预分配输出数组

# 指定 out=, 避免中间数组
np.multiply(a, 2, out=out)
np.add(out, 1, out=out)
np.divide(out, 3, out=out)
```

### axis

- 表示沿哪个维度压缩

```python
a = np.array(
    [[1, 2, 3],
     [4, 5, 6]],
)

print(a.sum()) # 所有元素求和: 21
print(a.sum(axis=0)) # 压掉行维度, 得到每列和: [5 7 9]
print(a.sum(axis=1)) # 压掉列维度, 得到每行和: [6 15]
```

```python
a = np.arange(6).reshape(2, 3)
row_sum = a.sum(axis=1, keepdims=True) # 保留行维度, 方便后续 broadcasting

print(row_sum.shape) # (2, 1)
```

### 线性代数

```python
x = np.array([[1, 2], [3, 4]])
y = np.array([[10], [20]])

print(x @ y) # 矩阵乘法
print(np.linalg.inv(x)) # 逆矩阵
print(np.linalg.solve(x, y)) # 解线性方程 x * a = y
```

### 随机数

```python
rng = np.random.default_rng(seed=42)

x = rng.normal(loc=0, scale=1, size=(3, 2)) # 在正态分布上采样
idx = rng.choice([0, 1, 2, 3], size=2, replace=False) # 随机采样, 不放回

print(x)
print(idx)
```

## pandas

- `Series` : 一列数据 +  `Index`
- `DataFrame`: `Series` 组成的表
- `Index`: 行标签, 会参与对齐

```python
s = pd.Series([10, 20, 30], index=["a", "b", "c"], name="score")
print(s)

df = pd.DataFrame(
    {
        "name": ["alice", "bob", "carol"],
        "age": [18, 20, 19],
        "score": [90.0, 85.5, 88.0],
    }
)

print(df.head()) # 显示前几行
print(df.dtypes) # 显示每列数据类型

# 自动对齐索引, 不同的索引的结果为 NaN
a = pd.Series([1, 2], index=["x", "y"])
b = pd.Series([10, 20], index=["y", "z"])

print(a + b)
```

### 读写数据

```python
from pathlib import Path

import pandas as pd

path = Path("data/sales.csv")

df = pd.read_csv(path)
df.to_csv("data/sales_clean.csv", index=False) # 保存为 CSV, 不保存索引
df.to_parquet("data/sales_clean.parquet", index=False) # 列式存储, 适合大表
```

```python
df = pd.read_csv(
    "data/sales.csv",
    usecols=["date", "region", "amount"], # 只读取指定列
    parse_dates=["date"], # 解析日期列
)
```

### 观察数据

```python
df.head() # 显示前几行
df.tail() # 显示后几行
df.info() # 显示每列数据类型, 非空数量, 内存占用
df.describe() # 显示数值列的统计信息, 包括 count, mean, std, min, 25%, 50%, 75%, max
df.shape # 显示行数和列数
df.columns # 显示列名
df.isna().sum() # 显示每列缺失值数量
```

### 选择数据

```python
df["name"] # Series
df[["name", "score"]] # DataFrame

df.loc[0, "name"] # 行标签, 列标签
df.iloc[0, 0] # 第 0 行第 0 列

# 布尔, `&` 和 `|` 两边要加括号
high_score = df[df["score"] >= 88]
adult = df[(df["age"] >= 18) & (df["score"] >= 85)]
```

### Copy-on-Write

- 从 DataFrame 中选择出来的子集, 对用户而言应当视为一个独立对象
    - 修改子集时, 不会顺带修改原始 DataFrame
    - 需要修改原始 DataFrame 时, 必须直接对原对象进行一次完整赋值

### 链式赋值

- 连续执行两次选择, 再对第二次选择的结果赋值

```python
df[df["score"] >= 60]["passed"] = True # 修改的是临时对象, 不是原始的 df

df.loc[df["score"] >= 60, "passed"] = True # 修改的是原始的 df
```

### 新增和修改列

```python
df1 = df.assign( # 返回加入新列的 DataFrame, 不修改原 DataFrame
    passed=df["score"] >= 60, # 布尔列
    score_level=lambda x: pd.cut( # 分箱, 返回分类列
        x["score"],
        bins=[0, 60, 80, 100],
        labels=["bad", "ok", "good"],
        include_lowest=True, # 包含左端点
    ),
)
```

```python
# 推荐
df["amount_with_tax"] = df["amount"] * 1.13

# 逐行应用函数, 慢
df["amount_with_tax"] = df.apply(lambda row: row["amount"] * 1.13, axis=1)
```

### 缺失值

```python
df.isna() # 显示每个元素是否缺失, 返回布尔 DataFrame
df.dropna(subset=["name"]) # 删除 name 列缺失的行
df.fillna({"score": 0}) # 用 0 填充 score 列缺失值
```

- `np.nan` 传统浮点缺失值
- `None`空值
- `pd.NA` pandas nullable dtype 的缺失值

### dtype

- 常用类型
    - `int64`: 64 位整数
    - `float64`: 64 位浮点数, 可用 `NaN`表示缺失
    - `object`: 任意 Python 对象
    - `category`: 分类类型, 保存分类值及其整数编码, 重复值很多时通常可节省内存
    - `datetime64[ns]`: 无时区日期时间, 精度到纳秒, 缺失值为 `NaT`
    - `timedelta64[ns]`: 时间差, 精度到纳秒, 缺失值为 `NaT`
    - `datetime64[ns, UTC]`: 带时区的日期时间, `UTC` 可替换为其他时区
    - `boolean`: 可空布尔类型, 可存 `True`, `False` 和 `<NA>`
    - `string`: 可空字符串类型
    - `Int64`: 可空 64 位整数
    - `Int32`: 可空 32 位整数
    - `Float64`: 可空 64 位浮点数
    - `Float32`: 可空 32 位浮点数
    - `Sparse[...]`: 稀疏类型, 当大量值等于同一填充值时可节省内存
    - `interval[...]`: 区间类型, 如 `(0, 60]`, 端点可以是整数, 浮点数或日期时间
    - `period[...]`: 周期类型, 如 `period[M]` 或 `period[Q]`, 用于表示规则时间段

### groupby

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
    .groupby("region", as_index=False) # 按 region 分组, 不把 region 作为索引
    .agg(
        total_amount=("amount", "sum"), # 计算每组 amount 的总和保存为 total_amount
        avg_amount=("amount", "mean"), # 计算每组 amount 的平均值保存为 avg_amount
        orders=("amount", "size"), # 计算每组订单数量保存为 orders
    )
)

print(summary)

# 多字段分组
summary = (
    sales
    .groupby(["region", "product"], as_index=False)
    .agg(total=("amount", "sum"))
)
```

```python
sales["region_total"] = sales.groupby("region")["amount"].transform("sum") # 填充回原表, 每行对应分组的总和
sales["ratio"] = sales["amount"] / sales["region_total"] # 计算每行占分组总和的比例
```

### 连接

```python
orders = pd.DataFrame(
    {"order_id": [1, 2, 3], "user_id": [10, 20, 10], "amount": [99, 30, 50]}
)

users = pd.DataFrame(
    {"user_id": [10, 20], "name": ["alice", "bob"]}
)

df = orders.merge(users, on="user_id", how="left") # 返回新 DataFrame
print(df)
```

- `left`: 保留左表全部行
- `inner`: 只保留两边匹配的行
- `outer`: 两边都保留
- `right`: 保留右表全部行

```python
# validate 仅表示校验
orders.merge(users, on="user_id", how="left", validate="many_to_one")
```

```python
# 纵向拼接, 重新生成索引
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
weekly = df.resample("W").sum() # 按周重采样, 求每周总和
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

## OpenCV

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

### 数据运算

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

### 插值

- 所有变换都会寻找输出坐标的原始坐标, 但计算结果通常不是整数
    - INTER_NEAREST: 最近邻插值, 直接取最近的像素
    - INTER_LINEAR: 双线性插值, 根据四个邻居加权平均
    - INTER_CUBIC: 双三次插值, 根据 16 个邻居加权平均
    - INTER_AREA: 面积重采样, 适合缩小图像
    - INTER_LANCZOS4: Lanczos 插值, 根据 8*8 邻域加权平均

```python
mask = cv2.resize(mask, size, interpolation=cv2.INTER_NEAREST)
# mask 不可以线性插值, 否则类别 0 和类别 2 之间可能被插值出类别 1
```

### 卷积

- 用一个局部邻域或 kernel 检查每个像素
    - kernel: 卷积核
    - kernel size: 卷积核大小
    - anchor: 锚点, 卷积核中心点
    - stride: 步幅, 卷积核移动的步长
    - padding: 填充, 卷积核超出边界时的处理
    - output depth: 输出类型
- 图像边缘没有足够邻居, 所以必须决定边界之外是什么 (borderType)
    - `cv2.BORDER_CONSTANT`: 常数填充, 用指定值填充
    - `cv2.BORDER_REPLICATE`: 复制边缘像素
    - `cv2.BORDER_REFLECT`: 镜像填充, 反射
    - `cv2.BORDER_WRAP`: 循环填充, 从另一边取

### 处理能力

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

## Pillow

- 模式表达颜色空间 / 通道数 / 位深
    - 默认 RGB
- `size` 是 `(width, height)`
- `PIL.Image.Image`
- `Image.open()` 是惰性解码, 只有访问像素或调用 `load()` 时才真正解码
    - `image = image.convert("RGB")` 会返回新对象, 原始文件不需要保持打开

### `mode`

- `1` 二值图
- `L` 8 位灰度图
- `P` 调色板图
    - `P` 模式的像素值是调色板索引
- `RGB` 三通道彩色图
- `RGBA` RGB + Alpha
- `CMYK` 印刷颜色
- `I` 32 位整数
- `F` 32 位浮点

### 操作

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

### Alpha 影响操作行为

```python
Image.blend(...) # 使用全局固定比例混合两张图
Image.composite(...) # 使用 Mask 决定每个位置选哪张图
Image.alpha_composite(...) # 按照两张 RGBA 图像自身的 Alpha 做合成
image.paste(..., mask=...) # 把内容写进目标图, 可以提供 Mask
```

### EXIF Orientation

- 旋转是个麻烦事, 许多图像格式用 EXIF Orientation 标签声明显示时旋转, 但底层像素数据没有旋转

```python
from PIL import ImageOps

image = ImageOps.exif_transpose(image) # 根据 EXIF Orientation 实际旋转或翻转像素
```

### 模型预处理

```python
image = Image.open(path) # 打开文件
image = ImageOps.exif_transpose(image) # 根据 EXIF Orientation 实际旋转或翻转像素
image = image.convert("RGB") # 转为 RGB 模式
image = image.resize((width, height)) # 调整图像尺寸

array = np.array(image, copy=True) # (H, W, C)
tensor = torch.from_numpy(array) # (H, W, C)
tensor = tensor.permute(2, 0, 1) # 调整为 (C, H, W) 顺序
tensor = tensor.float() / 255.0 # 归一化到 [0, 1] 范围
tensor = tensor.unsqueeze(0) # 增加 batch 维度, 变为 (1, C, H, W)
```

## scikit-learn

TODO

## PyTorch

TODO

## Ray
