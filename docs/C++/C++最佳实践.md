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
