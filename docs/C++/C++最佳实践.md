# C++ 最佳实践

## 参考资料

- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
- Effective C++ 系列书籍

## 使用头文件优化编译时检查

- 源文件应包含其配对的头文件有助于将链接时错误转化为编译时错误 (函数返回值不一致)
- 头文件使用了另一个头文件的内容, 应该直接包含该头文件, 而不是依赖于使用者的包含顺序, 所以我们的包含顺序应该反过来
    - 配对头文件
    - 同项目头文件
    - 第三方库头文件
    - 标准库头文件
- 避免依赖传递包含

## 避免使用无符号整型

- 无符号整型在算术运算中可能导致意外的结果
- 除外情况
    - 位运算
    - 需要明确表示非负值的场景
    - 需要明确的环绕行为的场景

## `new` 和 `delete`

- `operator new` 和 `operator delete` 只分配和释放内存, 不调用构造函数和析构函数
- 与 `malloc` 和 `free` 类似, 但更安全, 因为它们会抛出异常而不是返回空指针

```C++
void* buf {operator new(4)}; // new 为运算符, 只分配空间
My_class* p {new(buf) My_class{}}; // 在 buf 指向的空间上构造一个 int 对象
p->~My_class(); // 必须显式调用析构函数
operator delete(p); // delete 也为运算符, 只释放空间
```

- `new` 和 `delete` 是关键字, 会调用构造函数和析构函数 + `operator new` 和 `operator delete`

```C++
My_class* p {new My_class{}}; // 分配空间并构造对象
delete p; // 调用析构函数并释放空间
```

- 内存分配与构造析构都是编译时确定的, 只有数组的长度可以在运行时确定 (分配的内存块前的块表存储了已分配的相关信息)
- `new (std::nothrow)` 在分配失败时返回空指针而不是抛出异常
- 删除一个空指针是安全的, 不会有任何效果

## CRTP (奇异递归模板模式)

```C++
#include <cstdio>
 
#ifndef __cpp_explicit_this_parameter // Traditional syntax
 
template <class Derived>
struct Base
{
    void name() { static_cast<Derived*>(this)->impl(); }
protected:
    Base() = default; // prohibits the creation of Base objects, which is UB
};
struct D1 : public Base<D1> { void impl() { std::puts("D1::impl()"); } };
struct D2 : public Base<D2> { void impl() { std::puts("D2::impl()"); } };
 
#else // C++23 deducing-this syntax
 
struct Base { void name(this auto&& self) { self.impl(); } };
struct D1 : public Base { void impl() { std::puts("D1::impl()"); } };
struct D2 : public Base { void impl() { std::puts("D2::impl()"); } };
 
#endif
 
int main()
{
    D1 d1; d1.name();
    D2 d2; d2.name();
}
```

## 返回值优化

- 挨个尝试
    - RVO: 直接返回临时对象
    - NRVO: 只返回一个局部对象, 且这个变量初始化后没有被修改过 + 没有地址相关的操作 (如取地址或绑定到引用)
    - 移动语义

## 小问题

- 不要用父类指针遍历子类对象的数组
    - 父类指针算术运算的步长是父类大小, 可能无法正确遍历子类对象
    - `delete[]` 也会有类似问题
- 用枚举给 `std::bitset` 定义位名
- 在 `#include` 后面 `using`
- 用无作用域枚举索引容器
    - 枚举器是隐式 `constexpr` 导致无法赋给变量
    - 通过指定类型抑制隐式 `constexpr`
- 切勿从构造函数或析构函数中调用虚函数
    - 在构造函数或析构函数中调用虚函数时, 对象的动态类型是当前类, 而不是派生类

## 面试题补充

### 并发

#### `std::atomic` 与内存模型

- CAS 操作
    - 比较并交换 (Compare-And-Swap, CAS) 是一种用于实现并发算法的基本操作
    - 它包含三个操作数: 内存位置 V, 预期值 A 和新值 B
    - CAS 操作的原子性确保了在多个线程同时访问共享变量时, 只有一个线程能够成功地将变量的值从 A 交换为 B
- ABA 问题
    - ABA 问题是指在使用 CAS 操作时, 线程 A 读取了共享变量的值 A, 然后线程 B 改变了共享变量的值为 B, 最后线程 A 再次使用 CAS 操作将共享变量的值从 B 交换为 A
    - 尽管线程 A 成功地将共享变量的值从 A 交换为 B, 但是线程 A 并不知道共享变量的值在中间被改变过
    - 为了解决 ABA 问题, 通常会在共享变量中添加一个版本号或时间戳, 每次改变共享变量的值时, 版本号或时间戳也会相应地改变
    - 这样, 线程 A 在使用 CAS 操作时, 就可以检查共享变量的版本号或时间戳是否与预期值相同, 从而避免了 ABA 问题

#### `std::thread`

### 类型系统

#### 内存对齐

#### 栈上创建对象的过程

#### 可变性语义与其优化

### 完美转发与引用折叠

### 技术

#### 禁止栈 / 堆分配

#### 限制对象的数量

#### 判断大小端

```C++
#include <iostream>

bool isLittleEndian() {
    uint16_t num = 0x1; // 16-bit number with the least significant byte set to 1
    char* bytePtr = reinterpret_cast<char*>(&num); // Interpret the address of num as a char pointer
    return bytePtr[0] == 1; // Check if the first byte is 1 (little-endian)
}
```
