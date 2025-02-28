# C++ 工具

## 参考资料

* [Make 与 CMake](https://www.bilibili.com/video/BV1tyWWeeEpp) - 神教程 - 5
* [跟我一起写 Makefile](https://write-makefile-with-me.elabtalk.com/) - 翻译的文档 - 3
* 菜鸟教程 [CMake](https://www.runoob.com/cmake/cmake-tutorial.html) - 精简快速 - 5

## makefile

### 执行步骤

* 读入被 include 的其它 Makefile
* 初始化文件中的变量
* 推导隐式规则, 并分析所有规则
* 为所有的目标文件创建依赖关系链
    * `VPATH = dir:dir # 指定文件搜寻目录`
* 决定哪些目标要重新生成
* 执行生成命令

### 使用

```shell
make # 顺序寻找文件名为 GNUmakefile makefile 和 Makefile 的文件, 构建其中的第一个目标

make obj # 指定目标

make -f name.mk # 指定 make 文件

make -n # 打印命令, 不执行
```

### 注意

* 小心环境变量 `MAKEFILES`
* make 可以一定程度上的自动推导

### make 基础语法

* 注意依赖与命令相同的目标可以写在一起
* make 会打印执行的命令, `@command` 阻止这一行为
* 在命令前面加上 `-`, 表示忽略错误

```Makefile
targets : prerequisites
    command # 注意这个tab必须存在
    ...
```

### 变量与命令包

```Makefile
name= f1 f2

define name
命令
endef
```

* 变量用 $(name) 引用
* make 可以使用通配符
* 预设变量
    * `@` 目标文件
    * `<` 第一个依赖文件
    * `^` 所有依赖文件

### 伪目标

```Makefile
.PHONY : clean
clean :
    -rm edit $(objects) # 实现 make clean
```

* 伪目标也可以有依赖, 类似子命令
* 经常声明伪目标 `all` 放在第一个目标, 因为无参数的 `make` 默认构建第一个目标

## Cmake

* `CMakeLists.txt`

```CMakeLists
# PROJECT_BINARY_DIR是cmake系统变量,意思是执行cmake命令的目录

cmake_minimum_required (VERSION 2.8)
# 要求cmake版本

project (learn_cmake)
# 指定项目名称

include_directories ( dir )
# 将dir目录加入头文件搜索路径

add_subdirectory ( dir )
# 递归调用dir目录下的CMakeLists.txt

aux_source_directory(dir var)
# 将dir目录下的所有文件加入var

set(LIBRARY_OUTPUT_PATH ${PROJECT_BINARY_DIR}/lib)
# 指定库生成到lib目录
set(EXECUTABLE_OUTPUT_PATH ${PROJECT_BINARY_DIR}/bin)
# 指定可执行文件生成到bin目录

add_executable(hello ${var})
# 生成可执行文件
add_library(lib_name STATIC/SHARED ${var})
# 生成库文件

find_library(var lib_name lib_path1 lib_path2)
# 查找库,并把库的绝对路径和名称存储到第一个参数里

target_link_libraries ( hello lib1 lib2 )
# 将lib1 lib2加入target的链接库

add_compile_options ( hello PRIVATE "-Wall" )
# 将"-Wall"加入编译选项
```

* 执行 `cmake .` 生成 Makefile
* 执行 `make` 生成可执行文件
