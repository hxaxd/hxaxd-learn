# Shell 编程与文本处理

# Shell 基础

## 参考资料

- [命令行的艺术](https://github.com/jlevy/the-art-of-command-line/blob/master/README-zh.md)

## 帮助

- 面对一个 command, 你首先要知道它是可执行文件 shell 内置命令还是别名 `type command`
- 用 man 来查询帮助, 不是所有 shell 都提供 info/help, 用 apropos 去查找文档

```text
man 的代号
1 shell
2 内核可用
3 库
4 设备
5 配置
6 games
7 协议
8 管理命令
9 内核文件
```

### 开关机

- `sync` 数据写入磁盘
- `shutddown [时间] [消息]` 警告关机
- `reboot` 重启
- `poweroff` 关机

### 命令

```bash
tab # 补全
^+r # 查找历史
^+u/k # 删除命令
^+a/e # 移动光标
^+i # 清屏
shift+[PD/PU] # 翻页

history n # 显示历史
!command !! !n # 执行历史

alias/unalias # 别名

command1 | command2 # 管道 (前一个命令的输出作为后一个命令的输入)
```

### 通配符

```bash
# 通配符
# *任意
# ?只一个任意字符  
# [abc]任意其中一个
# [^abc]任意不在其中
# [0-9]
```

### 文件基本操作

```bash
cp # 复制 -r form obj
mv # 移动 form obj
mkdir # 建立目录
pwd # 输出当前目录
rmdir # 删除目录
rm # 删除

cd # 跳转目录
# .当前 ..父 -上 ~家 ~name name 的家

ls # 列出目录中文件 -al  -i 显示 inode

ln from obj 硬链接 -s 软

file filename # 看文件类型
find # 建议用 fd 代替
head/tail filename # 看文件头尾 tail -f 自动跟随新增 (实时监控)
more/less filename # 按页看文件
cat filename # 读文本文件 -n 行号 -s 多空行合并
od filename # 二进制看文件 -t x/c 16 进制/字符
wc filename # 统计

touch # 建立空文件/改时间

spilt -b/l # size/行 file 文件前缀 分割文件

rename from obj filename # 重命名
```

### 系统与编码差异

- dos 与 unix 换行符不同, dos 为 `\r\n`, unix 为 `\n`
- `dos2unix filename` 转换为 unix 格式
- `unix2dos filename` 转换为 dos 格式
- `file filename` 查看文件类型 (编码)
- `iconv -f from -t to filename` 转换编码

### 文件权限

```bash
chown name:group filename # 改文件归属 -R 递归
chmod [mode] filename -R # 递归

# mode:
# - u/g/o/a +/-/= r/w/x
# - xyz r/w/x=4/2/1 x/y/z=u/g/o(r+w+x) 如 777

umask # 打印文件默认权限 拿掉的权限累加
chattr -R +-ai # 只追加/不可修改 改变属性
lsattr # 显示属性 -a 隐藏
```

### 解压缩

```bash
- tar -jcv -f name.tar.bz2 # 打包压缩
- tar -jtv -f f... # 查询
- tar -jxv -f f... # 解压
```

---

# Shell 文本处理

## 参考资料

- [命令行的艺术](https://github.com/jlevy/the-art-of-command-line/blob/master/README-zh.md)

## 文本基本操作

```bash
sort file/stdio # 排序 -n/r/f/k 按数字大小 / 反向排 / 忽略大小写 / 排每行的第 n 个字段
uniq file # 去重复打印 -d/c 只显示重复 / 显示行重复次数
command | tee filename # 重定向加打印 -af add / 覆盖
cut -f n -d 'c' file # 按 c 为分割提取每行第 n 个字段
paste file1 file2 # 按行拼接
join f1 f2 # 若第一个字段相同, 拼接这行 -a1/2 不匹配的按谁来
```

- [diff 输出的格式](https://www.ruanyifeng.com/blog/2012/08/how_to_read_diff.html)

```bash
diff fromfile tofile # 文本对比-bBi 忽略连续空格/忽略空白行/忽略大小写 

cmp -l file1 file2 # 对比二进制 返回第一个不同

patch -pn # 根据 diff 输出文件来更改
patch -R -pn # 还原
```

## 正则

- `^` 指定后一个模式匹配字符串的开始
- `$` 指定前一个模式匹配字符串的结束
- `*` 匹配任意长度的字符
- `+` 匹配至少一个字符
- `?` 匹配零或一个字符
- `{n}` 匹配 n 个 `{n}` 前面的模式
- `{n, }` 匹配至少 n 个 `{n, }` 前面的模式
- `{n, m}` 匹配 n 到 m 个 `{n, m}` 前面的模式
- `[]` 匹配任意字符中的一个
- `[^]` 匹配任意字符中的一个 (取反)
- `|` 逻辑或, 连接两个模式
- `()` 分组
- `\\` 转义
- `模式一(?=模式二)` 正向前瞻, 匹配模式二前的模式一, 但不获取匹配结果
- `模式一(?!模式二)` 负向前瞻
- `(?<=模式二)模式一` 正向后顾
- `(?<!模式二)模式一` 负向后顾
- `[:classname:]` 匹配字符类
    - `[:alnum:]` 字母和数字
    - `[:alpha:]` 字母
    - `[:blank:]` 空格和制表符
    - `[:cntrl:]` 控制字符
    - `[:digit:]` 数字
    - `[:graph:]` 可打印字符
    - `[:lower:]` 小写字母

## `grep`

```bash
grep [option] pattern file # 查找文件中匹配的行

# -A<显示行数>:除了显示符合范本样式的那一列之外, 并显示该行之后的内容 
# -B<显示行数>:除了显示符合样式的那一行之外, 并显示该行之前的内容 
# -C<显示行数>:除了显示符合样式的那一行之外, 并显示该行之前后的内容 
# -v:显示不被 pattern 匹配到的行, 相当于 [^] 反向匹配
# -i:忽略大小写
# -n:显示行号
```

## `sed`

```bash
sed [options] 'command' file(s) # 逐行编辑
sed [options] -f scriptfile file(s) # 从文件中读取命令

# -n:不输出模式空间内容到屏幕, 即不自动打印, 只打印匹配到的行
# -i:直接将处理的结果写入文件

# command : 地址操作内容

# 不给地址:对全文进行处理
# n 指定的行
# 1, n 指定的行范围

sed -n '1~2p'  # 只打印奇数行  (1~2 从第 1 行, 一次加 2 行)
sed -n '2~2p'  # 只打印偶数行

# d:删除模式空间匹配的行, 并立即启用下一轮循环
# p:打印当前模式空间内容, 追加到默认输出之后
# a:在指定行后面追加文本, 支持使用 \n 实现多行追加
# i:在行前面插入文本, 支持使用 \n 实现多行追加
# c:替换行为单行或多行文本, 支持使用 \n 实现多行追加
# !:模式空间中匹配行取反处理
# s///:查找替换, 支持使用其它分隔符, s@@@, s###, 加 g 表示行内全局替换
```

## `awk`

- awk 使用 AWK 语言, 我实在不喜欢

---

# Shell 编程

## 参考资料

- [菜鸟教程](https://www.runoob.com/Linux/Linux-shell.html)

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

#### `printf` (可移植)

- `printf "%-10s %-8s %-4s\n" 姓名 性别 体重 kg` 格式化输出, 可以指定宽度, 类型, 并且随意使用转义字符

#### `test` (可移植)

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
