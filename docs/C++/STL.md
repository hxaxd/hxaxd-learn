# C++ 标准库

## 参考资料

- [C++ Reference](https://en.cppreference.com/w/)
- STL 源码剖析 TODO

## 程序控制

- `std::abort()` 立即终止程序, 不进行清理
- `std::atexit(clean())` 注册程序终止时调用的清理函数
- `std::exit()` 终止程序, 调用已注册的清理函数 (最后注册的首先调用), 不调用局部对象的析构函数
- `std::quick_exit()` 与 `std::at_quick_exit()` 终止程序, 不清理静态对象
- `std::terminate()` 调用终止处理程序, 默认调用 `std::abort()`
- `std::unreachable()` 告诉编译器该代码路径不可达, 允许编译器进行优化
- `std::stacktrace::current()` 获取当前堆栈跟踪信息, 需要 C++23 支持
- `std::stacktrace_entry` 获取每一层堆栈信息, 包括函数名、文件名、行号等

### 断言

- `assert(condition)` 在调试模式下检查 `condition`, 失败时打印错误信息并调用 `std::abort()`
- `static_assert(condition, "message")` 在编译时检查 `condition`, 失败时打印 `message`

## 字符串

- `std::ssize()` 返回有符号整数类型, 用于表示容器大小
- 字面量后缀
    - `using namespace std::string_literals`, 导入 `std::string` 的字面量 (适用于类型推导)
    - `"hello"s` 是 `std::string` 类型, 注意这是创建了一个新的临时字符串对象
    - `"hello"sv` 是 `std::string_view` 类型
- `std::string_view`
    - 是不可变字符串视图, 不拥有字符串数据, 支持 `constexpr`
    - 适用于传递只读字符串参数, 避免不必要的字符串拷贝
    - 不会隐式转换为 `std::string`, 但可以显式转换
    - 相较于 `const std::string&`, 可以接受字符串字面量和 C 风格字符串而不需创建临时 `std::string` 对象, 并且不会延长临时对象的生命周期
    - 不要使用 `std::string` 字面量初始化 `std::string_view` 对象, 会创建临时 `std::string` 对象, 并立刻销毁, 导致悬空视图
    - 修改原有字符串会导致视图悬空
    - `std::string_view` 不一定以空字符结尾

```C++
std::string_view func(std::string_view sv) {
    sv.remove_prefix(1); // 删除第一个字符
    sv.remove_suffix(1); // 删除最后一个字符
    return sv;
}

std::string_view sv {func("hello"s)}; // 错误: 悬空视图

std::string s {func("hello"s)}; // 正确

if (str.find("abc") != string::npos); // 检查子字符串是否存在

if (str.contains("abc")); // C++23 语法糖

str.c_str(); // 获取 C 风格字符串, 注意返回的指针指向的字符串数据必须以空字符结尾
```

### `std::format`

TODO

### `std::print` / `std::println`

## 随机数

- `std::random_device` 用于生成非确定性随机数种子
- `std::chrono::steady_clock` 亦可
- `std::mt19937` Mersenne Twister 算法, 速度快, 周期长, 适合大多数用途
- `std::uniform_int_distribution` 均匀整数分布

```C++
// 使用 steady_clock 为 Mersenne Twister 生成种子
std::mt19937 mt{ static_cast<std::mt19937::result_type>(
    std::chrono::steady_clock::now().time_since_epoch().count()
    // std::random_device{}() // 也可以使用随机设备, 但有些实现并非非确定性
    ) };

// 创建可复用的随机数分布, 生成 1 到 6 之间的均匀整数
std::uniform_int_distribution<int> die6{ 1, 6 }; // C++14 可写为 std::uniform_int_distribution<> die6{ 1, 6 };

// 打印一堆随机数
for (int count{ 1 }; count <= 40; ++count)
{
    std::cout << die6(mt) << '\t'; // 生成一次掷骰子结果

    // 每打印 10 个数字换行
    if (count % 10 == 0)
        std::cout << '\n';
}
```

- 考虑 `std::seed_seq` 用于生成更高质量的随机数序列

```C++
std::random_device rd{};
std::seed_seq ss{ rd(), rd(), rd(), rd(), rd(), rd(), rd(), rd() }; // 使用多个随机设备值初始化种子序列

std::mt19937 mt{ ss }; // 使用种子序列初始化 Mersenne Twister

std::uniform_int_distribution die6{ 1, 6 };

for (int count{ 1 }; count <= 40; ++count)
{
 std::cout << die6(mt) << '\t';
 if (count % 10 == 0)
  std::cout << '\n';
}
```

## 容器

- 实现特定接口的标准库类型才叫容器
    - `std::string` 不是
    - `std::vector<bool>` 不是
    - C 风格数组不是
- 通常提供列表初始化函数
    - 这可能导致无法使用 `{}` 初始化调用其它构造函数
    - 也可以用 `std::vector<int> vec{std::vector<int>(10, 42)};` 规避
- 除了 `std::array` 外, 容器都使用 `std::allocator` 分配内存
    - 这导致容器的 `T::size_type` 都是 `std::size_t`
- 容器都会实现 `.size()`
    - 推荐使用 `std::size` /  `std::ssize` 获得非容器的兼容性
    - 其实对于容器就是调用它们的 `.size()` 方法
- `.erase()`
    - 序列容器删除元素后可能导致迭代器失效 -> `it = vec.erase(it);`
    - 但是请记住, 用循环说明你没明白 STL, 请使用 `std::erase` 语法糖, 这对于序列容器会调用 `std::remove_if` 来移动元素, 然后调用容器的 `.erase()` 来删除多余的元素
        - 显然, 对于关联容器, `std::erase` 会直接调用容器的 `.erase()` 来删除元素
- 自定义比较时, 请严格定义 `<` 运算符, 以满足严格弱排序要求 (等价关系必须返回 `false`)

### `std::initializer_list`

- 编译器看到初始化列表时, 会自动将其转换为 `std::initializer_list`
- `std::initializer_list` 是一个轻量级的不可变数组视图, 包含指向元素的指针和大小
- 不能使用 `[]` 下标访问元素, 只能使用迭代器或范围 `for` 语句
- `{}` 会优先匹配 `std::initializer_list` 构造函数
    - 导致无法使用 `{}` 初始化调用其它构造函数

### `std::vector`

- 遗憾的是 `std::vector` 不能是 `constexpr` 的
- 容器适配器
    - `std::priority_queue` 适配器, 默认底层容器为 `std::vector`, 维护一个堆结构, 允许快速访问极值元素
- 所有移除元素的操作都会调用元素的析构函数, 但不会释放内存, 内存会被保留以供未来使用, 直到容器被销毁或显式调用 `shrink_to_fit()`
    - 内置类型的析构函数是空的, 因此移除元素不会有任何效果

```C++
std::vector<int> vec {1, 2, 3, 4, 5}; // 列表初始化

vec[0u] = 10;
vec.at(0u) = 20; // 带边界检查的访问
vec.data(); // 返回指向底层数组的指针
vec.data()[0] = 30; // 通过指针访问底层数组, 不会有窄化报错

// 容量与大小的区别主要体现在栈行为
vec.resize(10); // 调整大小与容量
vec.reserve(20); // 预留容量, 不改变大小

vec.push_back(42); // 在末尾添加元素
vec.pop_back(); // 移除末尾元素
vec.emplace_back(43); // 直接在末尾构造元素, 完美转发参数, 但可以调用显示构造函数

vec.erase(vec.remove_if([](int x) { return x % 2 == 0; }), vec.end()); // 移除所有偶数元素, 注意 remove_if 返回新的逻辑结尾迭代器
std::erase(vec.begin(), vec.end(), [](int x) { return x % 2 == 0; }); // 语法糖
```

### `std::array`

- 可以是 `constexpr` 的, 显然长度必须是常量表达式
- `std::array` 是一个聚合类型, 可以使用聚合初始化
- `const arr&` 形参的 `std::size` 结果不是 `constexpr` 的, 这是一个缺陷

```C++
std::array<int, 5> arr {1, 2, 3, 4, 5};

// 问题来了, CTAD 无法只省略一个模板参数, 如果我需要指定类型, 但不想指定大小怎么办
std::array arr2 { std::to_array<short>({1, 2, 3, 4, 5}) }; // 使用 std::to_array 函数, 注意会创建一个临时数组对象

arr[0] = 10;
arr.at(0) = 20; // 带边界检查的访问
std::get<0>(arr) = 30; // 通过 std::get 访问元素, 实现编译时边界检查

std::array arr3 {
    MyClass{1},
    MyClass{2},
    MyClass{3}
}

std::array arr4 {{
    {1},
    {2},
    {3}
}} // 双花括号才可以, 原因好长, 回忆一下哦
```

### `std::set` 与 `std::map`

- `std::map<const Key, T>` 本质上就是 `std::set<pair<const Key, T>>`
- `std::multiset` 允许重复键, 相同时插在右边 (排序是稳定的)
- `std::set` 的元素与 `std::map` 的键都是 const 的, 因为它们的排序依赖于该值, 修改会破坏容器的内部结构

```C++
std::map<std::string, int> myMap {
    {"one", 1},
    {"two", 2},
    {"three", 3}
};

// 检查键是否存在
if (myMap.find("two") != myMap.end());

if (myMap.contains("two"));

if (myMap["four"] == 1); // 若键不存在, 会插入一个默认值 (0), 然后返回该值的引用, 注意这可能会修改容器

if (myMap.at("four") == 1); // 若键不存在, 会抛出 std::out_of_range 异常

myMap.insert({"four", 4}); // 插入一个键值对, 如果键已存在则不插入
if (myMap.insert_or_assign("four", 4).second); // 插入或更新键值对, 返回一个 pair, 其中 .second 是一个 bool, 表示是否插入了新元素
```

### `std::unordered_set` 与 `std::unordered_map`

- 基于哈希表实现, 提供平均常数时间复杂度的查找、插入和删除操作
- 需要提供哈希函数和相等比较函数, 默认使用 `std::hash` 和 `std::equal_to`

### `std::deque`

- 双端队列, 支持在两端高效地添加和删除元素
- 内部实现为分段连续内存, 一个数组指向多个固定大小的块, 每个块存储一定数量的元素
- 容器适配器
    - `std::stack` 适配器, 默认底层容器为 `std::deque`, 只允许在一端添加和删除元素
    - `std::queue` 适配器, 默认底层容器为 `std::deque`, 只允许在一端添加元素, 另一端删除元素

### `std::list`

### `std::bitset`

```C++
std::bitset<8> bits {}; // 8 位, 全部初始化为 0

bits.set(3); // 将第 3 位设置为 1
bits.reset(3); // 将第 3 位设置为 0
bits.flip(2); // 翻转第 2 位
bits.test(1); // 测试第 1 位是否为 1, 返回 bool
bits.count(); // 返回为 1 的位数
bits.size(); // 返回位数
bits.to_string(); // 返回字符串表示

constexpr std::uint8_t mask0{ 0b0000'0001 }; // 位掩码
```

## 迭代器

- 支持 `++` / `--` / `*` / `->` / `[]` 等操作符, 以及与其他迭代器的比较
- 功能
    - 随机访问迭代器支持所有操作
    - 双向迭代器支持 `++` 和 `--`
    - 前向迭代器支持 `++`, 可重复使用
    - 输出迭代器支持单向单次写入
    - 输入迭代器支持单向单次读取
- 迭代器类型
    - 指向类型
    - 距离类型
    - 指针类型
    - 引用类型
    - 分类标签 -> 就是迭代器的功能分类
- 通过 tag dispatching 实现算法对不同类型迭代器的优化
- 迭代器适配器
    - `std::reverse_iterator` 适配器, 反向迭代器, 使得算法可以从后向前遍历容器
    - `std::move_iterator` 适配器, 移动迭代器, 使得算法可以移动元素而不是复制
    - `std::back_insert_iterator` 适配器, 后插入迭代器, 使得算法可以在容器末尾添加元素
    - `std::front_insert_iterator` 适配器, 前插入迭代器, 使得算法可以在容器前面添加元素
    - `std::insert_iterator` 适配器, 插入迭代器, 使得算法可以在容器的任意位置添加元素

### 查找与遍历

- `std::for_each` 对范围内的每个元素执行函数, 不修改返回值, 但函数可以有副作用
- `std::find` / `std::find_if` / `std::find_if_not` 在范围内查找第一个满足特定条件的元素
    - `std::find` 查找等于给定值的元素
    - `std::find_if` 查找满足谓词的元素
- `std::find_end` 在范围内查找最后一次出现的子序列
- `std::find_first_of` 在范围内查找与另一范围中任意元素匹配的第一个元素
- `std::adjacent_find` 查找范围内第一对相邻的重复元素
- `std::count` / `std::count_if` 统计范围内满足特定条件的元素个数
- `std::mismatch` 比较两个范围, 返回第一对不匹配元素的迭代器 pair
- `std::equal` 检查两个范围内的元素是否完全相等
- `std::search` 在范围内查找第一个匹配的子序列
    - `std::search_n` 查找连续 n 个满足条件的元素

### 修改与替换

- `std::transform` 对输入范围的每个元素应用一个函数, 将结果存储在输出范围中
    - 注意输出范围必须至少与输入范围一样大, 否则会导致未定义行为
- `std::copy` / `std::copy_if` / `std::copy_n` / `std::copy_backward` 将元素从一个范围复制到另一个范围
    - `std::copy_backward` 从后往前复制, 适用于输出范围与输入范围重叠且输出起点在输入起点之后的情况
- `std::move` / `std::move_backward` 将元素移动(move语义)到另一个范围
- `std::fill` / `std::fill_n` 将给定值赋值给范围内的所有元素
- `std::generate` / `std::generate_n` 使用生成器函数的返回值赋值给范围内的元素
- `std::replace` / `std::replace_if` / `std::replace_copy` 将范围内满足条件的元素替换为新值
- `std::iota` 用顺序递增的值填充范围 (位于 numeric 头文件)

### 删除与重排

- `std::remove` / `std::remove_if` 移除满足条件的元素, 将保留的元素移到范围前端, 返回新的逻辑结尾
    - 注意此算法不调整容器大小, 通常配合 erase 使用 (Erase-Remove Idiom)
- `std::remove_copy` / `std::remove_copy_if` 将不满足条件的元素复制到输出范围
- `std::reverse` / `std::reverse_copy` 将范围内的元素顺序反转
- `std::rotate` / `std::rotate_copy` 将范围内的元素进行循环移动
    - 常用于将缓冲区某部分移到前面
- `std::shuffle` 将范围内的元素随机打乱 (C++11起)

### 排序

- `std::sort` 对范围内的元素进行升序排序
- `std::stable_sort` 保持相等元素的相对顺序, 但可能更慢
- `std::partial_sort` / `std::partial_sort_copy` 只对前 N 个元素进行排序
- `std::nth_element` 将第 N 大的元素放到第 N 个位置, 且左边元素都小于它, 右边都大于它
- `std::is_sorted` 检查范围是否已经排序
- `std::is_sorted_until` 返回第一个未排序元素的迭代器
- 去重
    - `std::unique` 移动相邻重复元素到范围末尾, 返回新的逻辑结尾迭代器, 但不删除元素
    - `std::unique_copy` 将相邻重复元素复制到输出范围, 返回输出范围的结尾迭代器

### 二分查找

- `std::lower_bound` / `std::upper_bound` / `std::equal_range` 在已排序范围内查找目标元素的位置
    - `std::lower_bound` 返回第一个不小于目标元素的位置
    - `std::upper_bound` 返回第一个大于目标元素的位置
    - `std::equal_range` 返回一个 pair, 包含 lower_bound 和 upper_bound 的结果
- `std::binary_search` 在已排序范围内检查元素是否存在, 返回布尔值

### 有序集合操作

- `std::set_union` / `std::set_intersection` / `std::set_difference` / `std::set_symmetric_difference` 对两个已排序范围执行集合操作, 结果存储在输出范围中
    - 注意输出范围必须至少与输入范围的总大小一样大, 否则会导致未定义行为
- `std::includes` 检查一个已排序范围是否包含另一个已排序范围
- `std::merge` 将两个已排序范围合并成一个已排序范围, 结果存储在输出范围中
    - 注意输出范围必须至少与输入范围的总大小一样大, 否则会导致未定义行为
- `std::inplace_merge` 将一个已排序范围的两个连续子范围合并成一个已排序范围, 结果存储在原范围中

### 堆操作

- 适用于随机访问迭代器的算法
- `std::make_heap` 将范围内的元素组织成一个堆
- `std::push_heap` 将范围内的最后一个元素添加到堆中
- `std::pop_heap` 将堆顶元素移到范围内的最后一个位置, 但不删除它
- `std::sort_heap` 将堆中的元素排序, 结果是一个升序排列

### 最值与排列

- `std::min_element` / `std::max_element` 返回范围内最小或最大元素的迭代器
- `std::minmax_element` 同时返回最小和最大元素的迭代器 pair
- `std::next_permutation` 将范围内的元素重排为字典序的下一个排列, 如果存在返回 true
- `std::prev_permutation` 将范围内的元素重排为字典序的上一个排列

## tuple-like 类型

- 实现 `std::tuple_size` 和 `std::tuple_element` 模板特化的类型, 可以使用 `std::get` 访问元素
- 该类型 + 聚合 + 数组可以被结构化绑定 -> `auto [x, y, z] = tuple_like;`

### `std::tuple`

TODO

### `std::pair`

## 视图

### `std::span`

### `std::view`

### `std::mdspan`

```C++
int data[6] = {1, 2, 3, 4, 5, 6};
std::mdspan mdspan1 {data, 2, 3}; // 创建一个 mdspan 视图

mdspan1.extents().extent(0) // 获取第 0 维的大小
mdspan1.extents().extent(1) // 获取第 1 维的大小

mdspan1.data_handle()[3] // 访问底层指针
mdspan1[0, 0] = 20; // 也可以使用下标访问
```

## Ranges

### `std::ranges::transform`

## 类型

### `std::function`

```C++
std::function<int(int, int)> foo1 = [](int a, int b) { return a + b; }; // 使用 lambda 表达式创建一个 std::function 对象
std::function<int(int, int)> foo2 = std::plus{}; // 使用函数对象创建一个 std::function 对象
std::function<int(int, int)> foo3 {&fun1} // 使用函数指针创建一个 std::function 对象, 注意要取地址符
```

### `std::bind`

### `std::variants` / `std::visit`

### `std::reference_wrapper`

- 表现出引用的行为
    - `=` 会改变引用的对象, 而不是被引用的对象
    - 会被隐式转换为引用类型
    - `.get()` 返回被引用的对象的引用

```C++
int x = 1, y = 2, z = 3;

std::vector<std::reference_wrapper<int>> vec {std::ref(x), std::ref(y), std::ref(z)};

// 没有 CTAD 的原始人会这样做
auto ref = std::ref(x); // 创建一个 std::reference_wrapper<int>
auto cref = std::cref(x); // 创建一个 std::reference_wrapper<const int>
```

### `std::optional`

- 有可能无值, 解引用前要检查

```C++
std::optional<int> divide(int a, int b) {
    if (b == 0) {
        return std::nullopt; // 返回空的 optional
    }
    return a / b; // 返回结果
}

int main() {
    auto result = divide(10, 2);
    if (result) {
        std::cout << "Result: " << *result << std::endl; // 解引用 optional 获取值
        std::cout << "Result: " << result.value() << std::endl; // 或者使用 value() 方法获取值
        std::cout << "Result: " << result.value_or(-1) << std::endl; // 或者使用 value_or() 提供默认值
    } else {
        std::cout << "Division by zero!" << std::endl;
    }
    return 0;
}
```

### `std::any`

TODO

### `std::expected`

- 不可能无值, 但可能有错误

## 智能指针

### `std::unique_ptr`

- `std::make_unique<T>(args...)` 创建一个指向类型 `T` 的智能指针, 并完美转发参数 `args...` 给 `T` 的构造函数
- 禁用复制语义, 只支持移动语义保证唯一所有权

### `std::shared_ptr`

- 可以用 `unique_ptr` 初始化, 但反过来不行
- 支持引用计数, 允许多个 `shared_ptr` 指向同一个对象
    - 一定要复制 `shared_ptr`, 而不是重复创建

### `std::weak_ptr`

- 本质是在观察 `shared_ptr` 指向的对象以及控制块, 不拥有对象的所有权
- 通过 `.lock()` 方法获取一个临时的 `shared_ptr`, 如果对象已经被销毁, 则返回持有 `nullptr` 的 `shared_ptr`
    - `.expired()` 方法检查对象是否已经被销毁

## 协程

TODO

## 内存

### `std::allocator`

- 容器级

### `std::pmr`

- 内存池

### 自定义分配

## 元编程

### Concepts

### 工具

- `std::numeric_limits<T>` 提供类型 `T` 的数值特性
    - `std::numeric_limits<T>::max()` 返回类型 `T` 可表示的最大值
    - `std::numeric_limits<T>::min()` 返回类型 `T` 可表示的最小正值 (对于整数类型, 是最小负值)
    - `std::numeric_limits<T>::lowest()` 返回类型 `T` 可表示的最小值
    - `std::numeric_limits<T>::is_signed` 如果类型 `T` 是有符号类型则为 true
    - `std::numeric_limits<T>::is_integer` 如果类型 `T` 是整数类型则为 true
- `std::is_...<>` 检查类型特性
    - 基础类型
    - 复合类型
    - 类 / 函数类型
    - 构造 / 移动 / 拷贝
    - 类型间关系
- `std::..._t<>` 类型变换
    - 移除修饰
    - 添加修饰
    - `std::decay_t<T>` 移除引用和 cv 修饰, 并将数组和函数类型转换为指针类型
- 编译期
    - `std::enabled_if` 条件编译
    - `std::conditional` 条件类型选择
    - `std::void_t` SFINAE 占位类型
