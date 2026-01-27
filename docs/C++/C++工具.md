# C++ 工具

## 参考资料

- [Make 与 CMake](https://www.bilibili.com/video/BV1tyWWeeEpp) - 神教程 - 5
- [跟我一起写 Makefile](https://write-makefile-with-me.elabtalk.com/) - 翻译的文档 - 3
- 菜鸟教程 [CMake](https://www.runoob.com/cmake/cmake-tutorial.html) - 精简快速 - 5

## makefile

### 执行步骤

- 读入被 include 的其它 Makefile
- 初始化文件中的变量
- 推导隐式规则, 并分析所有规则
- 为所有的目标文件创建依赖关系链
    - `VPATH = dir:dir # 指定文件搜寻目录`
- 决定哪些目标要重新生成
- 执行生成命令

### 使用

```bash
make # 顺序寻找文件名为 GNUmakefile makefile 和 Makefile 的文件, 构建其中的第一个目标

make obj # 指定目标

make -f name.mk # 指定 make 文件

make -n # 打印命令, 不执行
```

### 注意

- 小心环境变量 `MAKEFILES`
- make 可以一定程度上的自动推导

### make 基础语法

- 注意依赖与命令相同的目标可以写在一起
- make 会打印执行的命令, `@command` 阻止这一行为
- 在命令前面加上 `-`, 表示忽略错误

```Makefile
targets : prerequisites
    command # 注意这个 tab 必须存在
    ...
```

### 变量与命令包

```Makefile
name= f1 f2

define name
命令
endef
```

- 变量用 $(name) 引用
- make 可以使用通配符
- 预设变量
    - `@` 目标文件
    - `<` 第一个依赖文件
    - `^` 所有依赖文件

### 伪目标

```Makefile
.PHONY : clean
clean :
    -rm edit $(objects) # 实现 make clean
```

- 伪目标也可以有依赖, 类似子命令
- 经常声明伪目标 `all` 放在第一个目标, 因为无参数的 `make` 默认构建第一个目标

## Cmake

- `CMakeLists.txt`

```CMakeLists
# PROJECT_BINARY_DIR 是 cmake 系统变量, 意思是执行 cmake 命令的目录

cmake_minimum_required (VERSION 2.8)
# 要求 cmake 版本

project (learn_cmake)
# 指定项目名称

include_directories ( dir )
# 将 dir 目录加入头文件搜索路径

add_subdirectory ( dir )
# 递归调用 dir 目录下的 CMakeLists.txt

aux_source_directory(dir var)
# 将 dir 目录下的所有文件加入 var

set(LIBRARY_OUTPUT_PATH ${PROJECT_BINARY_DIR}/lib)
# 指定库生成到 lib 目录
set(EXECUTABLE_OUTPUT_PATH ${PROJECT_BINARY_DIR}/bin)
# 指定可执行文件生成到 bin 目录

add_executable(hello ${var})
# 生成可执行文件
add_library(lib_name STATIC/SHARED ${var})
# 生成库文件

find_library(var lib_name lib_path1 lib_path2)
# 查找库, 并把库的绝对路径和名称存储到第一个参数里

target_link_libraries ( hello lib1 lib2 )
# 将 lib1 lib2 加入 target 的链接库

add_compile_options ( hello PRIVATE "-Wall" )
# 将"-Wall"加入编译选项
```

- 执行 `cmake .` 生成 Makefile
- 执行 `make` 生成可执行文件

## GCC/G++

- `-g` 生成调试信息
- `-O0/-O1/-O2/-O3/-Ofast` 优化等级
- `-Wall` 打开大部分警告
- `-Werror` 将警告视为错误
- `-Wextra` 打开额外警告
- `-Wpedantic` 打开标准兼容警告
- `-fsanitize=address` 地址检测
- `-fsanitize=undefined` 未定义行为检测
- `-I dir` 添加头文件搜索路径

## GDB

- 操作
    - 单步进入: 执行一行代码, 遇到函数时进入函数
    - 单步跳过: 执行一行代码, 遇到函数时直接执行完函数
    - 跳出: 执行完当前函数并返回调用处
    - 运行到某行
    - 继续: 运行程序直到下一个断点或结束
    - 设置下一行: 修改下一条要执行的代码行
- 打印变量 & 打印堆栈
- `ulimit -c unlimited` 开启核心转储
- `gdb ./a.out` 调试可执行文件
- `gdb ./core.12345` 调试核心转储文件, 12345 是进程号
    - `bt` 打印调用栈
    - `info locals` 打印局部变量
    - `info args` 打印参数
    - `print var` 打印变量 var 的值

## valgrind

## gprof

## strace

## ldd
