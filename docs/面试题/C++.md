# C++ 面试题

## 并发

### `std::atomic` 与内存模型

- CAS 操作
    - 比较并交换 (Compare-And-Swap, CAS) 是一种用于实现并发算法的基本操作
    - 它包含三个操作数: 内存位置 V, 预期值 A 和新值 B
    - CAS 操作的原子性确保了在多个线程同时访问共享变量时, 只有一个线程能够成功地将变量的值从 A 交换为 B
- ABA 问题
    - ABA 问题是指在使用 CAS 操作时, 线程 A 读取了共享变量的值 A, 然后线程 B 改变了共享变量的值为 B, 最后线程 A 再次使用 CAS 操作将共享变量的值从 B 交换为 A
    - 尽管线程 A 成功地将共享变量的值从 A 交换为 B, 但是线程 A 并不知道共享变量的值在中间被改变过
    - 为了解决 ABA 问题, 通常会在共享变量中添加一个版本号或时间戳, 每次改变共享变量的值时, 版本号或时间戳也会相应地改变
    - 这样, 线程 A 在使用 CAS 操作时, 就可以检查共享变量的版本号或时间戳是否与预期值相同, 从而避免了 ABA 问题

### `std::thread`

## 类型系统

### 内存对齐

### 栈上创建对象的过程

### 可变性语义与其优化

## 完美转发与引用折叠

## 技术

### 禁止栈 / 堆分配

### 限制对象的数量

### 判断大小端

```C++
#include <iostream>

bool isLittleEndian() {
    uint16_t num = 0x1; // 16-bit number with the least significant byte set to 1
    char* bytePtr = reinterpret_cast<char*>(&num); // Interpret the address of num as a char pointer
    return bytePtr[0] == 1; // Check if the first byte is 1 (little-endian)
}
```
