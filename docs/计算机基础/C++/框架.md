[makefile](https://seisman.github.io/how-to-write-makefile/overview.html)是实现自动化编译的关键

GNU make是makefile的一个实现,而Cmake可以跨平台编译makefile

## makefile
GNU的make工作时的执行步骤如下:
- 读入所有的Makefile  
顺序寻找文件名为 GNUmakefile 、 makefile 和 Makefile 的文件  
使用多条 -f 或 --file 参数,你可以指定多个makefile

- 读入被include的其它Makefile  
include 变量/文件/通配

- 初始化文件中的变量

- 推导隐式规则,并分析所有规则

- 为所有的目标文件创建依赖关系链  
`VPATH = dir:dir # 指定文件搜寻目录`

- 根据依赖关系,决定哪些目标要重新生成

- 执行生成命令  
在命令前面加上-,表示忽略错误
### 小心环境变量MAKEFILES
### make可以一定程度上的自动推导

### make基础语法
```make
targets : prerequisites
    command # 注意这个tab必须存在
    ...
```
### 变量与命令包
```make
name= f1 f2

define name
命令
endef
```
都用$(name)引用

### 伪目标
```
.PHONY : clean
clean :
    -rm edit $(objects) # 实现 make clean
```
伪目标也可以有依赖,类似子命令

## Cmake
CMakeLists.txt
```cmake
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
