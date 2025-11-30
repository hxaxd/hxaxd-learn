# Shell 脚本

## 参考资料

- [菜鸟教程](https://www.runoob.com/Linux/Linux-shell.html) - 清晰明了即可 - 5

### 基本

- `#!` 是一个约定的标记, 用于指定脚本解释器
- `zsh test.sh` 以这种方式运行的脚本忽略指定
- `#` 注释

```bash
#!/bin/bash
echo "Hello World !"
```

### 变量

- 类似 py 的声明方式, `=` 两侧不能有空格
- `${name}` 使用变量 (包括在字符串中展开)
- `readonly name` 声明变量只读 (不是声明变量时)
- `unset` 删除变量
- `declare/typeset -i my_integer=42` 声明变量类型, `-i` 整数

```bash
name="abc$LANG"->abczh_CN...
name='abc\&LANG'->abc&LANG
# 引号的区别
```

#### 字符串

- `${name:1:4}` 提取子字符串
- `${name:(-1)}` 提取最后一个字符
- `${name:0:-1}` 提取除了最后一个字符的所有字符
- `echo 反引 expr index "$string" io 反引` 查找字符位置 (i 或 o)

### 数组

- `val=${array_name[n]}` 获取元素
- `val=${array_name[@]}` 获取所有元素
- `len=${#array_name[@]}` 获取元素数量
- `len=${#array_name[*]}` 获取元素长度
- `declare -A map` 声明数组类型 `-A` 关联数组 (字典), `-a` 数组
- `echo "数组的键为: ${!site[*]}"` 所有键

### 参数

- 环境变量
- `$0` 脚本名称
- `$1`, `$2` 脚本参数
- `$#` 参数数量
- `$?` 上一个命令的退出状态
- `$*` 所有参数 (字符串形式)
- `$$` 当前进程 ID 号
- `$!` 后台运行的最后一个进程的 ID
- `$-` 显示 Shell 使用的当前选项, 与 set 命令功能相同

### 运算符

#### 算术

- `expr $a + $b` 其中 `expr` 用于表达式计算
- 注意, 赋值左值无需 `$`
- `[ $a ==/!= $b ]` 注意所有空格必要

#### 关系

- `-eq` 相等
- `-ne` 不相等
- `-gt` 大于
- `-lt` 小于
- `-ge` 大于等于
- `-le` 小于等于
- `[ $a -eq $b ]` 注意所有空格必要

#### 布尔

- `-a` 与
- `-o` 或
- `!` 非

#### 字符串相关

- `=` 相等
- `!=` 不相等
- `-z` 空
- `-n` 非空
- `$` 字符串长度

#### 文件测试

- `-e` 存在
- `-d` 目录
- `-f` 普通文件
- `-c` 字符设备文件 如键盘
- `-b` 块设备文件 如硬盘
- `-s` 非空
- `-r` 可读
- `-w` 可写
- `-x` 可执行
- `-g` SGID
- `-u` SUID
- `-k` 设置粘着位
- `-p` 有名管道
- `-s` 套接字
- `-L` 符号链接

#### 其它

- `let name++/--` 自增 / 自减
- `a=$((a+1))` 算术
- `((a++/--))` 自增 / 自减

### 命令

#### `echo`

- `echo "\"It is a test\""` 转义
- `echo -e "OK! \n"` `-e` 后 `\n` 换行 `\c` 跟下一行连接
- `echo "It is a test" > myfile` 重定向
- `echo 反引 date 反引` 显示命令结果

#### `printf`(可移植)

- `printf "%-10s %-8s %-4s\n" 姓名 性别 体重 kg` 格式化输出, 可以指定宽度, 类型, 并且随意使用转义字符

#### `test`(可移植)

- `test 布尔/字符串/文件测试运算式` 返回真值

### 流程控制

#### `if`

```bash
if test condition
then
    command1
elif (( a<b ))
then 
    command2
else
    commandN
fi
```

#### `for`

```bash
for var in item1 item2 ... itemN
do
    command1
    command2
    ...
    commandN
done
```

#### `while`与`until`

```bash
int=1
while(( $int<=5 )) # until 与之相反
do
    echo $int
    let "int++"
done
```

#### `case`

```bash
#!/bin/sh

site="runoob"

case "$site" in
   "runoob") echo "菜鸟教程" 
   ;;
   "google") echo "Google 搜索" 
   ;;
   "taobao") echo "淘宝网" 
   ;;
esac
```

#### `break`与`continue`

- 词义自明

### 函数

```bash
[ function ](可选) fun_name ()
{
    action;

    [return int;](可选, int 为 0-255)
}
```

### 输入 / 输出重定向

- `command > / < / >> file` 重定向
- `command` 的 `stdin/stdout/stderr` 对应 `0/1/2` 因此有 `command 2>&1`
- `/dev/null` 黑洞

```bash
$ wc -l << EOF  # Here Document 将 EOF 中的内容作为 command 的输入
    欢迎来到
    菜鸟教程
    www.runoob.com
EOF
```

### 文件包含

```bash
#!/bin/bash
# author:菜鸟教程
# url:www.runoob.com

#使用 . 号来引用 test1.sh 文件
. ./test1.sh

# 或者使用以下包含文件代码
# source ./test1.sh

echo "菜鸟教程官网地址:$url"
```
